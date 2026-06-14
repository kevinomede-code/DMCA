"""
llm_router.py
=============
Router intelligente per thesis-research.

WATERFALL DAL PIÙ ECONOMICO AL PIÙ COSTOSO:

  TIER 0 — Llama3:latest via Ollama  (ID: 365c0bd3c000)  → GRATIS
  TIER 1 — Claude Haiku 4.5                               → $1/$5  per MTok
  TIER 2 — Claude Sonnet 4.6                              → $3/$15 per MTok
  TIER 3 — Claude Opus 4.6                                → $5/$25 per MTok

Regola:
  - Tutto ciò che Llama3 sa fare → Tier 0 (gratis, privato, locale)
  - Qualità Anthropic necessaria, task semplice/definito → Tier 1 Haiku
  - Ragionamento profondo, analisi strategica tesi → Tier 2 Sonnet
  - Decisioni critiche e rare → Tier 3 Opus

Risparmio extra Anthropic:
  - Batch API: -50% (asincrono, 24h window) → usa per paper scoring massivo
  - Prompt caching: -90% su input ripetuto  → usa per system prompt fisso
"""

import os
import json
import requests
import anthropic
from loguru import logger
from dotenv import load_dotenv

load_dotenv()

# ─── Configurazione ────────────────────────────────────────────────────────────

OLLAMA_URL    = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL  = os.getenv("OLLAMA_MODEL", "llama3:latest")  # ID: 365c0bd3c000
ANTHROPIC_KEY = os.getenv("ANTHROPIC_API_KEY")

MODELS = {
    0: {"id": OLLAMA_MODEL,
        "label": "Llama3:latest (Ollama)",
        "input": 0.0, "output": 0.0},
    1: {"id": "claude-haiku-4-5-20251001",
        "label": "Claude Haiku 4.5",
        "input": 1.0, "output": 5.0},
    2: {"id": "claude-sonnet-4-6",
        "label": "Claude Sonnet 4.6",
        "input": 3.0, "output": 15.0},
    3: {"id": "claude-opus-4-6",
        "label": "Claude Opus 4.6",
        "input": 5.0, "output": 25.0},
}

# ─── Mappa task → tier ─────────────────────────────────────────────────────────

TASK_ROUTING = {

    # TIER 0 — Llama3 locale (gratis, tutto ciò che è ripetitivo)
    "score_abstract":        0,  # score 0-10 abstract vs 5 gap
    "classify_paper":        0,  # foundamenta / gap-evidence / future
    "generate_queries":      0,  # varianti query di ricerca
    "extract_metadata":      0,  # autori, anno, venue da testo
    "format_bibtex":         0,  # formatta entry BibTeX
    "clean_text":            0,  # pulizia testo grezzo da PDF
    "summarize_chunk":       0,  # riassunto chunk RAG (max 400 tok)
    "translate_abstract":    0,  # traduci abstract EN→IT
    "generate_qa_pairs":     0,  # coppie Q&A sintetiche per fine-tuning
    "log_parsing":           0,  # parsing log PLC/SCADA
    "drift_label":           0,  # etichetta punto drift in serie temporale
    "constraint_extract":    0,  # estrai vincoli da AAS JSON strutturato
    "benchmark_label":       0,  # etichetta riga risultato benchmark

    # TIER 1 — Claude Haiku 4.5 ($1/$5)
    # Task definiti che richiedono qualità Anthropic
    "zotero_note":           1,  # nota Zotero: implicazione paper per tesi
    "search_query_refine":   1,  # raffina query di ricerca complessa
    "benchmark_interpret":   1,  # interpreta singolo risultato benchmark
    "aas_validate":          1,  # valida coerenza AAS generato
    "model_recommend_fast":  1,  # raccomandazione rapida modello HF
    "constraint_validate":   1,  # valida logica vincoli estratti da DT

    # TIER 2 — Claude Sonnet 4.6 ($3/$15)
    # Ragionamento profondo — default per analisi strategiche tesi
    "analyze_implications":  2,  # implicazioni strategiche paper per tesi
    "gap_decision":          2,  # quale gap copre paper ambiguo
    "weekly_report":         2,  # report autoresearch settimanale
    "architecture_review":   2,  # revisione coerenza architettura
    "thesis_section_draft":  2,  # bozza sezione tesi
    "experiment_design":     2,  # design esperimento validazione cap.7
    "model_recommend_deep":  2,  # raccomandazione con rationale dettagliato
    "drift_cycle_analysis":  2,  # analisi ciclo DT→selection→drift→realign

    # TIER 3 — Claude Opus 4.6 ($5/$25)
    # Solo per decisioni critiche e rare (max 1-2 volte a settimana)
    "critical_gap_analysis": 3,  # gap con evidenza contraddittoria
    "thesis_contribution":   3,  # valutazione originalità contributo
    "final_validation":      3,  # validazione finale framework cap.7
}

# ─── Cost tracker sessione ─────────────────────────────────────────────────────

_costs = {
    t: {"calls": 0, "input_tok": 0, "output_tok": 0, "cost_usd": 0.0}
    for t in MODELS
}

# ─── Chiamate ai modelli ───────────────────────────────────────────────────────

def _call_ollama(prompt: str, system: str = "",
                 temperature: float = 0.1) -> str:
    full = f"{system}\n\n{prompt}" if system else prompt
    try:
        r = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={"model": OLLAMA_MODEL, "prompt": full,
                  "stream": False,
                  "options": {"temperature": temperature,
                               "num_predict": 1024}},
            timeout=120,
        )
        r.raise_for_status()
        text = r.json()["response"].strip()
        _costs[0]["calls"]      += 1
        _costs[0]["input_tok"]  += len(prompt.split())
        _costs[0]["output_tok"] += len(text.split())
        return text
    except Exception as e:
        logger.error(f"[Ollama] {e}")
        raise


def _call_anthropic(prompt: str, tier: int, system: str = "",
                    temperature: float = 0.3) -> str:
    if not ANTHROPIC_KEY:
        raise ValueError("ANTHROPIC_API_KEY mancante nel .env")
    client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)
    kwargs = {
        "model":      MODELS[tier]["id"],
        "max_tokens": 2048,
        "messages":   [{"role": "user", "content": prompt}],
    }
    if system:
        kwargs["system"] = system
    try:
        resp    = client.messages.create(**kwargs)
        text    = resp.content[0].text.strip()
        in_tok  = resp.usage.input_tokens
        out_tok = resp.usage.output_tokens
        cost    = (in_tok  * MODELS[tier]["input"] +
                   out_tok * MODELS[tier]["output"]) / 1_000_000
        _costs[tier]["calls"]      += 1
        _costs[tier]["input_tok"]  += in_tok
        _costs[tier]["output_tok"] += out_tok
        _costs[tier]["cost_usd"]   += cost
        logger.info(f"[{MODELS[tier]['label']}] "
                    f"in={in_tok} out={out_tok} cost=${cost:.5f}")
        return text
    except Exception as e:
        logger.error(f"[{MODELS[tier]['label']}] {e}")
        raise

# ─── Router principale ─────────────────────────────────────────────────────────

def route(task_type: str, prompt: str, system: str = "",
          temperature: float = 0.2, force_tier: int = None) -> str:
    """
    Chiama automaticamente il modello corretto per il task.

    Args:
        task_type:   chiave da TASK_ROUTING (es. "score_abstract")
        prompt:      testo del prompt
        system:      system prompt opzionale
        temperature: 0.0-1.0 (default 0.2 per task analitici)
        force_tier:  sovrascrive TASK_ROUTING (0=Llama3, 1=Haiku, 2=Sonnet, 3=Opus)
    """
    tier = force_tier if force_tier is not None else TASK_ROUTING.get(task_type, 0)
    logger.info(f"[Router] '{task_type}' → {MODELS[tier]['label']}")
    if tier == 0:
        return _call_ollama(prompt, system=system, temperature=temperature)
    return _call_anthropic(prompt, tier=tier, system=system,
                           temperature=temperature)

# ─── Funzioni helper pronte all'uso ───────────────────────────────────────────

def score_abstract(title: str, abstract: str, gaps_summary: str) -> dict:
    """Llama3 → score 0-10 paper vs 5 gap. Ritorna dict JSON."""
    prompt = f"""Sei un assistente di ricerca per una tesi magistrale.

I 5 gap della ricerca:
{gaps_summary}

Valuta questo paper:
TITOLO: {title}
ABSTRACT: {abstract}

Rispondi SOLO con JSON valido, nessun testo extra:
{{"score": <0-10>, "gap_numbers": [<lista 1-5>], "ruolo": "<foundamenta|gap-evidence|future|irrilevante>", "motivo": "<max 15 parole>"}}"""
    raw = route("score_abstract", prompt)
    try:
        s, e = raw.find("{"), raw.rfind("}") + 1
        return json.loads(raw[s:e])
    except Exception:
        return {"score": 0, "gap_numbers": [], "ruolo": "irrilevante",
                "motivo": "parsing error"}


def analyze_implications(title: str, abstract: str, gaps_summary: str) -> str:
    """Sonnet → analisi profonda implicazioni paper per tesi. Solo per score >= 8."""
    prompt = f"""Analizza le implicazioni strategiche di questo paper per la tesi.

PAPER: {title}
ABSTRACT: {abstract}

CONTESTO TESI: {gaps_summary}

Rispondi in italiano con:
1. Cosa copre (max 2 righe)
2. Cosa manca rispetto al contributo originale (max 2 righe)
3. Come citarlo — capitolo e ruolo specifico (max 2 righe)"""
    return route("analyze_implications", prompt)


def recommend_model(aas_constraints: dict, task: str) -> dict:
    """Haiku → raccomanda modello HF dato AAS + task. Ritorna dict JSON."""
    prompt = f"""Sei un orchestratore MAS per Industry 4.0.

VINCOLI AZIENDALI DAL DIGITAL TWIN:
{json.dumps(aas_constraints, indent=2, ensure_ascii=False)}

TASK: {task}

Scegli il modello HuggingFace più adatto.
Rispondi SOLO con JSON:
{{"model_id": "<hf model id>", "rationale": "<max 20 parole>", "adaptation": "<none|rag|lora|onnx>", "latency_ms": <numero>}}"""
    raw = route("model_recommend_fast", prompt)
    try:
        s, e = raw.find("{"), raw.rfind("}") + 1
        return json.loads(raw[s:e])
    except Exception:
        return {"model_id": "unknown", "rationale": "parsing error",
                "adaptation": "none", "latency_ms": 0}


# ─── Report costi ──────────────────────────────────────────────────────────────

def cost_report() -> str:
    lines = ["", "=" * 55, "REPORT COSTI SESSIONE", "=" * 55]
    total = 0.0
    for tier, d in _costs.items():
        if d["calls"] == 0:
            continue
        label = MODELS[tier]["label"]
        lines.append(f"\n{label}")
        lines.append(f"  Chiamate : {d['calls']}")
        lines.append(f"  Token in : {d['input_tok']:,}")
        lines.append(f"  Token out: {d['output_tok']:,}")
        if tier == 0:
            lines.append(f"  Costo    : GRATIS")
        else:
            lines.append(f"  Costo    : ${d['cost_usd']:.5f}")
            total += d["cost_usd"]
    lines.append(f"\nTOTALE API ANTHROPIC: ${total:.5f}")
    lines.append("=" * 55)
    return "\n".join(lines)


# ─── DMCA Stage 5 helpers ─────────────────────────────────────────────────────

# Add Stage 5 copilot task types to routing table
TASK_ROUTING.update({
    "copilot_pre_swap":  1,   # Haiku: pre-swap operator explanation
    "copilot_post_swap": 1,   # Haiku: post-swap monitoring briefing
    "label_drift_type":  0,   # Llama3: label a drift event from features
})


class LLMRouter:
    """Class-based wrapper around the functional router.

    Used by pipeline/realignment.py so it can call:
        router = LLMRouter()
        text = router.call(prompt, tier=1, max_tokens=300)

    This avoids circular imports and provides a cleaner interface for
    Stage 5 copilot calls that need explicit tier control.
    """

    def call(
        self,
        prompt:     str,
        tier:       int   = 0,
        max_tokens: int   = 512,
        system:     str   = "",
        temperature: float = 0.2,
    ) -> str:
        """Call the LLM at the given tier directly (bypasses task routing).

        Args:
            prompt:      User prompt text.
            tier:        0=Llama3, 1=Haiku, 2=Sonnet, 3=Opus.
            max_tokens:  Maximum tokens in response (passed to Anthropic only).
            system:      Optional system prompt.
            temperature: Sampling temperature.

        Returns:
            LLM response string.
        """
        logger.info(f"[LLMRouter.call] tier={tier}, model={MODELS[tier]['label']}")
        if tier == 0:
            return _call_ollama(prompt, system=system, temperature=temperature)
        return _call_anthropic(prompt, tier=tier, system=system,
                               temperature=temperature, max_tokens=max_tokens)


def generate_copilot_explanation(
    drift_type:     str,
    active_model:   str,
    candidate_model: str,
    asset_id:       str,
    improvement_pct: float,
    severity:       str,
    sil_level:      int,
) -> str:
    """Generate a human-readable pre-swap explanation for the operator.

    Called by Stage 5 before COPILOTCONFIRM gate.
    Uses Haiku for SIL < 2, Sonnet for SIL >= 2 (safety-critical).

    Returns explanation string in Italian (operator language).
    """
    prompt = (
        f"Sistema DMCA: drift '{drift_type}' (severita={severity}) rilevato "
        f"sull'asset '{asset_id}' (SIL={sil_level}).\n"
        f"Modello attivo: '{active_model}'.\n"
        f"Candidato proposto: '{candidate_model}' "
        f"(miglioramento atteso MAE: +{improvement_pct:.1f}%).\n\n"
        f"Spiega in 3 frasi brevi (in italiano, per operatore non tecnico):\n"
        f"1. Perché si raccomanda lo swap ora.\n"
        f"2. Cosa potrebbe andare storto.\n"
        f"3. Cosa monitorare nelle prossime ore dopo lo swap."
    )
    task = "copilot_pre_swap"
    if sil_level >= 2:
        return route(task, prompt, force_tier=2)  # Sonnet for safety-critical
    return route(task, prompt)


def label_drift_type(
    features: dict[str, float],
    mae_at_detection: float,
    baseline_mae: float,
) -> str:
    """Use Llama3 to label a drift event from Layer 2 features.

    Called when DMCADriftDetector returns UNCLASSIFIED and a human-readable
    label is needed for the audit trail or copilot explanation.

    Returns one of: abrupt / gradual / incremental / variance_shift /
                    distribution_shift / outlier_driven / unclassified
    """
    prompt = (
        f"Sei un esperto di concept drift per serie temporali industriali.\n"
        f"Un detector ha prodotto queste feature al momento della rilevazione:\n"
        f"{json.dumps(features, indent=2)}\n"
        f"MAE al momento della rilevazione: {mae_at_detection:.4f}\n"
        f"MAE baseline: {baseline_mae:.4f}\n\n"
        f"Classifica il tipo di drift. Rispondi SOLO con una parola fra:\n"
        f"abrupt / gradual / incremental / variance_shift / "
        f"distribution_shift / outlier_driven / unclassified"
    )
    raw = route("label_drift_type", prompt).strip().lower()
    valid = {"abrupt", "gradual", "incremental", "variance_shift",
             "distribution_shift", "outlier_driven", "unclassified"}
    for token in raw.split():
        if token in valid:
            return token
    return "unclassified"


# ─── Test di connessione ───────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys

    print("=" * 55)
    print("TEST ROUTER LLM")
    print("=" * 55)

    # Test Ollama
    print("\n1. Test Ollama (Llama3)...")
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        names = [m["name"] for m in r.json().get("models", [])]
        print(f"   ✓ Ollama attivo. Modelli: {names}")
    except Exception as e:
        print(f"   ✗ Ollama non raggiungibile: {e}")
        print("   → Avvia con: ollama serve")
        sys.exit(1)

    # Test score_abstract con Llama3
    print("\n2. Test score_abstract (Llama3 - gratis)...")
    gaps = """
GAP 1: Selezione adattiva modelli HF guidata da Digital Twin constraints
GAP 2: Integrazione time-series + LLM nello stesso orchestratore
GAP 3: XAI conversazionale integrata nel dialogo
GAP 4: Framework validazione industriale (safety + latenza)
GAP 5: Fiducia calibrata nel tempo"""

    result = score_abstract(
        title="Recommending Pre-Trained Models for IoT Devices",
        abstract="We identify limitations of current model recommendation approaches "
                 "regarding hardware constraints and introduce a novel hardware-aware "
                 "method for PTM selection for IoT edge devices.",
        gaps_summary=gaps,
    )
    print(f"   Risultato: {result}")

    # Test recommend_model con Haiku (richiede API key)
    if ANTHROPIC_KEY:
        print("\n3. Test recommend_model (Haiku $1/$5)...")
        aas = {
            "hardware": "jetson_nano",
            "ram_gb": 4,
            "latency_sla_ms": 50,
            "sensors": ["vibration_10hz", "temperature"],
            "data_available": "zero_shot",
            "protocol": "OPC-UA",
        }
        rec = recommend_model(aas, "time_series_anomaly_detection")
        print(f"   Raccomandazione: {rec}")
    else:
        print("\n3. Skipping Haiku test (ANTHROPIC_API_KEY non configurata)")

    print(cost_report())