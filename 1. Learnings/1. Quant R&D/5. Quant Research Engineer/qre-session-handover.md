# Session Handover — Quant Research Engineer Course

**Created**: 2026-10-14 · **Restructured**: 2026-11-13 (PO)
Entry point for any new Claude session teaching this course. Read fully before responding.

## 1. What This Program Is

A judgment course run in parallel with KCMME startup work (cost-down, fund-raising).
Goal: think and judge like a Quant Research Engineer — understand every concept, its impact
on money, and how it works behind the scene — so every AI plan and result on KCMME can be
judged. Execution is offloaded to AI while learning. The **Job-Ready Build Track** (last
tier) codes every QRE + Market Making concept and makes the learner industry job-ready.

Roadmap shape (PO 2026-11-13, after a Fable 5.1 relevance review): traditional order by
prerequisite (Foundation → Intermediate → Lifetime → Build Track); relevance from examples
(current business problem → future stages → past); a level needed early is taught in a
separate session on request and marked ✅. Topics moved to Market Making went only into its
upcoming levels (16, 19, new 21); MM next = Level 14.

Why restructured (2026-11-13): the Market Making course (theory-first, Claude runs the
engine check, learner judges) moved ~1 level/week. The first QRE design (learner computes
in Excel/Python, term drills, interview drills) stalled Level 2 for 3 weeks on syntax.

Sister program: Market Making (`../../5. Market Making/`, Levels 0–20) = domain pillar.
This course = statistics, research method, engineering judgment, business of research.
Cross-link, never duplicate.

## 2. Files

| Purpose | File |
|---|---|
| Roadmap + progress table | `learning-roadmap/qre-roadmap.md` |
| Teaching contract (6 steps) | `learning-template/qre-topic-template.md` (inherits the MM template's HARD rules) |
| Taught content | `quant-research-engineer.md` |
| Proof-of-skill entries | `qre-career-portfolio.md` |
| Engine gaps | KCMME `docs/architecture/gaps/engine-gaps.md` (on `fugu-dev`) |
| Delivery-workflow gaps | KCMME `docs/architecture/gaps/delivery-workflow-gaps.md` (on `fugu-dev`) |

## 3. Non-Negotiables

- Read BOTH templates (this course's + `../../5. Market Making/learning-template/topic-template.md`).
- 6 steps: terms → teaching → clear? + your call → KCMME example (Claude computes) + your
  call → gap check (engine + workflow, learner judges) → doc. Never self-advance.
- Low friction: a level ≈ 4–6 messages; the learner never computes or types code; a "your
  call" answer is one line; no stacked homework.
- Every concept impact-driven: the money decision it changes → idea → worked numbers →
  impact / desk practice → "ask the AI" questions.
- Non-quant accessibility: every symbol glossed every time; every math word explained.
- Plain-text formulas, never LaTeX. Sign convention: + = earned, − = lost.

## 4. Next Step (updated 2026-11-13)

Level 0 ✅, Level 1 ✅. Gaps on KCMME `fugu-dev`: delivery WG0.1–WG0.8 + WG1.1–WG1.3
(briefs = Appendix C + D), engine QRE-L1-G1/G2. Current engine = `spine`
(`~/dev/kcmme-spine`; state in KCMME master `docs/stripdown/README.md`).

**Level 2 (Signal vs Noise)** — Steps 1–3 done. Under the old format the learner already
worked, on the tiny list [−1, 1, −2, 0, 3]: mean 0.2, median 0, σ 1.92, variance 3.7,
SE 0.86 (n=5) → 0.39 (n=20, √n rule), 95% CI includes zero, fills needed > (2σ ÷ effect)²
≈ 312, EV = P(bad)×avg(bad) + P(good)×avg(good) = mean. Open from old Drill 6: the spine
adverse number −mean(min(0, drift)) equals the P(bad)×avg(bad) part of EV.
NEXT (new format): short teaching of the remaining ideas — fat tails / median vs mean,
Bayes for adverse selection, clustered fills (autocorrelation) — then Step 4 KCMME example:
Claude computes on `2. Practice/3. QRE Exercises/level-2-statistics/xrp_spine_fills.csv`
(XRP spine mainnet 26 Oct, 228 rows; passive bids 109, passive asks 5) how much the spine's
20-fill AdverseMeter estimate wobbles vs the fills needed, and the ask-side cold start;
one "your call" question. Then Step 5 gap check (start with the adoption check on
WG0.x/WG1.x), Step 6 doc + commit. Then Level 3 (Cheap, Decisive Experiments).
