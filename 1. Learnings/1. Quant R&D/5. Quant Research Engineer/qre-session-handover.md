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

Level 0 ✅, Level 1 ✅ (all 8 steps). Gaps on KCMME `fugu-dev`: delivery WG0.1–WG0.8 +
WG1.1–WG1.3 (`docs/architecture/gaps/delivery-workflow-gaps.md`, briefs = Appendix C + D),
engine QRE-L1-G1/G2 (`engine-gaps.md`). Adoption check 2026-10-23: WG0.x not yet picked up
by a Workflow-architect session.
Current engine = `spine` branch (`~/dev/kcmme-spine`) — see template Current-Engine Rule.
Level 2: Steps 1–3 done. Step 4 IN PROGRESS (Python): data `2. Practice/3. QRE Exercises/level-2-statistics/xrp_spine_fills.csv` (XRP spine mainnet 26 Oct, 228 fills; passive bids 109, passive asks 5 — ask meter below its 20-fill window). Learner counted fills via Excel filters; switched to Python at Step P1 (venv + jupyterlab setup). NEXT: Step 4a term drill (Python): tiny list [−1, +1, −2, 0, +3] then XRP data — mean, median, σ, variance, SE, √n, CI, excludes-zero, EV, conditional probability, autocorrelation; THEN Step 4b: load CSV in pandas → passive bids → loss = max(0, −drift) → spine estimate on 20-fill blocks → σ, SE = σ ÷ √20, CI → fills needed → ask-side implication. Before teaching: Step 7.9
adoption check on WG0.x/WG1.x. Then Step 1 terminology check.
Learner style notes (Level 1): guide spreadsheet work ONE small step per message, wait for
"Done"; give algebra first, then the Excel mapping; never pre-compute the learner's answers;
learner works in PYTHON (pandas + JupyterLab in ~/qre-venv) from Level 2 Step 4 on — template Python-First Exercise Rule; Excel used only in Level 1. NEVER use LaTeX ($$…$$, \frac) — the terminal shows it raw; write formulas as plain text (SE = σ ÷ √n) in code blocks. Sign convention + = earned, − = lost.
