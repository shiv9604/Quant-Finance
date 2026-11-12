# Quant Research Engineer — Learning Roadmap

Goal: think and judge like a **Quant Research Engineer** on a market-making desk —
understand every concept, its impact on money, and how it works behind the scene — so
every AI-written plan and result on KCMME can be judged (plan granularity + "is this
right?"). Execution is offloaded to AI while learning; the **Job-Ready Build Track** at the
very end codes every concept from this course AND the Market Making course, which makes
the learner industry job-ready.

Shape (PO 2026-11-13, after a Fable 5.1 relevance review against the business):
- **Order is traditional — by prerequisite**, so it stays right for anyone and for future
  stages. Foundation → Intermediate → Lifetime → Build Track.
- **Relevance comes from the examples**: every level is taught on the current business
  problem first, then future stages, then past (template Example Priority Rule).
- **Speed comes from the format**: about 4–6 messages per level; Claude computes, the
  learner judges (template Low-Friction Pace Rule).
- A level needed early is taught in a separate session on request and marked ✅ here.
Teaching format: `learning-template/qre-topic-template.md` (6-step contract).

Scope boundary: **QRE = how to measure, test, prove, build and run** (statistics,
experiments, metrics, data trust, replay, validation, research process, latency and infra
measurement/engineering, reliability, ops automation, prioritisation). **Market Making =
how markets work** (`5. Market Making/market-making.md`, Levels 0–21: queues, adverse
selection, fair value, spread, inventory, latency as a market race, cross-venue, risk and
business economics). Cross-link, never duplicate. Topics moved to MM on 2026-11-13 went only
into its UPCOMING levels: optimal MM models → MM 21 (new); rebate tiers, volume vs per-$1k,
RPI, colocation value → MM 19; hedging/correlation → MM 16. MM 14 and MM 18 point here for
method.

Role this course targets (how a MM desk splits the work you currently do alone):

| Desk role | Owns | KCMME equivalent |
|---|---|---|
| Quant Trader | live behaviour, params, daily P&L judgement | you as PO watching runs |
| Quant Researcher | hypothesis, model, statistical proof | feature planning + "is it right?" |
| **Quant Developer / Research Engineer** ← target | research → production, sim/backtest infra, data pipelines, proving code matches research | what the LLM implements + your review |
| Core C++ / Trading Systems Eng | gateways, hot path, latency | engine core, venue adapters |

---

## Progress

| Tier | Level | Topic | Needs | Status |
|---|---|---|---|---|
| Foundation | 0 | How a MM desk works — the research → production loop | — | ✅ 2026-10-21 |
| Foundation | 1 | P&L attribution & markouts | 0 | ✅ 2026-10-23 |
| Foundation | 2 | Signal vs noise — statistics for noisy outcomes | 1 | 🟡 in progress |
| Foundation | 3 | Cheap, decisive experiments | 2 | ⬜ |
| Foundation | 4 | Metrics that decide money — like-for-like cost per $1k | 1, 2 | ⬜ |
| Foundation | 5 | Data you can trust — feeds, clocks, recording, logs vs exchange | 1 | ⬜ |
| Foundation | 6 | Replay trust — measuring the sim-vs-live gap | 3, 5 | ⬜ |
| Foundation | 7 | Queue-priority measurement | 5, 6 | ⬜ |
| Foundation | 8 | Overfitting & held-out validation | 2, 3, 6 | ⬜ |
| Intermediate | 9 | Latency measurement & engineering | 5 | ⬜ |
| Intermediate | 10 | Reading an engine — system map & implementation theater | 1 | ⬜ |
| Intermediate | 11 | Venue onboarding & integration verification | 5, 10 | ⬜ |
| Intermediate | 12 | Risk controls & incidents | 10 | ⬜ |
| Intermediate | 13 | Signal evaluation — does it predict, out of sample, after cost? | 8 | ⬜ |
| Intermediate | 14 | Research notes, prioritisation & investor-grade evidence | 3, 4 | ⬜ |
| Lifetime | 15 | Reliability, ops automation & capacity | 9, 12 | ⬜ |
| Lifetime | 16 | Capital allocation across coins & venues — the measurement side | 4, 8; MM 16, 19 | ⬜ |
| Lifetime | 17 | Machine learning for microstructure (optional) | 13 | ⬜ |
| Build Track | B1–B6 | Job-Ready Build Track — code every QRE + MM concept | all concept tiers | ⬜ (last) |

Every level below lists: **Why (impact)** · concepts · **KCMME example** (Claude runs it,
the learner judges) · **Ask the AI** · **Gap hunt** · cross-links.

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
- Clustered fills (autocorrelation): why 100 fills can count as 30; day-clustered
  confidence intervals; three verdicts (pass / fail / continue); correlation ≠ causation

**KCMME example**: the spine sets its adverse-selection cost from the last 20 passive fills
(`AdverseMeter`) — how much does that estimate wobble vs the fills a trustworthy estimate
needs; and a current HTX cost-per-$1k verdict read with day-clustered intervals.
**Ask the AI**: "How many fills / days is this based on? What's the range, not the point?
How many would we need for this effect?"
**Gap hunt**: engine estimates or workflow verdicts made from a sample too small for the
effect they claim.
**Cross-links**: MM Level 14 (Statistical Validation — points here for method).

## Level 3 — Cheap, Decisive Experiments

**Why (impact)**: the idea that drove the strip-down — test an idea for the least money and
time, and get an answer that actually decides. Fixes "the result looked good but was an
artifact" (GH#109).

- Hypothesis → predicted number → kill criteria, written BEFORE the run (pre-registration)
- The cost ladder: thinking → existing data → replay → tiny live → full live
- Control, one change at a time; A/B, interleaving, paired comparisons on the same market
- Minimum detectable effect and power in plain words (links Level 2's fills-needed)
- Running many tests at once: the "many tests" trap and how to correct for it
- Confounders: regime, coin, time of day, latency; ablation (which part caused it)

**KCMME example**: grade the current HTX pre-registered test agenda (11 tests with controls
and kill lines) — which tests are sized to decide, which can only say "continue".
**Ask the AI**: "What's the control? What else changed? What result would have killed this?
Is there a cheaper rung of the ladder that answers it?"
**Gap hunt**: features shipped without a predicted number or kill criteria.
**Cross-links**: MM Level 13 (Simulation), Profitability L13 (validation ladder).

## Level 4 — Metrics That Decide Money: Like-for-Like Cost per $1k

**Why (impact)**: you optimise what you measure. Cost per $1k changed the engine — but the
−0.115 → −0.073 improvement was mostly a coin change, not like-for-like. A metric read
without controls sends the next decision the wrong way.

- Normalising: per fill, per $1k volume, per hour, per unit of capital — and what each hides
- Like-for-like attribution: controlling for coin mix, time band, venue, size
- Decomposing a metric into levers (fees, rebates, adverse, inventory, volume)
- Leading vs lagging metrics; guardrail metrics that must not get worse
- Goodhart's law: when a metric becomes a target it stops measuring

**KCMME example**: split the −0.115 → −0.073 cost change into coin-mix effect vs real
engine improvement; decompose current HTX cost per $1k into levers.
**Ask the AI**: "Is this like-for-like? Which lever moved? Could the metric improve while
we lose money?"
**Gap hunt**: features verified on a metric that doesn't decide money, or not like-for-like.
**Cross-links**: MM Level 3 (Maker Economics), MM Level 19 (rebate tiers, volume vs per-$1k).

## Level 5 — Data You Can Trust

**Why (impact)**: every number sits on data; bad data gives confident wrong answers
(fills.jsonl missing taker exits made gross look 3× too kind; a testnet export read as
mainnet).

- Feeds: L2 snapshots + diffs, trades, sequence numbers, gaps, resyncs
- Timestamps: exchange vs receive vs process time; clock sync
- Look-ahead: using data the engine didn't have yet
- Quality checks: crossed books, stale quotes, duplicate/missing messages
- The recording pipeline: recorder → archive (S3) → fill ledger; completeness checks
- Logs vs exchange truth: reconciliation as a standing habit

**KCMME example**: audit one recent session's fill log and recorder output against
exchange trades for completeness and environment.
**Ask the AI**: "Which clock is this? Is this log complete versus the exchange? Which
environment? Could the signal see the future?"
**Gap hunt**: logs or ledgers that disagree with exchange truth; missing completeness checks.
**Cross-links**: MM Level 2 (LOB), Level 9 (Latency/Staleness).

## Level 6 — Replay Trust: Measuring the Sim-vs-Live Gap

**Why (impact)**: every HTX verdict is a replay calibrated to a live A/B. A replay that says
"ship" while live bleeds costs real money (GH#133: $15.51/day fidelity gap).

- What a replay assumes (fill model, latency, fees) — the concepts are MM Level 13
- Calibration: matching replay to a live A/B on the same period
- Measuring the gap per component; when a replay result can be trusted
- Multi-seed done right (scenario regeneration, not just RNG)

**KCMME example**: the back-of-queue replay vs the live HTX A/B (−0.231 vs −0.236) — what
that agreement does and does not prove.
**Ask the AI**: "How far is this replay from live on the same period, and on which part?"
**Cross-links**: MM Level 8 (Queue/Fill Probability), MM Level 13 (Simulation).

## Level 7 — Queue-Priority Measurement

**Why (impact)**: queue priority drives fills, rebates and revenue — but we can't see our
queue position (L2 only). Without measurement, every "better queue" claim is a guess.

- Estimating our queue position from public L2 data; what is assumed (arrival time)
- Front vs back of queue fills; the value of priority as a measurable number
- Proving a change improved priority: before/after vs concurrent, controls
- Error bars on an estimated position; when the estimate is too weak to decide

**KCMME example**: the HTX queue-position test (front-third vs all fills, BTC + ETH) — what
it can and cannot show with the fills we have.
**Ask the AI**: "How was queue position estimated, what was assumed, and is the effect
bigger than the estimate's error?"
**Gap hunt**: queue claims with no measurement behind them.
**Cross-links**: MM Level 8 (Queue / Fill Probability — how queues behave).

## Level 8 — Overfitting & Held-Out Validation

**Why (impact)**: a setting that wins on the days it was tuned on usually loses live (the
in-sample basket optimiser did not hold out of sample).

- In-sample vs out-of-sample; leave-one-day-out; walk-forward
- The "best of N trials" trap; deflated Sharpe in plain words
- Regime dependence; testing across coins and days
- Parameter stability and sensitivity; when a "win" was a bug artifact

**KCMME example**: the HTX shrunk top-N basket — fitted days vs held-out day.
**Ask the AI**: "How many variants were tried? Does it hold on data it never saw?"
**Cross-links**: MM Level 14 (points here for method), MM Level 15 (Adaptive Control).

---

# INTERMEDIATE — "I can judge the engine, the venue and the research"

## Level 9 — Latency Measurement & Engineering

**Why (impact)**: speed protects against being picked off and buys queue position — but
only measured latency can be improved. Our order path is ~56 ms while the network is
~1–2 ms: the gateway, not the wire.

- Clocks and timestamps for latency; round-trip breakdown by hop
- Gateway path vs network; tail latency (p99), jitter
- Measuring the value of speed: the latency-slope test (gain at 1 / 3 / 5 / 12 ms)
- Where engineering time pays: which hop to cut first
**KCMME example**: break the current order round trip into hops and rank them.
**Ask the AI**: "Which hop is this, measured how, at p50 and p99?"
**Cross-links**: MM Level 9 (latency as a market race), MM Level 19 (what colocation is worth).

## Level 10 — Reading an Engine: System Map & Implementation Theater

**Why (impact)**: closes "implementation theater" (code exists but its output is never
used). Lets you trace any parameter to the decision it changes — without writing C++.

- Canonical MM engine flow: market data → fair value → signals → quoting → risk checks →
  gateway → fills → position/P&L → hedging
- Invariants and where they're enforced (limits, kill switch, stop)
- Tracing a parameter end to end: config → load → consumer → decision → log
- Trading-code bug classes in plain words: units, side sign, stale state, integer division
- Reviewing AI-written code at scale: diff → claims → evidence

**KCMME example**: Claude draws the spine data flow and traces 3 parameters to their
decision point; the learner spots any computed but never consumed.
**Ask the AI**: "Where is this new output CONSUMED? Show me the decision path."
**Cross-links**: MM Level 10 (Execution Engineering).

## Level 11 — Venue Onboarding & Integration Verification

**Why (impact)**: every new exchange (HTX now, Binance next, more later) is a chance to
silently lose fills, pay wrong fees or break tier rules. Verifying an integration is a QRE
job.

- Gateway acceptance tests: orders, cancels, rejects, reconnects
- Fill-stream completeness and fee/environment checks against exchange truth
- Rate limits, contract-size and tick conventions, venue filters
- Tier-keeping metrics (maker share, volume) and monitoring them
**KCMME example**: the current HTX integration checklist — what is proven, what is assumed.
**Ask the AI**: "Which venue rules were tested live, and how do we know no fill is missing?"
**Cross-links**: MM Level 1 (Market Structure), MM Level 18 (exchange rules).

## Level 12 — Risk Controls & Incidents

**Why (impact)**: survival — one unguarded bad day can end the business; larger pilots
raise the stakes.

- Pre-trade checks, position/notional limits, kill switches, loss limits
- Monitoring what matters live: fills, markouts, latency, rejects
- Deployment safety: canary, rollback, config management
- Incident response and blameless postmortems
**KCMME example**: walk the spine's stop / kill path against a past incident.
**Ask the AI**: "What stops this if it goes wrong, how fast, and who is told?"
**Cross-links**: MM Level 17 (risk as a market concept).

## Level 13 — Signal Evaluation

**Why (impact)**: every quote adjustment is a bet that a signal predicts the next move. A
signal that only predicts in-sample costs spread for nothing.

- Regression in plain words: coefficients, R², residuals
- Stationarity, autocorrelation, half-life
- Out-of-sample evaluation, net of cost; calibration of predicted probabilities
- When a small R² is still worth money, and when it isn't
**KCMME example**: one current HTX signal test — out-of-sample predictive power and its
value in bps after cost.
**Ask the AI**: "What does it predict, at which horizon, out of sample, net of cost?"
**Cross-links**: MM Level 4 (Fair Value), MM Level 6 (Adverse Selection) — the features.

## Level 14 — Research Notes, Prioritisation & Investor-Grade Evidence

**Why (impact)**: the cheapest place to kill a bad idea is on paper; the right next idea is
worth more than doing the current one well; investors fund evidence.

- Writing a note: question, mechanism, evidence, prediction, risks, kill criteria, rollout
- Reviewing research: the senior-reviewer question list; pre-mortems
- Ranking ideas by expected value × probability × cost; what to stop
- Presenting evidence honestly to investors: intervals, not best days
**KCMME example**: rank the current cost-down levers; draft (Claude) and judge (learner)
the note for the top one.
**Ask the AI**: "What is the mechanism, the predicted number, the kill criterion — and why
this idea before the others?"
**Cross-links**: Level 0 research note; delivery-workflow-gaps Appendix A.

---

# LIFETIME — "I set direction and scale it"

## Level 15 — Reliability, Ops Automation & Capacity
Monitoring and alerting that a one-person company can run; recorder/archive health;
automating routine operations; capacity and message budgets; size step-ups (1× → 3× → 5×)
with cost measured at each step. **KCMME example**: the "too many open files" stop.
**Cross-links**: MM Level 18 (exchange rules).

## Level 16 — Capital Allocation Across Coins & Venues (measurement side)
Measuring risk-adjusted return per coin and venue; drawdown; how much capital where, and how
to prove it. Concepts (hedging, correlation, business economics) are MM 16 / 17 / 19.

## Level 17 — Machine Learning for Microstructure (optional)
Label design (markout labels), gradient boosting, drift and monitoring; when ML beats a hand
model and when it is theater. **Cross-links**: Level 13, MM Level 6.

---

# JOB-READY BUILD TRACK — "I can code every concept I understand" (last tier)

Starts only after the concept tiers. Each step re-implements concepts already understood —
from THIS course and the Market Making course — so coding is learned on ideas that are
already clear. Hands-on: the learner writes the code; Claude reviews like a senior.

- **B1 — Python research stack**: pandas/numpy, notebooks, plotting; code Level 1
  waterfall, Level 2 intervals and fills-needed, Level 3 A/B grading, MM markout curves.
- **B2 — Data & replay**: load tick logs, rebuild an order book, a small event-driven
  replay with a fill model, queue-position estimate (QRE 5–7; MM 2, 8, 13).
- **B3 — Validation & signals in code**: held-out validation, regression, calibration
  (QRE 8, 13; MM 4, 6, 14).
- **B4 — C++ reading & writing**: modern C++, the spine strategy rewritten by hand,
  tests and sanitizers (QRE 10, 12; MM 5, 7, 10, 11).
- **B5 — Performance & low latency**: profiling, allocation-free hot paths, lock-free
  queues (QRE 9; MM 9).
- **B6 — Interview mastery & career**: probability puzzles, market-making games, coding
  rounds, trading-system design; the KCMME story from `qre-career-portfolio.md`; target
  firm map (Wintermute, GSR, Keyrock, Flowdesk, Auros, B2C2 → Optiver, IMC, Jane Street,
  HRT, Citadel Securities).

## Capstone — "Day One at a MM Firm" Simulation
Given an unfamiliar MM engine (KCMME treated as new), within one working session:
(1) draw its system map, (2) produce yesterday's attribution, (3) spot one statistically
real issue, (4) write the research note for its fix, (5) review an AI-written
implementation of that fix and accept or reject it with reasons. Pass = day-one ready.
