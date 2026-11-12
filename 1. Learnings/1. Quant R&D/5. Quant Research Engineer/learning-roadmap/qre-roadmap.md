# Quant Research Engineer — Learning Roadmap

Goal: think and judge like a **Quant Research Engineer** on a market-making desk —
understand every concept, its impact on money, and how it works behind the scene — so
every AI-written plan and result on KCMME can be judged (plan granularity + "is this
right?"). Execution is offloaded to AI while learning; the **Job-Ready Build Track** at the
very end codes every concept from this course AND the Market Making course, which makes
the learner industry job-ready.

Restructured 2026-11-13 (PO) to the shape that worked in the Market Making course:
theory-first, impact-driven, Claude runs the KCMME example, the learner judges.
Teaching format: `learning-template/qre-topic-template.md` (6-step contract).

Ordering principle: **by impact on money decisions, not by textbook order.** Depth grows
in passes, like Market Making: a light Foundation read → full-depth Levels → the Build
Track where each concept is coded.

Role this course targets (how a MM desk splits the work you currently do alone):

| Desk role | Owns | KCMME equivalent |
|---|---|---|
| Quant Trader | live behaviour, params, daily P&L judgement | you as PO watching runs |
| Quant Researcher | hypothesis, model, statistical proof | feature planning + "is it right?" |
| **Quant Developer / Research Engineer** ← target | research → production, sim/backtest infra, data pipelines, proving code matches research | what the LLM implements + your review |
| Core C++ / Trading Systems Eng | gateways, hot path, latency | engine core, venue adapters |

Domain pillar (market microstructure) lives in `5. Market Making/market-making.md`
Levels 0–20. This course covers the OTHER pillars (statistics, research method,
engineering judgment, business of research) and cross-links into MM levels — never
duplicates them.

---

## Progress

| Tier | Level | Topic | Decision it unlocks | Status |
|---|---|---|---|---|
| Foundation | 0 | How a MM desk works — the research → production loop | who must judge what, before money is risked | ✅ 2026-10-21 |
| Foundation | 1 | P&L attribution & markouts | where the money actually went | ✅ 2026-10-23 |
| Foundation | 2 | Signal vs noise — statistics for noisy outcomes | is this result real or luck? | 🟡 in progress |
| Foundation | 3 | Cheap, decisive experiments | how to test an idea for the least money and time | ⬜ |
| Foundation | 4 | Metrics that decide money — unit economics of research | which number to optimise (cost per $1k, volume, rebate) | ⬜ |
| Foundation | 5 | Data you can trust — market data, clocks, logs vs exchange truth | can this number be believed at all? | ⬜ |
| Foundation | 6 | Reading an engine — system map, tracing a parameter, implementation theater | does the code actually do what the plan says? | ⬜ |
| Intermediate | 7 | Backtesting & simulation — when to trust a replay | can this sim result be shipped on? | ⬜ |
| Intermediate | 8 | Overfitting & robust validation | is this tuned "win" going to survive live? | ⬜ |
| Intermediate | 9 | Signals & time series | does this signal really predict, out of sample? | ⬜ |
| Intermediate | 10 | Research notes & research review | is this plan worth building? | ⬜ |
| Intermediate | 11 | Production risk controls & operations | what stops a bad day becoming the last day? | ⬜ |
| Lifetime | 12 | Optimal market-making models (the theory behind quoting) | is our quoting rule principled or ad hoc? | ⬜ |
| Lifetime | 13 | Machine learning for microstructure | when does ML pay, and when is it theater? | ⬜ |
| Lifetime | 14 | Latency & infrastructure economics | when does speed earn more than it costs? | ⬜ |
| Lifetime | 15 | Portfolio, risk & capital allocation | how much capital to which coin / venue? | ⬜ |
| Lifetime | 16 | Leading research — agenda, prioritisation, founder lens | what to research next, and what to stop | ⬜ |
| Build Track | B1–B6 | Job-Ready Build Track — code every QRE + MM concept | industry job-ready | ⬜ (last) |

Every level below lists: **Why (impact)** · concepts · **KCMME example** (Claude runs it,
the learner judges) · **Ask the AI** · **Gap hunt** (where to look for engine and
workflow gaps) · cross-links.

---

# FOUNDATION — "I can tell whether a plan or result is right"

## Level 0 — How a MM Desk Works: the Research → Production Loop ✅

**Why (impact)**: names the loop you run alone, shows which steps need human judgment
(research note, research review, daily attribution) and why an LLM cannot supply judgment
nobody in the loop has. Every later level slots into this loop.

- The four roles (QT / QR / QD / Core Eng) and how they hand work to each other
- The loop: research note → research review → implementation → sim/backtest
  reproduction → small-size live (often A/B) → daily attribution → scale or kill
- What a research note contains: hypothesis, mechanism, predicted effect as a number,
  evidence, kill criteria
- Where judgment lives in the loop vs where execution lives

**Ask the AI**: "Which step of the loop is this output, and who should have reviewed it?"
**Cross-links**: MM Level 0 (Mental Model), Level 20 (Institutional Reality).

## Level 1 — P&L Attribution & Markouts ✅

**Why (impact: highest)**: the debugger of a trading system. Without it, "we lost money"
can't be traced to a cause, so no fix can be judged.

- Gross vs net; realised vs unrealised; mark-to-market
- The waterfall: spread capture + adverse selection + inventory − fees = net
- Markouts at several horizons; reading a markout curve
- Per-fill → per-asset → per-session; why averages hide tails
- Reconciliation: engine P&L vs exchange truth

**Ask the AI**: "Which waterfall bar is this change supposed to move, by how much, and did
that bar actually move?"
**Cross-links**: MM Level 3 (Maker Economics), Level 6 (Adverse Selection); Profitability L1, L12.

## Level 2 — Signal vs Noise: Statistics for Noisy Outcomes 🟡

**Why (impact)**: "is it right?" in quant mostly means "is the effect real or luck?". One
lucky session can ship a losing change; one unlucky one can kill a good one.

- Mean, median, spread of outcomes (σ, variance) — done
- Standard error and why it shrinks with √n (square root of the number of fills) — done
- Confidence intervals; "excludes zero"; fills needed = (2 × σ ÷ effect)² — done
- Expected value, split into P(bad) × avg(bad) + P(good) × avg(good) — done
- Fat tails and outliers: why one fill can flip a session; median vs mean
- Conditional probability & Bayes — the language of adverse selection
- Clustered fills (autocorrelation): why 100 fills can count as 30; correlation ≠ causation

**KCMME example**: the spine sets its adverse-selection cost from the last 20 passive fills
(`AdverseMeter`). Claude computes, on XRP spine fills, how much that 20-fill estimate
wobbles and how many fills a trustworthy estimate needs; the ask side (5 fills) shows the
cold-start problem.
**Ask the AI**: "How many fills is this based on? What's the range, not the point? How many
would we need for this effect?"
**Gap hunt**: any engine estimate or workflow verdict made from a sample too small for the
effect it claims.
**Cross-links**: MM Level 14 (Statistical Validation) — this level is its prerequisite.

## Level 3 — Cheap, Decisive Experiments

**Why (impact)**: the idea that drove the strip-down — test an idea for the least money and
time, and get an answer that actually decides. Turns runs from "see what happens" into
evidence; fixes "the result looked good but was an artifact" (GH#109).

- Hypothesis → predicted number → kill criteria, written BEFORE the run
- The cost ladder: thinking → existing data → replay → tiny live → full live
- Control, one change at a time; A/B, interleaving, paired comparisons on the same market
- Minimum detectable effect and power in plain words (links Level 2's fills-needed)
- Confounders: regime, asset, time of day, latency; three verdicts (pass / fail / continue)
- Ablation: proving which part of a change caused the effect

**KCMME example**: grade a past spine A/B (e.g. JT1) against a pre-registration written
after the fact: was it sized to detect the effect it claimed?
**Ask the AI**: "What's the control? What else changed? What result would have killed this?
Is there a cheaper rung of the ladder that answers it?"
**Gap hunt**: features shipped without a prediction-as-a-number or kill criteria.
**Cross-links**: MM Level 13 (Simulation), Profitability L13 (validation ladder).

## Level 4 — Metrics That Decide Money: Unit Economics of Research

**Why (impact)**: you optimise what you measure. Picking cost per $1k volume instead of
raw P&L changed the engine. A wrong north-star metric makes every later decision wrong.

- Normalising: per fill, per $1k volume, per hour, per unit of capital — and what each hides
- Decomposing a metric into levers (fees, rebates, adverse, inventory, volume)
- Leading vs lagging metrics; guardrail metrics that must not get worse
- Goodhart's law: when a metric becomes a target it stops measuring
- Rebate tiers and volume: when more volume is worth a worse per-$1k number

**KCMME example**: decompose current cost per $1k on the core basket into its levers and
show which lever the next feature should move.
**Ask the AI**: "Which metric does this plan move, what are the guardrails, and could it
improve the metric while losing money?"
**Gap hunt**: features verified on a metric that doesn't decide money.
**Cross-links**: MM Level 3 (Maker Economics), Level 19 (Business Economics).

## Level 5 — Data You Can Trust

**Why (impact)**: every model sits on data; bad data gives confident wrong answers
(Level 1: fills.jsonl missing taker exits made gross look 3× too kind).

- Feeds: L2 snapshots + diffs, trades, sequence numbers, gaps, resyncs
- Timestamps: exchange vs receive vs process time; clock sync; latency measurement
- Look-ahead: using data the engine didn't have yet
- Quality checks: crossed books, stale quotes, duplicate/missing messages
- Logs vs exchange truth: reconciliation as a standing habit

**KCMME example**: audit one spine session's logs against exchange trades and market data
for gaps and staleness.
**Ask the AI**: "Which clock is this? Is this log complete versus the exchange? Could the
signal see the future?"
**Gap hunt**: logs the engine writes that disagree with exchange truth.
**Cross-links**: MM Level 2 (LOB), Level 9 (Latency/Staleness).

## Level 6 — Reading an Engine: System Map & Implementation Theater

**Why (impact)**: closes "implementation theater" (code exists but its output is never
used). After this you can draw the spine from memory and trace any parameter to the
decision it changes — without writing C++.

- Canonical MM engine flow: market data → fair value → signals → quoting → risk checks →
  gateway → fills → position/P&L → hedging
- Invariants and where they're enforced (limits, kill switch, stop)
- Tracing a parameter end to end: config → load → consumer → decision → log
- Common trading-code bug classes in plain words: units (bps vs fraction), side sign,
  stale state, integer division — what to ask about in a diff
- Reviewing AI-written code at scale: diff → claims → evidence

**KCMME example**: Claude draws the spine data flow and traces 3 parameters to their
decision point; the learner spots any that are computed but never consumed.
**Ask the AI**: "Where is this new output CONSUMED? Show me the decision path."
**Gap hunt**: parameters or meters with no consumer; docs that disagree with code.
**Cross-links**: MM Level 10 (Execution Engineering).

---

# INTERMEDIATE — "I can judge research and its risks"

## Level 7 — Backtesting & Simulation: When to Trust a Replay

**Why (impact)**: a sim that says "ship" while live bleeds costs real money (GH#133:
$15.51/day fidelity gap).

- Event-driven vs vectorised replay; why MM needs event-driven
- Fill, latency and fee models; queue position; selective optimism of touch fills
- Look-ahead, survivorship, data snooping
- Sim-vs-live fidelity: measuring the gap; when a sim result can be trusted
- Multi-seed done right (scenario regeneration, not just RNG)

**KCMME example**: compare the public-tape queue-model replay with live spine results for
one coin.
**Ask the AI**: "How far is this sim from live on the same period? Which fill model?"
**Cross-links**: MM Level 8 (Queue/Fill Probability), Level 13 (Simulation).

## Level 8 — Overfitting & Robust Validation

**Why (impact)**: a tuned parameter that wins on the data it was tuned on usually loses
live.

- In-sample vs out-of-sample; walk-forward; purged time-series cross-validation
- The "best of N trials" trap; deflated Sharpe
- Regime dependence; testing across coins and periods
- Parameter stability and sensitivity; when a "win" was a bug artifact

**KCMME example**: check one spine parameter's chosen value across coins and days.
**Ask the AI**: "How many variants were tried? Does it hold on data it never saw?"
**Cross-links**: MM Level 14 (Statistical Validation), Level 15 (Adaptive Control).

## Level 9 — Signals & Time Series

**Why (impact)**: every quote adjustment is a bet that some signal predicts the next move.
A signal that only predicts in-sample costs spread for nothing.

- Linear & logistic regression — what coefficients mean, R², residuals, in plain words
- Stationarity, autocorrelation, EWMA, half-life
- Microstructure features: OFI, microprice, imbalance, trade sign, volatility
- Out-of-sample evaluation; calibration of predicted probabilities

**KCMME example**: how well does order-flow imbalance predict the 1 s markout on one coin?
**Ask the AI**: "What does it predict, at which horizon, out of sample, net of cost?"
**Cross-links**: MM Level 4 (Fair Value), Level 6 (Adverse Selection).

## Level 10 — Research Notes & Research Review

**Why (impact)**: the cheapest place to kill a bad idea is on paper, before build.

- Writing a note: question, mechanism, evidence, prediction, risks, kill criteria, rollout
- Reviewing others' research: the senior-reviewer question list
- Pre-mortems; communicating uncertainty to traders, investors, management

**KCMME example**: write (Claude drafts, learner judges) the research note for the next
spine change before the AI plans it; compare with the AI plan.
**Ask the AI**: "What is the mechanism, the predicted number, and the kill criterion?"
**Cross-links**: Level 0 research note; delivery-workflow-gaps Appendix A.

## Level 11 — Production Risk Controls & Operations

**Why (impact)**: survival — one unguarded bad day can end the business.

- Pre-trade checks, position/notional limits, kill switches, fat-finger guards
- Monitoring: what to watch live (fills, markouts, latency, rejects)
- Deployment: canary, rollback, config management
- Reconciliation, incident response, blameless postmortems
- Exchange rules: rate limits, self-trade prevention, order-to-trade ratios

**KCMME example**: walk the spine's stop / kill path against a past incident.
**Ask the AI**: "What stops this if it goes wrong, and how fast?"
**Cross-links**: MM Level 17 (Risk), Level 18 (Operations).

---

# LIFETIME — "I set direction"

## Level 12 — Optimal Market-Making Models
Avellaneda–Stoikov, Guéant–Lehalle, Cartea–Jaimungal — the intuition, not the derivation:
reservation price, optimal spread, inventory penalty; calibrating them from data; where they
break in crypto. **KCMME example**: the spine's quote-distance formula vs the textbook one.
**Cross-links**: MM Levels 5, 7.

## Level 13 — Machine Learning for Microstructure
Label design (markout labels), gradient boosting, drift and monitoring; when ML beats a hand
model and when it is theater. **Cross-links**: MM Level 6.

## Level 14 — Latency & Infrastructure Economics
Tick-to-trade, jitter, colocation, kernel bypass — as economics: when does speed earn more
than it costs? **KCMME example**: the 56 ms gateway path vs ~1–2 ms network.
**Cross-links**: MM Level 9.

## Level 15 — Portfolio, Risk & Capital Allocation
Cross-coin/venue hedging, correlation, drawdown control, VaR/CVaR in plain words; capital to
coins and venues by risk-adjusted return. **Cross-links**: MM Levels 16, 17, 19.

## Level 16 — Leading Research: Agenda, Prioritisation, Founder Lens
Ranking ideas by expected value × probability × cost; what to stop; build vs buy; what makes
a MM business viable; review standards and hiring.

---

# JOB-READY BUILD TRACK — "I can code every concept I understand" (last tier)

Starts only after the concept tiers. Each step re-implements concepts already understood —
from THIS course and the Market Making course — so coding is learned on ideas that are
already clear. Hands-on: the learner writes the code; Claude reviews like a senior.

- **B1 — Python research stack**: pandas/numpy, notebooks, plotting; code Level 1
  waterfall, Level 2 CI and fills-needed, Level 3 A/B grading, MM markout curves.
- **B2 — Data & replay**: load tick logs, rebuild an order book, a small event-driven
  replay with a fill model (QRE 5, 7; MM 2, 8, 13).
- **B3 — Signals & validation in code**: regression, walk-forward, calibration
  (QRE 8, 9; MM 4, 6, 14).
- **B4 — C++ reading & writing**: modern C++, the spine strategy rewritten by hand,
  tests and sanitizers (QRE 6, 11; MM 5, 7, 10, 11).
- **B5 — Performance & low latency**: profiling, allocation-free hot paths, lock-free
  queues (QRE 14; MM 9).
- **B6 — Interview mastery & career**: probability puzzles, market-making games, coding
  rounds, trading-system design; the KCMME story from `qre-career-portfolio.md`; target
  firm map (Wintermute, GSR, Keyrock, Flowdesk, Auros, B2C2 → Optiver, IMC, Jane Street,
  HRT, Citadel Securities).

## Capstone — "Day One at a MM Firm" Simulation
Given an unfamiliar MM engine (KCMME treated as new), within one working session:
(1) draw its system map, (2) produce yesterday's attribution, (3) spot one statistically
real issue, (4) write the research note for its fix, (5) review an AI-written
implementation of that fix and accept or reject it with reasons. Pass = day-one ready.
