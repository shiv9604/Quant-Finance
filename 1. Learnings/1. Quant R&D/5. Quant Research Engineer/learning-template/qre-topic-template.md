# Learning Topic Template — Quant Research Engineer Course

This course **inherits the Market Making learning contract in full**:
`~/Desktop/trading/1. Learnings/5. Market Making/learning-template/topic-template.md`

Every HARD rule there binds here unchanged — Terminology Check, Non-Quant Accessibility
(every symbol glossed every time, every math word explained at first use), Re-anchoring
(level numbers are never an explanation), Teaching Flow Rules (naive-fails first → layer
by layer with "what this still misses" → why each formula is built that way → concrete
numbers → "why should I believe this?" → Sees vs Misses), Progression Rule (never
self-advance), Flip Rule (where a level has a defensive/offensive pair).

This file only adds what is DIFFERENT for this course: the job-readiness layer.

Goal of the course: become an industry-ready **Quant Developer / Quant Research Engineer**
for a market-making desk — able to contribute to a firm's MM engine from day one — AND,
as the same skill, able to judge every AI-written plan and result on KCMME.

---

## Step Sequencing Rule (HARD — extends the MM 5-step contract to 7 steps)

```
Step 1 — Terminology check        (unchanged from MM template)
Step 2 — Teaching                 (unchanged; Teaching Flow Rules apply)
Step 3 — Understanding check      (unchanged; explicit "is this clear?")
Step 4a — Term drill (Python)     Before any analysis: compute EVERY term of the level
                                  from data — first on a tiny hand-checkable list
                                  (learner verifies by hand), then on the level's
                                  real KCMME data. One term per step: algebra →
                                  Python line → meaning → hand check. Added
                                  2026-10-28 (PO): terms are recalled by using them.
Step 4b — Hands-on KCMME exercise THE LEARNER DOES IT, not Claude.
                                  Claude gives the task, data location and the
                                  expected-shape of the answer; the learner runs it
                                  (notebook / script / code reading) and reports.
                                  Claude reviews like a senior reviewing a junior.
Step 5 — Job-readiness check      Interview drill (3 questions: concept, numeric,
                                  scenario). Learner answers first; Claude grades
                                  against the Junior / Mid / Senior bar and states
                                  which bar the answer met.
Step 6 — LLM-judgment check       Claude shows a deliberately flawed AI plan or result
                                  on this level's topic; the learner must find the
                                  flaw(s). This is the direct fix for "I can't judge
                                  what the AI built".
Step 7 — Doc update               Only now: write the level into
                                  quant-research-engineer.md, the exercise artifact
                                  into qre-career-portfolio.md, any engine gaps into
                                  KCMME docs/architecture/gaps/engine-gaps.md.
                                  Commit + push the trading repo.
```

Steps 4–7 are FORBIDDEN before Step 3 confirmation. Step 7 is FORBIDDEN before Steps 5
and 6 are done. A level is ✅ only when all 7 steps are done.

Why Step 4 is learner-hands-on: the course goal is skill, not output. If Claude runs the
analysis, the learner gains a result and loses the skill — the exact failure mode this
course exists to fix.

---

## Plain-Text Formula Rule (HARD — added 2026-10-28, PO)

The learner reads in a terminal: NEVER write LaTeX (`$$…$$`, `\frac`, `\sqrt`, `\text`). Write
formulas as plain text in code blocks (`SE = σ ÷ √n`), then the same formula in words, then a
worked number.

## Python-First Exercise Rule (HARD — added 2026-10-28, PO directive)

All hands-on work (Step 4 exercises, any data check) is done in **Python** — pandas in a
JupyterLab notebook — never in Excel/Sheets. Reason: the course targets a Quant Developer /
Research Engineer role, where analysis is done in Python; spreadsheet skill does not transfer.
- **Environment:** `~/qre-venv` (`source ~/qre-venv/bin/activate`; packages: pandas,
  jupyterlab — add numpy/matplotlib when a level needs them). One notebook per exercise,
  saved in that level's exercise folder (`2. Practice/3. QRE Exercises/level-N-…/`).
- **Teaching order per step:** algebra (plain text) → the Python line(s) → what each part of
  the line means, word by word → the expected result to check against. One small step per
  message; wait for "Done".
- **The learner types and runs the code.** Claude explains, reviews and debugs pasted
  errors — never runs the analysis for the learner (same rule as Step 4).
- Python skill is built INSIDE each level's exercise; Level 4 (Python research stack) then
  consolidates and deepens it instead of introducing it.
- Data prep exception: Claude may extract raw logs (lz4/jsonl) to a plain CSV for the
  exercise — that is plumbing, not the skill. No computed answer columns in the CSV.

## Current-Engine Rule (added 2026-10-24, PO directive)

The live engine is the **strip-down `spine` branch** (worktree `~/dev/kcmme-spine`; sibling
`spine-ab-formula`), cut from `fugu-dev`: `src/strategy/spine.cpp` (~300-line strategy),
`docs/architecture/spine-parameters.md`, plan `docs/architecture/simple-robust-mm-engine-plan-20261020.md`.
- **Step 4 (KCMME exercise) and engine gaps** read the `spine` branch first — that is what
  runs now. Older `fugu-dev` code is history: cite it only to show where a gap came from.
- **Step 7 (workflow cross-check)** uses BOTH: feature history (M0–M10 on `fugu-dev`) for
  counterfactuals, and how the spine work is being delivered now for live gaps.
- Read `spine` with `git -C ~/dev/kcmme-spine` or `git show spine:<path>`; never edit it.

## Separation Rule (extends the MM one)

| File | Contains | Never contains |
|---|---|---|
| `quant-research-engineer.md` | Pure concepts + industry practice + seniority bar | KCMME specifics |
| `qre-career-portfolio.md` | One proof-of-skill entry per level: what was built/analysed on KCMME, the result, how to tell it in an interview | Teaching content |
| KCMME `engine-gaps.md` | Engine gaps found in Step 4 | Teaching content |
| `market-making.md` | MM domain (Levels 0–20) — this course cross-links, never duplicates | QRE content |

---

# [Level N — Topic Name] — Learning

*(Sections 1–7 = same as the MM template. Sections 8–11 = job-readiness layer, new.)*

## 1. What It Is
Plain language. Why a quant developer at a MM firm needs it. What breaks if wrong.

## 2. Simple Example
Concrete numbers. Works-correctly case and failure case.

## 3. Why the Naive Approach Fails
What a software engineer new to quant would do, and where it breaks.

## 4. How It Works (Simple → Sophisticated)
Basic → Intermediate → Professional. "What this still misses" at the end of each.

## 5. Why Should You Believe This?
An end-to-end scenario that makes it felt, not just understood.

## 6. Professional Standard (Jane Street / Optiver / Citadel Securities / Wintermute)
Inputs, tools, cadence, what their version does that a typical one doesn't.

## 7. Summary + Sees vs Misses
Summary table (what / why / professional standard) + Method | Sees | Misses table.

## 8. Industry Practice — How a Desk Does This Manually
- Which role owns it (Quant Trader / Quant Researcher / Quant Developer / Core C++ Eng).
- The ritual: when it happens (pre-trade research, daily review, post-incident…),
  what artifact it produces (research note, dashboard, review comment, postmortem),
  who signs off.
- The standard tooling (e.g. Python/pandas/Jupyter, kdb+/q, ClickHouse, Grafana,
  internal sim, C++/Rust).

## 9. Job-Readiness by Seniority

| Bar | Can do (observable behaviour) | Day-one contribution at a MM firm |
|---|---|---|
| **Junior** | executes with guidance | … |
| **Mid** | owns it end to end | … |
| **Senior** | sets the standard, reviews others, decides | … |

## 10. Interview Drill
3 questions — **Concept** (explain X), **Numeric** (compute Y), **Scenario** (what do you
do when Z) — each with the answer that meets the Junior / Mid / Senior bar.

## 11. LLM-Judgment Checklist
The questions the learner must now ask of ANY AI plan or result touching this topic.
Example shape: "Did the plan state the expected effect as a number before running?"
"Is the sample big enough for that effect to beat noise?"

## Notes & Open Questions
