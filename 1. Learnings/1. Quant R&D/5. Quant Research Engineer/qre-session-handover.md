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

Sister program: Market Making (`../../5. Market Making/`, Levels 0–21) = domain pillar.
This course = statistics, research method, engineering judgment, business of research.
Cross-link, never duplicate.

## 2. Files

| Purpose | File |
|---|---|
| Roadmap + progress table | `learning-roadmap/qre-roadmap.md` |
| Teaching contract (6 steps) | `learning-template/qre-topic-template.md` (inherits the MM template's HARD rules) |
| Taught content | `quant-research-engineer.md` |
| Proof-of-skill entries | `qre-career-portfolio.md` |
| Gap index (all gaps, both courses) | KCMME `docs/architecture/gaps/GAPS-INDEX.md` (branch `learning/gaps`) |
| Engine gaps | KCMME `docs/architecture/gaps/engine-gaps.md` (branch `learning/gaps`) |
| Delivery-workflow gaps | KCMME `docs/architecture/gaps/delivery-workflow-gaps.md` (branch `learning/gaps`) |

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

## 4. Next Step (updated 2026-11-15)

Level 0 ✅, Level 1 ✅, **Level 2 ✅ 2026-11-15**. Gaps on KCMME branch `learning/gaps` (index `GAPS-INDEX.md`; fugu-dev copy frozen at `165f7d89c`):
delivery WG0.1–WG0.8, WG1.1–WG1.3, WG2.1–WG2.2 (briefs = Appendix C, D, E — all still
unsent; the PO runs one Workflow-architect session for them); engine QRE-L1-G1/G2,
QRE-L2-G1/G2. Current engine = `spine` (`~/dev/kcmme-spine`; state in KCMME master
`docs/stripdown/README.md`); live research = HTX sessions (`docs/htx/reports/` on
`docs/htx-integration-research`, esp. report 09 tracker) — use it for current-problem examples.

How Level 2 went (for pacing): the learner asked to learn A/B design BEFORE judging results;
it worked best as one question at a time with real HTX numbers, correcting until right,
re-explaining with a toy-number example when stuck (race/wind analogy for random order,
tea-stall for Case A/B). Define every case label and every bar in words before asking.
Learner habit to reinforce: name the ingredient number AND the fix, not only the flaw.

NEXT: **Level 3 (Cheap, Decisive Experiments)** — start with Step 5 rule 9 adoption check
(WG0.x–WG2.x routed? used?), then Step 1 terms. A/B design foundations are already taught
(roadmap Level 3 note): recap in one line, then teach the cost ladder, minimum detectable
effect / power, the many-tests trap, confounders, ablation; KCMME example = grade the HTX
pre-registered agenda (report 08) and tracker 09 verdicts (which tests could decide).
Free video companions (learner watches on their own): StatQuest (stats), Udacity "A/B
Testing" by Google, Quantopian lectures, López de Prado talks, Carl Cook CppCon 2017,
Jane Street "Signals and Threads".
