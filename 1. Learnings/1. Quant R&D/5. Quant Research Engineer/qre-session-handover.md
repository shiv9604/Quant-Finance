# Session Handover — Quant Research Engineer Course

**Created**: 2026-10-14
Entry point for any new Claude session teaching this course. Read fully before responding.

## 1. What This Program Is

A job-readiness course run in parallel with KCMME startup work. Two goals every level:
1. **Industry-ready**: reach the Junior → Mid → Senior bar of a Quant Developer / Quant
   Research Engineer at a market-making firm — contribute to their MM engine day one.
2. **KCMME judgment**: be able to understand AI plans at full granularity and judge
   whether what the AI built is right (the root problem that started this course:
   the delivery loop is the same as the PO's frontend job, but judgment of
   "correct" in quant needs statistics + domain + engine knowledge).

Sister program: Market Making (`../../5. Market Making/`, Levels 0–20) = domain pillar.
This course = statistics, research method, engineering, career pillars. Cross-link,
never duplicate.

## 2. Files

| Purpose | File |
|---|---|
| Roadmap + progress table | `learning-roadmap/qre-roadmap.md` |
| Teaching contract (7 steps) | `learning-template/qre-topic-template.md` (inherits the MM template's HARD rules) |
| Taught content | `quant-research-engineer.md` |
| Proof-of-skill entries | `qre-career-portfolio.md` |
| Engine gaps found | KCMME repo `docs/architecture/gaps/engine-gaps.md` |

## 3. Non-Negotiables

- Read BOTH templates (this course's + `../../5. Market Making/learning-template/topic-template.md`) before teaching.
- 7-step sequence; never pre-write content before teaching; never self-advance.
- Step 4 (KCMME exercise) is done BY THE LEARNER — Claude guides and reviews only.
- Non-quant accessibility rule: every symbol glossed every time; every math word explained.
- Learner style: repetition across contexts with new concrete numbers each time; concise.

## 4. Next Step (updated 2026-10-23)

Level 0 ✅. Level 1 (P&L Attribution & Markouts): Steps 1–3 DONE (14 terms clear; teaching
confirmed). NOW: Step 4 hands-on, guided step by step (wait for "Done" between steps).
Exercise folder: `~/Desktop/trading/2. Practice/3. QRE Exercises/level-1-attribution/`
(SOL session 7 Oct 2026 06:44–07:00; 73 engine fills). Part A steps 1–4 done (learner
built per-fill spread / adverse-5s / fee / total columns M–P, chose mid column J = (bid+ask)/2
— column K equals the fill price on buys). NEXT: Part A Step 5 — SUM totals (row 76) +
SUMIF maker/taker split (rows 77–78) + COUNTIF takers; learner reports + reads biggest bar.
Then Part B (vs `sol_engine_computed.csv` — expect engine spread≈0 on buys from K),
Part C (vs exchange `sol_exchange_truth.xlsx` User Trades), Steps 5–8.
Learner computes all answers — Claude does NOT pre-compute totals (PO rejected it 2026-10-21).
Sign convention: + = earned, − = lost; say "net result".
