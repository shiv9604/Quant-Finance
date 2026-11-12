# Learning Topic Template — Quant Research Engineer Course

This course **inherits the Market Making learning contract**:
`~/Desktop/trading/1. Learnings/5. Market Making/learning-template/topic-template.md`

Every HARD rule there binds here unchanged — Terminology Check, Non-Quant Accessibility
(every symbol glossed every time, every math word explained at first use), Re-anchoring
(level numbers are never an explanation), Teaching Flow Rules (naive-fails first → layer
by layer with "what this still misses" → why each formula is built that way → concrete
numbers → "why should I believe this?" → Sees vs Misses), Progression Rule (never
self-advance), Flip Rule (where a level has a defensive/offensive pair).

Goal of the course (restructured 2026-11-13, PO): think and judge like a **Quant Research
Engineer** — understand every concept, its impact on money, and how it works behind the
scene — so every AI-written plan and result on KCMME can be judged. Execution is offloaded
to AI while learning. Coding every concept (QRE + Market Making) is the LAST tier of the
roadmap (Job-Ready Build Track), which then makes the learner industry job-ready.

Why this shape: the Market Making course (theory-first, Claude does the engine check, the
learner judges) moved ~1 level/week with deep, lasting understanding. The first QRE design
(learner computes everything in Excel/Python, term drills, interview drills) stalled one
level for 3 weeks on syntax instead of ideas. Understanding first; hands second.

---

## Step Sequencing Rule (HARD — the MM 5-step contract + one gap step)

```
Step 1 — Terminology check     List the level's terms, each explained simply with its
                               impact in one line. Wait for "clear".
Step 2 — Teaching              Impact-Driven Teaching Rule below + MM Teaching Flow Rules.
Step 3 — Understanding check   Explicit "is this clear, or does any part need more depth?"
                               plus ONE "your call" question (a one-line prediction or
                               decision on a scenario). Learner answers; Claude grades.
Step 4 — KCMME example         CLAUDE does the work: reads the spine engine / runs the
                               numbers on real KCMME data, and shows it as a worked
                               example — what the concept says, what the engine does,
                               the impact in money / cost per $1k / fills. Ends with ONE
                               "your call" question the learner answers (spot the flaw,
                               predict the impact, or pick the decision).
Step 5 — Gap check             (value-delivery layer — never skipped)
                               a) Engine gaps → KCMME docs/architecture/gaps/engine-gaps.md
                               b) Delivery-workflow cross-check → delivery-workflow-gaps.md
                                  (Delivery-Workflow Cross-Check Rule below)
                               Claude gathers the evidence and presents gaps inline; the
                               learner judges each (agree / disagree / adjust).
Step 6 — Doc update            Write the level into quant-research-engineer.md (Foundation
                               entry + full-depth section), a short entry into
                               qre-career-portfolio.md, learner-confirmed gaps into the
                               two gap files. Commit + push the trading repo; KCMME gap
                               files go to `fugu-dev` (PO directive 2026-10-21).
```

Steps 4–6 are FORBIDDEN before Step 3 confirmation. Step 6 is FORBIDDEN before Step 5 is
judged. A level is ✅ only when all 6 steps are done.

## Low-Friction Pace Rule (HARD — added 2026-11-13, PO)

- A level takes **about 4–6 messages**, not dozens: terms → teaching (one or two rich
  messages) → clear? + your call → KCMME example + your call → gaps → doc.
- **The learner never computes, types code, or builds spreadsheets.** Claude computes;
  the learner predicts, judges and decides. A "your call" answer is one line.
- Never "one tiny step per message, wait for Done". Never stack outstanding homework.
- If the learner is stuck on one concept, give a second example with new numbers — do not
  add drills. Depth comes from the concept returning in later levels (MM Repetition Rule).

## Impact-Driven Teaching Rule (HARD — added 2026-11-13, PO)

Every concept is taught in this order:
1. **The money decision it changes** — one line: "this decides whether we …". If a concept
   changes no decision, it does not get taught.
2. **The idea** in plain words; plain-text formula only if it is the clearest form.
3. **Worked example** with concrete numbers (KCMME numbers when they exist).
4. **Impact** — what goes wrong, in money or cost per $1k, when it is ignored; and what a
   desk does instead (Jane Street / Optiver / Citadel Securities / Wintermute).
5. **Ask the AI** — the 1–3 questions this concept lets the learner put to any AI plan.

## Plain-Text Formula Rule (HARD — added 2026-10-28, PO)

The learner reads in a terminal: NEVER write LaTeX (`$$…$$`, `\frac`, `\sqrt`, `\text`). Write
formulas as plain text in code blocks (`SE = σ ÷ √n`), then the same formula in words, then a
worked number. Money sign convention: + = earned, − = lost.

## Current-Engine Rule (added 2026-10-24, PO directive)

The live engine is the **strip-down `spine` branch** (worktree `~/dev/kcmme-spine`), cut from
`fugu-dev`. Strip-down state: `docs/stripdown/README.md` on KCMME master.
- **Step 4 (KCMME example) and engine gaps** read the `spine` branch first — that is what
  runs now. Older `fugu-dev` code is history: cite it only to show where a gap came from.
- **Step 5b (workflow cross-check)** uses BOTH: feature history (M0–M10 on `fugu-dev`) for
  counterfactuals, and how the spine work is being delivered now for live gaps.
- Read `spine` with `git -C ~/dev/kcmme-spine` or `git show spine:<path>`; never edit it.
- Claude may extract raw logs to CSV/notebooks for the example; data files stay local
  (gitignored), never committed.

## Delivery-Workflow Cross-Check Rule (HARD — Step 5b, added 2026-10-18 PO directive)

Every level teaches how a professional desk does something. Step 5b asks: **does our AI
delivery workflow do it, did past features do it, and what did not doing it cost?**

1. **Current workflow** — read the canonical process, not memory of it:
   `docs/product/features/feature-lifecycle.md`, the contract template / `contract_check.py`,
   the relevant `.ai/roles/*.md`. Cite file:line for what exists.
2. **Feature history** — check past features (contracts, timelines, A/B / closure reports in
   `docs/product/features/M<n>/`, `features.md` close lines). Cite file:line or a number.
   Include features that did it well, not only failures.
3. **Gap entry** — only where the professional practice is missing or partial. Credit what
   the workflow already does at professional standard (a "Matches standard" line per level).
4. **Counterfactual** — for each gap: "if this had existed, what would have changed in
   feature M<n>?" Label every counterfactual **Evidenced** (the record shows the exact moment
   it would have bitten) or **Plausible** (reasoned, not provable). Never present Plausible
   as Evidenced.
5. **Proposal, not change** — each gap carries a proposed workflow change, but the learning
   session NEVER edits the workflow. Changes route to a Workflow-architect session
   (router option 4), PO-gated.
6. **Learner judges** — present gaps inline first; the learner agrees / disagrees / adjusts
   each before anything is written (Step 6).
7. **Direction check against the target delivery flow** — `delivery-workflow-gaps.md`
   Appendix B holds the CUMULATIVE target end-to-end feature delivery flow (research note →
   research review → contract → plan → build → reproduction → concurrent A/B → attribution →
   economic verdict / scale-or-kill → graded note). Each level: (a) EXTEND that flow with
   whatever this level teaches (a new stage, gate, artifact or field); (b) walk the live
   workflow stage by stage against it; (c) wherever the workflow is not moving in that
   direction — a stage missing, a stage that exists but proves the wrong thing, an artifact
   with no template — DECLARE it a gap (WG<N>.<k>) and record it. A missing ARTIFACT or
   TEMPLATE the level relies on (e.g. Level 0: the research note) is always its own gap,
   with a draft template in an appendix.
8. **Workflow-architect handoff brief** — every level whose gaps are confirmed ends with a
   paste-ready brief (Appendix C pattern) for a Workflow-architect session: Task (gap IDs) ·
   Scope (artifacts, lifecycle sections, gates, role contracts) · Constraints (never weaken
   SAFETY.md, never touch engine code, lean / extend existing checkers, bar-freeze: in-flight
   features keep frozen contracts) · Acceptance (an end-to-end dry-run feature through the new
   flow + the existing E2E regression suite green) · Flow (plan → PO review → implement on
   `workflow-improvements` → self-test + E2E → PO tests → merge to `fugu-dev` → gaps marked
   RESOLVED).
9. **Adoption check (next level start)** — before teaching a new level, check every
   previously ROUTED gap: merged? RESOLVED? and — the implementation-theater test applied to
   the workflow itself — was the new stage actually USED by the next feature that went
   through it (artifact exists, gate fired)? A merged-but-unused stage is re-opened as a gap.

Gap entry format (in `delivery-workflow-gaps.md`, one `## Level N` section per level):

```
### WG<N>.<k>: <gap name>
- Professional standard: <what desks do — one line>
- Current workflow: <what exists, file:line> → MISSING | PARTIAL
- Feature history evidence: <M<n>: file:line / number>
- Counterfactual (Evidenced | Plausible): <what would have changed>
- Proposed change: <smallest workflow change that closes it>
- Verdict: Likely issue | Investigate | Low priority
- Status: OPEN | ROUTED-TO-WORKFLOW-ARCHITECT <date> | RESOLVED <date> <one line> | ADOPTED <feature> | RE-OPENED <date> (merged but unused)
```

Engine gap entries (`engine-gaps.md`, section `## QRE Level N`) follow that file's existing
format: `### QRE-L<N>-G<k>: <name>` with evidence (file:line on `spine`), impact, verdict.

## Separation Rule (extends the MM one)

| File | Contains | Never contains |
|---|---|---|
| `quant-research-engineer.md` | Pure concepts + impact + industry practice | KCMME specifics |
| `qre-career-portfolio.md` | One entry per level: what was found/judged on KCMME, the result, how to tell it | Teaching content |
| KCMME `engine-gaps.md` | Engine gaps found in Step 5a | Teaching content |
| KCMME `delivery-workflow-gaps.md` (same folder) | Delivery-process gaps found in Step 5b + feature-history counterfactuals | Engine gaps, teaching content |
| `market-making.md` | MM domain (Levels 0–20) — this course cross-links, never duplicates | QRE content |

---

# [Level N — Topic Name] — Learning

## 1. What It Is — and the money decision it changes
Plain language. Why a quant research engineer at a MM firm needs it. What breaks if wrong.

## 2. Simple Example
Concrete numbers. Works-correctly case and failure case.

## 3. Why the Naive Approach Fails
What a software engineer new to quant would do, and where it breaks.

## 4. How It Works (Simple → Sophisticated)
Basic → Intermediate → Professional. "What this still misses" at the end of each.

## 5. Why Should You Believe This?
An end-to-end scenario that makes it felt, not just understood.

## 6. Impact & Professional Standard
What it costs when ignored (money / cost per $1k); what Jane Street / Optiver / Citadel
Securities / Wintermute do; who owns it on a desk and what artifact it produces.

## 7. Summary + Sees vs Misses
Summary table (what / why / professional standard) + Method | Sees | Misses table.

## 8. Ask the AI — Judgment Checklist
The questions the learner must now ask of ANY AI plan or result touching this topic.
Example shape: "Did the plan state the expected effect as a number before running?"
"Is the sample big enough for that effect to beat noise?"

## Notes & Open Questions
