# DMCA — Design Decisions Log

Questa cartella documenta le scelte implementative non ovvie del framework DMCA.
Ogni file descrive UN modulo o UN problema specifico, con:

- **Problema**: cosa non funzionava o perché non era ovvio
- **Opzioni valutate**: alternative considerate
- **Scelta adottata**: cosa è stato implementato
- **Ragione**: perché questa opzione
- **Trade-off**: cosa si perde
- **Verifica**: come si misura che funziona
- **Riferimento codice**: riga/funzione specifica

## File presenti

| File | Modulo | Data |
|------|--------|------|
| [01_aas_type1_vs_sdk.md](01_aas_type1_vs_sdk.md) | aas_parser.py | 2026-04-21 |
| [02_topsis_latency_margin.md](02_topsis_latency_margin.md) | topsis_ranker.py | 2026-04-21 |
| [03_topsis_mae_999_sentinel.md](03_topsis_mae_999_sentinel.md) | gaps.json / topsis_ranker.py | 2026-04-21 |
| [04_quality_gate_constant_prediction.md](04_quality_gate_constant_prediction.md) | quality_gate.py | 2026-04-21 |
| [05_dmca_drift_window_baseline.md](05_dmca_drift_window_baseline.md) | dmca_drift.py | 2026-04-21 |
| [06_dmca_drift_decision_tree.md](06_dmca_drift_decision_tree.md) | dmca_drift.py | 2026-04-21→22 |
| [07_quality_gate_latency_p95.md](07_quality_gate_latency_p95.md) | quality_gate.py | 2026-04-22 |
| [08_realignment_shadow_deploy.md](08_realignment_shadow_deploy.md) | realignment.py | 2026-04-22 |

## Come leggere questi file

Ogni documento è scritto per essere comprensibile da un revisore umano
senza accesso al codice. Il formato è pensato per essere citabile in tesi
come "nota metodologica" o "appendice implementativa".
