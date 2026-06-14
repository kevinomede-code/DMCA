"""
modal_mae_completion.py
=======================
Completa le 5 MAE mancanti nel benchmark canonico 2026-04-07.

Modelli target (CMAPSS FD001, sensor s2, split=train, seed=42):
  - Salesforce/moirai-1.1-R-small
  - Salesforce/moirai-1.1-R-large
  - amazon/chronos-t5-tiny
  - amazon/chronos-t5-large
  - time-series-foundation-models/Lag-Llama

NON tocca il benchmark canonico — salva in results/benchmarks/2026-04-27/.

App: "thesis-mae-completion"
Secrets: "thesis-secrets" (stesso del canonico)

Deploy:
    python -m modal deploy pipeline/modal_mae_completion.py

Run:
    python run_mae_completion.py
"""

from __future__ import annotations

import datetime
import os
import time
from typing import Any

import modal

# ─── App (separata dal benchmark canonico) ────────────────────────────────────

app = modal.App("thesis-mae-completion")
thesis_secrets = modal.Secret.from_name("thesis-secrets")

# ─── Image: stessa base del canonico + chronos-forecasting ───────────────────
# chronos-forecasting: API ufficiale Amazon Chronos per output distribuzionale.
# Richiede transformers>=4.37 e torch>=1.9 — già soddisfatti.

image_mae = (
    modal.Image.debian_slim(python_version="3.11")
    .apt_install("git")
    .pip_install(
        "torch>=2.1.0",
        # Pin <5: chronos-forecasting is incompatible with transformers 5.x
        # (raises TypeError: not a string during model loading / generate())
        "transformers>=4.40.0,<5",
        "datasets>=2.19.0",
        "numpy",
        "pandas",
        "scikit-learn",
        "loguru",
        "huggingface_hub",
        "scipy",
        "sentencepiece",
        "safetensors",
        "gluonts>=0.15,<0.16",
        "hydra-core==1.3.2",
        "omegaconf>=2.3",
        "accelerate>=0.27.0",
    )
    .run_commands(
        "pip install 'jax[cpu]' --quiet",
        "pip install uni2ts --no-deps --quiet",
        "pip install 'einops==0.7.*' 'jaxtyping>=0.2.28,<0.3' --quiet",
        # chronos-forecasting: ChronosPipeline → output distribuzionale → mediana
        "pip install chronos-forecasting --quiet",
        # Lag-Llama: solo da GitHub
        "pip install git+https://github.com/time-series-foundation-models/lag-llama.git --quiet",
    )
)

# ─── Costanti ─────────────────────────────────────────────────────────────────

CMAPSS_DATASET = "LucasThil/nasa_turbofan_degradation_FD001"
PRED_LEN = 24        # stesso del benchmark canonico
N_REPS   = 20        # stesso del benchmark canonico
SEED     = 42        # documentato: run canonico non aveva seed esplicito
CONTEXT_LEN = 128    # stesso del benchmark canonico (model_context_len default Moirai)

MODELS_TO_COMPLETE = [
    "Salesforce/moirai-1.1-R-small",
    "Salesforce/moirai-1.1-R-large",
    "amazon/chronos-t5-tiny",
    "amazon/chronos-t5-large",
    "time-series-foundation-models/Lag-Llama",
]
_CODE_VERSION = "v4-lag-llama-sliding-window"  # force container refresh


# ══════════════════════════════════════════════════════════════════════════════
# FUNZIONE 1 — compute_mae_single
# GPU T4. Un modello per invocazione. Lanciata in parallelo da run_mae_suite.
# ══════════════════════════════════════════════════════════════════════════════

@app.function(
    image=image_mae,
    gpu="t4",
    timeout=1800,
    max_containers=5,
    secrets=[thesis_secrets],
)
def compute_mae_single(model_id: str) -> dict[str, Any]:
    """
    Calcola MAE/RMSE + latenza per un modello su CMAPSS FD001 (sensor s2).

    Strategia MAE per output distribuzionale:
      - Chronos  : ChronosPipeline.predict() → mediana dei 20 campioni
      - Moirai   : MoiraiModule.forward() con patch reali → distr.mean o distr.loc
      - Lag-Llama: LagLlamaEstimator.create_predictor() con hp dal ckpt → media campioni

    Latenza: stessa tecnica del benchmark canonico per ciascun tipo.

    Ritorna dict con schema identico al CSV canonico.
    """
    import functools as _functools
    import traceback

    import numpy as np
    import torch
    from loguru import logger

    # Fix seed
    torch.manual_seed(SEED)
    np.random.seed(SEED)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(SEED)

    timestamp = datetime.datetime.utcnow().isoformat()
    hf_token  = os.environ.get("HF_TOKEN")
    device    = "cuda" if torch.cuda.is_available() else "cpu"

    logger.info(f"[{model_id}] device={device} seed={SEED} dataset={CMAPSS_DATASET}")

    # ── Carica CMAPSS FD001 sensor s2 ────────────────────────────────────────
    try:
        from datasets import load_dataset
        ds = load_dataset(CMAPSS_DATASET, trust_remote_code=True, token=hf_token)
        available = list(ds.keys())
        split = "train" if "train" in available else available[0]
        import pandas as pd
        df = ds[split].to_pandas()
        sensor_col = next(
            (c for c in df.columns if "sensor_2" in c.lower() or c.lower() == "s2"),
            None,
        )
        if sensor_col is None:
            numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
            sensor_col = numeric_cols[2] if len(numeric_cols) > 2 else numeric_cols[-1]
        series = df[sensor_col].dropna().values.astype(np.float32)
        logger.info(f"[{model_id}] CMAPSS: {len(series)} punti, col={sensor_col}, split={split}")
    except Exception as e:
        return {"error": f"dataset_load: {e}", "model_id": model_id,
                "dataset_name": CMAPSS_DATASET, "timestamp": timestamp, "status": "error"}

    ctx_real = series[:CONTEXT_LEN].astype(np.float32)
    gt_mae   = series[CONTEXT_LEN : CONTEXT_LEN + PRED_LEN].astype(np.float32)

    if len(gt_mae) < PRED_LEN:
        return {"error": "serie troppo corta per gt_mae", "model_id": model_id,
                "dataset_name": CMAPSS_DATASET, "timestamp": timestamp, "status": "error"}

    # ── Inizializza metriche ──────────────────────────────────────────────────
    mae_val      = None
    rmse_val     = None
    params_M     = 0.0
    load_time_s  = 0.0
    latencies_ms: list[float] = []
    chosen_split = split

    if torch.cuda.is_available():
        torch.cuda.reset_peak_memory_stats()

    try:
        t0_load = time.perf_counter()

        # ══════════════════════════════════════════════════════════════════════
        # CHRONOS (tiny e large)
        # ══════════════════════════════════════════════════════════════════════
        if "chronos" in model_id.lower():
            from chronos import ChronosPipeline

            # ChronosPipeline: carica modello + tokenizer in un colpo solo.
            # device_map="auto" lascia a accelerate la scelta dispositivo.
            # Richiede transformers<5 (pin nel image_mae).
            pipeline = ChronosPipeline.from_pretrained(
                model_id,
                device_map="auto",
                torch_dtype=torch.float32,
            )
            load_time_s = time.perf_counter() - t0_load
            try:
                params_M = sum(p.numel() for p in pipeline.model.parameters()) / 1e6
            except Exception:
                params_M = 8.39 if "tiny" in model_id else 708.96

            # Latenza: pipeline.predict() (include tokenizzazione + inferenza)
            # Coerente con il canonico che misura tokenize+generate insieme.
            ctx_tensor = torch.tensor(ctx_real).unsqueeze(0)  # [1, CONTEXT_LEN]
            for _ in range(N_REPS):
                t0 = time.perf_counter()
                pipeline.predict(ctx_tensor, prediction_length=PRED_LEN, num_samples=1)
                latencies_ms.append((time.perf_counter() - t0) * 1000)

            # MAE: mediana dei 20 campioni predittivi
            with torch.no_grad():
                samples = pipeline.predict(
                    ctx_tensor, prediction_length=PRED_LEN, num_samples=20,
                )
            # samples shape: [1, 20, PRED_LEN]
            median_pred = torch.median(samples[0], dim=0).values.cpu().numpy()
            n = min(len(median_pred), len(gt_mae))
            mae_val  = float(np.mean(np.abs(median_pred[:n] - gt_mae[:n])))
            rmse_val = float(np.sqrt(np.mean((median_pred[:n] - gt_mae[:n]) ** 2)))
            logger.info(f"[{model_id}] Chronos MAE={mae_val:.4f} RMSE={rmse_val:.4f}")

        # ══════════════════════════════════════════════════════════════════════
        # MOIRAI (small e large)
        # ══════════════════════════════════════════════════════════════════════
        elif "moirai" in model_id.lower():
            import jaxtyping as _jt
            if not hasattr(_jt, "PyTree"):
                _jt.PyTree = type
                import sys as _sys
                _sys.modules["jaxtyping"].PyTree = type

            from huggingface_hub import hf_hub_download, list_repo_files
            from safetensors.torch import load_file as st_load
            from uni2ts.model.moirai import MoiraiModule
            from uni2ts.distribution import StudentTOutput

            # Scarica checkpoint (stesso pattern del canonico)
            repo_files = list(list_repo_files(model_id, token=hf_token))
            MODEL_EXTS = (".ckpt", ".pt", ".pth", ".bin", ".safetensors")
            weight_files = [
                f for f in repo_files
                if any(f.endswith(ext) for ext in MODEL_EXTS) and "optimizer" not in f.lower()
            ]
            if not weight_files:
                raise FileNotFoundError(f"Nessun file modello in {model_id}")
            target = weight_files[0]
            ckpt = hf_hub_download(model_id, target, token=hf_token)

            # Architettura nota (identica al canonico)
            _moirai_configs = {
                "small": dict(d_model=384, num_layers=6,  patch_sizes=[8, 16, 32, 64, 128],
                              max_seq_len=512, attn_dropout_p=0.0, dropout_p=0.0),
                "large": dict(d_model=1024, num_layers=24, patch_sizes=[8, 16, 32, 64, 128],
                              max_seq_len=512, attn_dropout_p=0.0, dropout_p=0.0),
                "base":  dict(d_model=768, num_layers=12,  patch_sizes=[8, 16, 32, 64, 128],
                              max_seq_len=512, attn_dropout_p=0.0, dropout_p=0.0),
            }
            _size = next(
                (s for s in ("large", "base", "small") if s in model_id.lower()), "small"
            )
            module = MoiraiModule(distr_output=StudentTOutput(), **_moirai_configs[_size])

            if target.endswith(".safetensors"):
                sd = st_load(ckpt, device=device)
            else:
                sd = torch.load(ckpt, map_location=device, weights_only=False)
                if isinstance(sd, dict) and "state_dict" in sd:
                    sd = sd["state_dict"]

            missing, unexpected = module.load_state_dict(sd, strict=False)
            if missing or unexpected:
                logger.warning(f"[{model_id}] state_dict loose: "
                               f"missing={len(missing)}, unexpected={len(unexpected)}")
            module = module.to(device).eval()
            load_time_s = time.perf_counter() - t0_load
            params_M = sum(p.numel() for p in module.parameters()) / 1e6

            # Latenza: stesso input sintetico del canonico (1 patch da 128)
            _ps = 128
            _np_lat = 1
            with torch.no_grad():
                for _ in range(N_REPS):
                    t0 = time.perf_counter()
                    module(
                        target=torch.randn(1, _np_lat, _ps, device=device, dtype=torch.float32),
                        observed_mask=torch.ones(1, _np_lat, _ps, dtype=torch.bool, device=device),
                        sample_id=torch.zeros(1, _np_lat, dtype=torch.long, device=device),
                        time_id=torch.arange(_np_lat, device=device).unsqueeze(0),
                        variate_id=torch.zeros(1, _np_lat, dtype=torch.long, device=device),
                        prediction_mask=torch.zeros(1, _np_lat, dtype=torch.bool, device=device),
                        patch_size=torch.tensor(_ps, dtype=torch.long, device=device),
                    )
                    latencies_ms.append((time.perf_counter() - t0) * 1000)

            # MAE: context patch reale + prediction patch → distr.mean/loc
            # Layout: [ctx_patch | pred_patch], prediction_mask=[False, True]
            with torch.no_grad():
                target_ctx  = torch.tensor(
                    ctx_real[:_ps], dtype=torch.float32, device=device,
                ).reshape(1, 1, _ps)
                target_pred = torch.zeros(1, 1, _ps, device=device, dtype=torch.float32)
                target_full = torch.cat([target_ctx, target_pred], dim=1)  # [1, 2, 128]

                obs_mask = torch.ones(1, 2, _ps, dtype=torch.bool, device=device)
                obs_mask[0, 1, :] = False   # prediction slot: non osservato

                distr = module(
                    target=target_full,
                    observed_mask=obs_mask,
                    sample_id=torch.zeros(1, 2, dtype=torch.long, device=device),
                    time_id=torch.arange(2, device=device).unsqueeze(0),
                    variate_id=torch.zeros(1, 2, dtype=torch.long, device=device),
                    prediction_mask=torch.tensor([[False, True]], device=device),
                    patch_size=torch.tensor(_ps, dtype=torch.long, device=device),
                )

            # Estrai punto di previsione: prova mean → loc → campioni
            try:
                if hasattr(distr, "mean"):
                    pred_raw = distr.mean[0, 1, :PRED_LEN]
                elif hasattr(distr, "loc"):
                    pred_raw = distr.loc[0, 1, :PRED_LEN]
                else:
                    pred_raw = distr.rsample([20])[:, 0, 1, :PRED_LEN].mean(0)
                pred_mean = pred_raw.cpu().numpy()
            except Exception as e_distr:
                logger.warning(f"[{model_id}] distr.mean fallito ({e_distr}) — uso rsample")
                samp = distr.rsample([20])          # [20, batch, n_patch, patch_size]
                pred_mean = samp[:, 0, 1, :PRED_LEN].mean(0).cpu().numpy()

            n = min(len(pred_mean), len(gt_mae))
            mae_val  = float(np.mean(np.abs(pred_mean[:n] - gt_mae[:n])))
            rmse_val = float(np.sqrt(np.mean((pred_mean[:n] - gt_mae[:n]) ** 2)))
            logger.info(f"[{model_id}] Moirai MAE={mae_val:.4f} RMSE={rmse_val:.4f}")

        # ══════════════════════════════════════════════════════════════════════
        # LAG-LLAMA
        # ══════════════════════════════════════════════════════════════════════
        elif "lag-llama" in model_id.lower() or "lag_llama" in model_id.lower():
            import inspect as _inspect
            import pandas as pd

            _orig_load = torch.load
            torch.load = _functools.partial(_orig_load, weights_only=False)
            try:
                from huggingface_hub import hf_hub_download as _hf_dl
                ckpt_path = _hf_dl(
                    repo_id=model_id, filename="lag-llama.ckpt", token=hf_token
                )
                ckpt_data = torch.load(ckpt_path, map_location="cpu")
                hp = ckpt_data.get("hyper_parameters", {})
                logger.info(f"[{model_id}] hp keys: {list(hp.keys())}")

                # ── Latenza: stesso backbone forward del canonico ──────────────
                from lag_llama.gluon.lightning_module import LagLlamaLightningModule as _LLM
                _llm_sig = set(_inspect.signature(_LLM.__init__).parameters.keys()) - {"self"}
                _llm_kwargs = {k: v for k, v in hp.items() if k in _llm_sig}
                lightning_module = _LLM(**_llm_kwargs)
                lightning_module.load_state_dict(ckpt_data["state_dict"], strict=False)
                lightning_module = lightning_module.to(device).eval()
                params_M = sum(p.numel() for p in lightning_module.parameters()) / 1e6

                _ll_inner = (
                    lightning_module.model
                    if hasattr(lightning_module, "model")
                    else lightning_module
                )
                try:
                    _feature_size = _ll_inner.transformer.wte.weight.shape[1]
                except Exception:
                    _feature_size = 92  # fallback noto

                _ctx_len = int(hp.get("context_length", 32))
                load_time_s = time.perf_counter() - t0_load

                with torch.no_grad():
                    for _ in range(N_REPS):
                        t0 = time.perf_counter()
                        _x = torch.randn(1, _ctx_len, _feature_size, device=device)
                        _x = _ll_inner.transformer.wte(_x)
                        for _blk in _ll_inner.transformer.h:
                            _x = _blk(_x, False)
                        _x = _ll_inner.transformer.ln_f(_x)
                        _ll_inner.param_proj(_x)
                        latencies_ms.append((time.perf_counter() - t0) * 1000)

                # ── MAE: sliding window diretto sul backbone (bypassa GluonTS) ──
                # Il predictor GluonTS fallisce per incompatibilità API (lags_seq,
                # time_feat, field names). Usiamo il backbone direttamente:
                # per ogni step k=0..23, alimentiamo series[k:k+ctx_len] come
                # feature vettori costruiti manualmente con lag extraction,
                # prendiamo l'output all'ultimo token = previsione 1-step-ahead.
                # lags_seq è in hp["model_kwargs"], non al livello radice
                _model_kw = hp.get("model_kwargs", {}) or {}
                lags_seq = hp.get("lags_seq") or _model_kw.get("lags_seq")
                logger.info(f"[{model_id}] model_kw keys: {list(_model_kw.keys())[:20]}")
                if not lags_seq:
                    raise RuntimeError(
                        f"lags_seq non trovato. hp keys: {list(hp.keys())} "
                        f"model_kw keys: {list(_model_kw.keys())}"
                    )
                lags_seq = list(lags_seq)
                max_lag  = max(lags_seq)
                # time_feat_dim: dedotto da feature_size noto e len(lags_seq)
                # feature_size = 1 (target) + len(lags_seq) + time_feat_dim
                time_feat_dim = max(0, _feature_size - 1 - len(lags_seq))
                logger.info(
                    f"[{model_id}] feature_size={_feature_size}, "
                    f"n_lags={len(lags_seq)}, max_lag={max_lag}, "
                    f"time_feat_dim={time_feat_dim}"
                )

                pred_unscaled: list[float] = []
                for step in range(PRED_LEN):
                    # Finestra contestuale reale (non autoregressiva → niente error accumulation)
                    window = series[step : step + _ctx_len].astype(np.float32)
                    scale_w = float(np.mean(np.abs(window))) + 1e-10
                    ws = window / scale_w

                    # Pad per accedere ai lag senza out-of-bounds
                    pad_w = np.zeros(max_lag + _ctx_len, dtype=np.float32)
                    pad_w[max_lag:] = ws

                    # Costruisci matrice feature [ctx_len, feature_size]
                    feats: list[list[float]] = []
                    for t in range(_ctx_len):
                        at = max_lag + t
                        target_f = float(pad_w[at])
                        lag_fs   = [float(pad_w[at - lag]) if at - lag >= 0 else 0.0
                                    for lag in lags_seq]
                        time_fs  = [0.0] * time_feat_dim  # zero-fill time features
                        feats.append([target_f] + lag_fs + time_fs)

                    feat_t = torch.tensor(
                        [feats], dtype=torch.float32, device=device
                    )  # [1, ctx_len, feature_size]

                    with torch.no_grad():
                        _x = _ll_inner.transformer.wte(feat_t)
                        for _blk in _ll_inner.transformer.h:
                            _x = _blk(_x, False)
                        _x = _ll_inner.transformer.ln_f(_x)
                        _params = _ll_inner.param_proj(_x)

                    # param_proj → (loc, scale, df) come tuple, o tensor [..., 3]
                    # Primo parametro = loc della StudentT = previsione in spazio scalato
                    if isinstance(_params, (tuple, list)):
                        loc_t = _params[0][0, -1]           # [1] o scalar
                    elif isinstance(_params, torch.Tensor):
                        if _params.ndim == 3:
                            loc_t = _params[0, -1, 0]       # [batch, seq, n_params]
                        else:
                            loc_t = _params[0, -1]          # [batch, seq]
                    else:
                        loc_t = torch.tensor(0.0)

                    pred_unscaled.append(float(loc_t.squeeze().cpu()) * scale_w)

                gt_ll = series[_ctx_len : _ctx_len + PRED_LEN].astype(np.float32)
                n = min(len(pred_unscaled), len(gt_ll))
                pred_arr = np.array(pred_unscaled[:n])
                mae_val  = float(np.mean(np.abs(pred_arr - gt_ll[:n])))
                rmse_val = float(np.sqrt(np.mean((pred_arr - gt_ll[:n]) ** 2)))
                logger.info(f"[{model_id}] LagLlama MAE={mae_val:.4f} RMSE={rmse_val:.4f}")

            finally:
                torch.load = _orig_load

        else:
            return {
                "error": f"modello non gestito: {model_id}",
                "model_id": model_id, "dataset_name": CMAPSS_DATASET,
                "timestamp": timestamp, "status": "error",
            }

    except Exception as e:
        logger.error(f"[{model_id}] FALLITO: {e}\n{traceback.format_exc()}")
        return {
            "error": str(e), "model_id": model_id, "dataset_name": CMAPSS_DATASET,
            "timestamp": timestamp, "status": "error",
        }

    # ── Metriche finali ───────────────────────────────────────────────────────
    lat_arr    = np.array(latencies_ms) if latencies_ms else np.array([0.0])
    ram_gpu_mb = (
        int(torch.cuda.max_memory_allocated() // (1024 ** 2))
        if torch.cuda.is_available() else 0
    )

    logger.info(
        f"[{model_id}] OK — lat={lat_arr.mean():.1f}ms p95={np.percentile(lat_arr, 95):.1f}ms "
        f"ram={ram_gpu_mb}MB params={params_M:.2f}M mae={mae_val} rmse={rmse_val}"
    )

    return {
        "model_id":        model_id,
        "dataset_name":    CMAPSS_DATASET,
        "split":           chosen_split,
        "params_M":        round(params_M, 2),
        "load_time_s":     round(load_time_s, 3),
        "latency_mean_ms": round(float(lat_arr.mean()), 3),
        "latency_p95_ms":  round(float(np.percentile(lat_arr, 95)), 3),
        "latency_min_ms":  round(float(lat_arr.min()), 3),
        "ram_gpu_mb":      ram_gpu_mb,
        "mae":             round(mae_val, 6)  if mae_val  is not None else None,
        "rmse":            round(rmse_val, 6) if rmse_val is not None else None,
        "device":          device,
        "dtype":           "float32",
        "n_reps":          N_REPS,
        "timestamp":       timestamp,
        "status":          "ok",
    }


# ══════════════════════════════════════════════════════════════════════════════
# FUNZIONE 2 — run_mae_suite
# Coordinator CPU. Lancia compute_mae_single.map() in parallelo per i 5 modelli.
# ══════════════════════════════════════════════════════════════════════════════

@app.function(
    image=image_mae,
    timeout=3600,
    secrets=[thesis_secrets],
)
def run_mae_suite(models: list[str] | None = None) -> dict[str, Any]:
    """
    Lancia compute_mae_single in parallelo per ogni modello.
    Ritorna dict con results + dataframe_dict (schema identico al CSV canonico).
    """
    import pandas as pd
    from loguru import logger

    if models is None:
        models = MODELS_TO_COMPLETE

    logger.info(f"MAE suite: {len(models)} modelli in parallelo")

    results: list[dict[str, Any]] = []
    for result in compute_mae_single.map(models):
        results.append(result)
        status = result.get("status", result.get("error", "?"))
        logger.info(f"  {result.get('model_id')} → {status} "
                    f"mae={result.get('mae')} rmse={result.get('rmse')}")

    df = pd.DataFrame(results)
    try:
        df.to_csv("/tmp/benchmark_mae_completion.csv", index=False)
    except Exception as e:
        logger.error(f"CSV /tmp write fallito: {e}")

    ok_count = int((df.get("status") == "ok").sum()) if "status" in df.columns else 0
    return {
        "total":          len(models),
        "completed":      len(results),
        "successful":     ok_count,
        "failed":         len(results) - ok_count,
        "results":        results,
        "dataframe_dict": df.to_dict(orient="records"),
    }
