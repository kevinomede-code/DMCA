# alignedge/ — Startup workspace

Cartella dedicata al lavoro sulla startup **AlignEdge**.

Tenuta separata da `systemX/` (collaborazione di ricerca) e dalla radice della tesi per disciplina di IP — vedi `00_IP_strategy_memo.md`.

---

## Struttura

```
alignedge/
├── README.md                              ← questo file (mappa)
├── 00_IP_strategy_memo.md                 ← strategia IP a 3 layer, leggi PRIMA di qualunque firma
├── email_drafts_polito.md                 ← draft email RIMIN + TRIN al Polito TTO
│
├── AlignEdge_BMC.docx                     ← Business Model Canvas completo
├── AlignEdge_pitch.docx                   ← pitch playbook italiano (v1)
├── AlignEdge_pitch_EN.docx                ← pitch playbook inglese (v1)
│
├── why_me/                                ← work-in-progress sull'insight founder-fit
│   └── 00_working_draft.md
│
├── pitch/                                 ← tutto quello che serve per pitchare
│   ├── content_skeleton.md                ← single source of truth per il deck (10 slide + spec visual)
│   ├── delivery_script.md                 ← script 6:20 verbatim con pause markers
│   └── qa_prep.md                         ← 10 kill questions con model answers
│
├── partners/                              ← briefing per meeting con partner
│   └── edgenext/
│       └── friday_briefing.md             ← prep meeting EdgeNext
│
├── __AlignEdge_Pitch_Deck_Design.pdf      ← deck finale rendered (v3)
└── __AlignEdge_Pitch_Deck_Design.pptx     ← deck finale source (v3)
```

---

## Come navigare

### Per pitchare adesso
- Deck: `__AlignEdge_Pitch_Deck_Design.pdf`
- Script: `pitch/delivery_script.md`
- Difesa Q&A: `pitch/qa_prep.md`

### Per iterare sul contenuto
- Single source of truth testo: `pitch/content_skeleton.md`
- Insight founder-fit: `why_me/00_working_draft.md`

### Per meeting partner
- EdgeNext (venerdì): `partners/edgenext/friday_briefing.md`
- Nuovi partner: crea `partners/<name>/briefing.md` con stesso pattern

### Per decisioni IP / firma contratti
- **Leggi PRIMA** `00_IP_strategy_memo.md`
- Poi email TTO: `email_drafts_polito.md`
- NON firmare nulla senza legal review

---

## Da aggiungere (roadmap prossimi 60 giorni)

**Post-Friday EdgeNext:**
- `partners/edgenext/follow_up.md` — riassunto post-meeting + decisione scenario
- `partners/edgenext/term_sheet_draft.md` (solo se scenario A/B emerge)

**Post-difesa tesi (Luglio 2026):**
- `operations/audit_playbook_v0.md` — protocollo audit MVP standard
- `operations/scope_letter_template.md` — dopo TTO advice
- `operations/nda_template.md` — dopo TTO advice
- `operations/report_template.md` — template report 15-page consegnato al customer

**Post-primo audit (Q1 2027):**
- `operations/audit_dataset/` — dataset proprietario che compounds
- `partners/[first_customer_name]/case_study.md`

**Fase raise (Q2-Q3 2027):**
- `raise/one_pager.md`
- `raise/data_room/` (contro-corrente del programma "no data room" — solo per Series A)

---

## Version log

- 2026-06-25: creazione cartella + IP memo + email drafts
- 2026-06-29: BMC + pitch playbook IT
- 2026-07-01: pitch playbook EN
- 2026-07-03: why_me/ working draft + pitch/content_skeleton.md
- 2026-07-05: dashboard integrata slide 3 · iterazioni content · deck v3 finalizzato · delivery_script + qa_prep salvati · partners/edgenext/ creata per Friday briefing
