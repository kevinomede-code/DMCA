# DD-07 — P95 latency e moltiplicatore × 1.5 nel quality gate (CHECK 1)

**Data**: 2026-04-22
**Modulo**: `pipeline/quality_gate.py:_check_latency()`
**Stage DMCA**: Stage 3 — Edge Deployment

---

## Problema

CHECK 1 del quality gate deve decidere se la latenza di inferenza del modello
candidato è compatibile con il SLA dell'asset prima del deployment.

Tre sotto-problemi da risolvere insieme:

1. **Quale statistica usare** per riassumere la distribuzione delle latenze
   (media, mediana, P95, max)?
2. **Quante inferenze eseguire** per stimarla in modo affidabile?
3. **Quale threshold** usare rispetto al valore SLA dell'AAS?

---

## Opzioni valutate — statistica di latenza

| Statistica | Pro | Contro |
|------------|-----|--------|
| **Media** | Semplice, bassa varianza | Nasconde picchi; in ambito industriale un singolo superamento SLA può essere un missing alarm |
| **Mediana (P50)** | Robusta agli outlier | Ignora metà della distribuzione; troppo ottimista per SLA hard |
| **P95** | Standard de facto nei SLA industriali; cattura il 95° percentile dei picchi reali | Richiede ≥20 campioni per stabilità statistica |
| **Max** | Conservativo al massimo | Instabile con pochi campioni; un singolo spike CPU non rappresenta il regime normale |

---

## Opzioni valutate — numero di runs

| Schema | Pro | Contro |
|--------|-----|--------|
| 5 warmup + 5 test | Veloce | P95 su 5 campioni = 1 valore: statisticamente degenere |
| 5 warmup + 10 test | Accettabile | P95 = 10° valore; instabile su distribuzioni con spike |
| **5 warmup + 20 test** | Stabile: P95 = media del 19°-20° valore; tempo totale <2s su CPU edge | Trade-off ottimale |
| 5 warmup + 50 test | Alta stabilità | Overhead eccessivo per un gate che gira a ogni riallineamento |

---

## Opzioni valutate — threshold

| Threshold | Pro | Contro |
|-----------|-----|--------|
| `sla_ms` (strict) | Aderente allo spec formale | Stessa trappola di DD-02: dati T4 → P95 misurato su laptop ≠ P95 su device target |
| **`sla_ms × 1.5`** | Coerente con DD-02; lascia margine per variabilità del carico | Stesso argomento del TOPSIS: empirico, ma documentato |
| `sla_ms × 2.0` | Troppo permissivo | Lascerebbe passare modelli fuori SLA anche su device scarico |

---

## Scelta adottata

**P95 su 20 runs, dopo 5 warmup, con threshold `sla_ms × 1.5`.**

```python
# quality_gate.py:_check_latency()  (riga ~79-81)
p95_idx      = max(0, int(math.ceil(0.95 * len(latencies_sorted))) - 1)
p95_ms       = latencies_sorted[p95_idx]
threshold_ms = sla_ms * 1.5
passed       = p95_ms <= threshold_ms
```

---

## Ragione

### Perché P95 e non media

Nei sistemi industriali l'SLA latency è un contratto sul **tail** della
distribuzione, non sulla media. Un modello con media 40ms ma P99=200ms
supera l'SLA in un ciclo su cento — sufficiente a causare un missing alarm
in un contesto di predictive maintenance ad alta frequenza di campionamento.

P95 è il valore de facto nelle specifiche di latency SLA industria (AWS,
IEC 62264, PROFINET RT class B): cattura i picchi reali legati a GC,
scheduling OS, e burst di memoria, senza essere instabile come il max.

### Perché 5 warmup + 20 test

I primi run su CPU/JIT sono dominati dalla compilazione lazy (PyTorch) o dal
caricamento delle strutture dati del modello (sklearn). I 5 warmup discardati
portano il runtime al regime stazionario prima che inizino le misure.

20 runs danno un campione sufficiente per stimare il 95° percentile:
il P95 corrisponde al 19°-20° valore ordinato, che è stabile dopo ≥15 campioni.
Il tempo totale su un Ridge surrogate è <50ms; su un modello HF leggero <2s —
overhead accettabile per un gate che gira a ogni ciclo di riallineamento.

### Perché × 1.5, uguale a TOPSIS

**Coerenza con DD-02**: il moltiplicatore 1.5 in `filter_admissible()` nasce
dal fatto che i benchmark sono stati misurati su GPU T4, non su device edge.
Il quality gate usa lo stesso moltiplicatore per la stessa ragione:

- Le latenze di inferenza nel gate vengono misurate sul nodo di orchestrazione
  (laptop / cloud), non sul device target reale.
- Usare un moltiplicatore diverso (es. 1.2 nel gate, 1.5 nel TOPSIS) creerebbe
  un'incongruenza: un modello ammesso da TOPSIS potrebbe essere rifiutato dal
  gate per motivi puramente di calibrazione diversa, non di effettiva violazione
  SLA.
- La consistenza 1.5 / 1.5 garantisce che **ogni modello che supera il filtro
  TOPSIS abbia una ragionevole probabilità di superare anche il gate**,
  riducendo i falsi negativi costosi (riallineamento avviato, candidato rifiutato
  al gate, escalation inutile all'operatore).

---

## Trade-off accettato

- **Si perde**: rilevazione di violazioni SLA sottili (picchi al P99 non coperti
  dal P95), e allineamento esatto alla latenza reale su device target
- **Si guadagna**: gate stabile e coerente con TOPSIS; nessuna escalation
  inutile causata da soglie inconsistenti tra Stage 2 e Stage 3
- **Limitazione documentata**: "Phase 2 eseguirà il gate direttamente sul
  device target (Jetson Nano) eliminando il fattore 1.5"

---

## Verifica

```bash
python pipeline/quality_gate.py
# [TEST 1] Good surrogate model — expect PASS
#   latency P95=<X>ms OK
# Tutti i test PASSATI.
```

---

## Riferimento codice

- `pipeline/quality_gate.py:_check_latency()` — P95 computation, riga ~79
- `pipeline/quality_gate.py:run_quality_gate()` — default `warmup_runs=5, test_runs=20`
- `pipeline/topsis_ranker.py:filter_admissible()` — moltiplicatore × 1.5 (DD-02)

## Vedi anche

- **DD-02** — `02_topsis_latency_margin.md` — origine del moltiplicatore × 1.5
