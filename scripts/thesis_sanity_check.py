"""
Static sanity-check pass over thesis_draft.tex (no LaTeX compilation needed).

Reports:
- Undefined \\ref / \\eqref / \\autoref (label cited but not defined)
- Defined-but-unused labels
- Duplicate labels
- \\cite keys missing from references_master.bib
- \\includegraphics files not findable on disk
- \\begin/\\end mismatches
- Section/subsection structural overview
- Word count + rough page estimate (250 words/page for technical text)
"""
from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEX = ROOT / "thesis_draft.tex"
BIB = ROOT / "references_master.bib"
FIG_DIRS = [ROOT / "figures", ROOT / "results/figures"]

src = TEX.read_text(encoding="utf-8", errors="replace")

# ----- strip comments (LaTeX % comments, but keep \% as literal) -------------
def strip_comments(text: str) -> str:
    out_lines = []
    for line in text.splitlines():
        # find first unescaped %
        i = 0
        while i < len(line):
            if line[i] == "%" and (i == 0 or line[i - 1] != "\\"):
                line = line[:i]
                break
            i += 1
        out_lines.append(line)
    return "\n".join(out_lines)


body = strip_comments(src)

# ----- Labels and refs --------------------------------------------------------
labels = re.findall(r"\\label\{([^}]+)\}", body)
refs = re.findall(r"\\(?:ref|eqref|autoref|Cref|cref|nameref)\{([^}]+)\}", body)
ref_keys = []
for r in refs:
    ref_keys.extend(k.strip() for k in r.split(","))

label_set = set(labels)
ref_set = set(ref_keys)
undef_refs = sorted(ref_set - label_set)
unused_labels = sorted(label_set - ref_set)
dup_labels = [k for k, v in Counter(labels).items() if v > 1]

# ----- Citations --------------------------------------------------------------
cites = re.findall(r"\\cite[tp]?\*?\{([^}]+)\}", body)
cite_keys = set()
for c in cites:
    for k in c.split(","):
        cite_keys.add(k.strip())

bib_text = BIB.read_text(encoding="utf-8", errors="replace") if BIB.exists() else ""
bib_keys = set(re.findall(r"@\w+\s*\{\s*([^,\s]+)\s*,", bib_text))
missing_cites = sorted(cite_keys - bib_keys)
unused_bib = sorted(bib_keys - cite_keys)

# ----- includegraphics --------------------------------------------------------
fig_refs = re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", body)
fig_missing = []
fig_found = []
for f in fig_refs:
    name = Path(f).name
    found = None
    for d in FIG_DIRS:
        for ext in ("", ".pdf", ".png", ".jpg", ".jpeg", ".eps", ".tex"):
            cand = d / (name + ext)
            if cand.exists():
                found = cand
                break
        if found:
            break
    if found:
        fig_found.append((f, str(found.relative_to(ROOT))))
    else:
        fig_missing.append(f)

# ----- begin/end balance ------------------------------------------------------
begins = re.findall(r"\\begin\{([^}]+)\}", body)
ends = re.findall(r"\\end\{([^}]+)\}", body)
imbalance = []
for env, count in Counter(begins).items():
    if count != Counter(ends).get(env, 0):
        imbalance.append((env, count, Counter(ends).get(env, 0)))

# ----- structural overview ---------------------------------------------------
sections = []
section_re = re.compile(r"\\(section|subsection|subsubsection)\*?\{([^}]+)\}")
for m in section_re.finditer(body):
    level = {"section": 1, "subsection": 2, "subsubsection": 3}[m.group(1)]
    sections.append((level, m.group(2)))

# ----- word count and page estimate -------------------------------------------
# Strip common environments that bloat word count without producing pages
stripped = body
for env in ("equation", "equation*", "align", "align*", "tabular",
            "table", "table*", "figure", "figure*", "tikzpicture",
            "algorithm", "algorithmic", "verbatim", "lstlisting"):
    stripped = re.sub(
        rf"\\begin\{{{env}}}.*?\\end\{{{env}}}",
        " ",
        stripped,
        flags=re.DOTALL,
    )
# strip math
stripped = re.sub(r"\$[^$]*\$", " ", stripped)
# strip commands like \section{...}, \cite{...}, \label{...}
stripped = re.sub(r"\\[a-zA-Z]+\*?(\[[^\]]*\])?(\{[^}]*\})?", " ", stripped)
words = re.findall(r"[A-Za-z][A-Za-z\-']{2,}", stripped)
n_words = len(words)
# Technical IEEE-like: ~280 words/page (single-column 10pt with figures/tables
# accounting for ~30% of pages)
page_est = round(n_words / 280)

# ----- print report -----------------------------------------------------------
def hdr(title):
    print(f"\n=== {title} ===")

print(f"Source: {TEX.relative_to(ROOT)}  ({TEX.stat().st_size} bytes)")
print(f"Bib:    {BIB.relative_to(ROOT)}  ({len(bib_keys)} entries)")

hdr(f"REFS — undefined ({len(undef_refs)})")
for r in undef_refs:
    print(f"  ! \\ref{{{r}}} has no \\label")

hdr(f"REFS — defined-but-unused ({len(unused_labels)})")
for r in unused_labels[:30]:
    print(f"  - \\label{{{r}}} not referenced")
if len(unused_labels) > 30:
    print(f"  ... and {len(unused_labels) - 30} more")

hdr(f"REFS — duplicate labels ({len(dup_labels)})")
for r in dup_labels:
    print(f"  ! \\label{{{r}}} defined more than once")

hdr(f"CITES — missing from bib ({len(missing_cites)})")
for c in missing_cites:
    print(f"  ! \\cite{{{c}}} not in references_master.bib")

hdr(f"CITES — bib entries unused ({len(unused_bib)})")
print(f"  (showing first 15)")
for c in unused_bib[:15]:
    print(f"  - {c}")
if len(unused_bib) > 15:
    print(f"  ... and {len(unused_bib) - 15} more")

hdr(f"FIGURES — missing on disk ({len(fig_missing)})")
for f in fig_missing:
    print(f"  ! \\includegraphics{{{f}}} → no file in figures/ or results/figures/")

hdr(f"FIGURES — found ({len(fig_found)})")
for f, p in fig_found:
    print(f"  ✓ {f}  →  {p}")

hdr(f"ENV BALANCE — mismatched ({len(imbalance)})")
for env, b, e in imbalance:
    print(f"  ! \\begin{{{env}}} = {b}, \\end{{{env}}} = {e}")

hdr("STRUCTURE — section tree")
for lvl, name in sections:
    indent = "  " * (lvl - 1)
    bullet = ["§", "•", "◦"][lvl - 1]
    print(f"  {indent}{bullet} {name}")

hdr("VOLUME")
print(f"  Word count (body, ex equations/tables/figures): {n_words}")
print(f"  Rough page estimate @ 280 wpp: ~{page_est} pages")
print(f"  Figures: {len(fig_refs)}")
print(f"  Tables (\\begin{{table}} + \\begin{{table*}}): "
      f"{Counter(begins).get('table', 0) + Counter(begins).get('table*', 0)}")
print(f"  Equations (\\begin{{equation}} + display $$): "
      f"{Counter(begins).get('equation', 0)}")
print(f"  Algorithms: {Counter(begins).get('algorithm', 0)}")
print(f"  Sections: {sum(1 for l,_ in sections if l == 1)}")
print(f"  Subsections: {sum(1 for l,_ in sections if l == 2)}")
