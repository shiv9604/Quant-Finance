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
Step 4 — Hands-on KCMME exercise  THE LEARNER DOES IT, not Claude.
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
