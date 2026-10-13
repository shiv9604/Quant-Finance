# Quant Research Engineer — Learning Roadmap (Levels 0–19)

Goal: become an industry-ready **Quant Developer / Quant Research Engineer** for a
market-making desk who contributes from day one — and, as the same skill, be able to
judge every AI-written plan and result on KCMME (plan granularity + "is this right?").

Ordering principle: **by impact, not by time.** Each level is placed where it unlocks the
most judgment on KCMME and the most hireability. Earlier levels are prerequisites for
later ones. Teaching format: `learning-template/qre-topic-template.md` (7-step contract).

Role this course targets (how a MM desk splits the work you currently do alone):

| Desk role | Owns | KCMME equivalent |
|---|---|---|
| Quant Trader | live behaviour, params, daily P&L judgement | you as PO watching runs |
| Quant Researcher | hypothesis, model, statistical proof | feature planning + "is it right?" |
| **Quant Developer / Research Engineer** ← target | research → production, sim/backtest infra, data pipelines, proving code matches research | what the LLM implements + your review |
| Core C++ / Trading Systems Eng | gateways, hot path, latency | engine core, venue adapters |

Domain pillar (market microstructure) lives in `5. Market Making/market-making.md`
Levels 0–20. This course covers the OTHER pillars (statistics, research method,
engineering, career) and cross-links into MM levels — never duplicates them.

---

## Progress

| Tier | Level | Topic | Hireability bar unlocked | Status |
|---|---|---|---|---|
| Foundation | 0 | How a MM desk works — the research → production loop | — | ⬜ |
| Foundation | 1 | P&L attribution & markouts | Junior | ⬜ |
| Foundation | 2 | Probability & statistics for noisy outcomes | Junior | ⬜ |
| Foundation | 3 | Experiment design & hypothesis testing | Junior | ⬜ |
| Foundation | 4 | Python research stack on real trading data | Junior | ⬜ |
| Foundation | 5 | Market data engineering | Junior | ⬜ |
| Foundation | 6 | Reading C++ for review | Junior | ⬜ |
| Foundation | 7 | System map & code review in a trading engine | **Junior-ready** | ⬜ |
| Intermediate | 8 | Backtesting & simulation methodology | Mid | ⬜ |
| Intermediate | 9 | Regression & time series for signals | Mid | ⬜ |
| Intermediate | 10 | Overfitting & robust validation | Mid | ⬜ |
| Intermediate | 11 | Research notes & research review | Mid | ⬜ |
| Intermediate | 12 | Writing performant modern C++ | Mid | ⬜ |
| Intermediate | 13 | Production trading engineering & risk controls | **Mid-ready** | ⬜ |
| Lifetime | 14 | Optimal market-making models (stochastic control) | Senior | ⬜ |
| Lifetime | 15 | Machine learning for microstructure | Senior | ⬜ |
| Lifetime | 16 | Low-latency systems | Senior | ⬜ |
| Lifetime | 17 | Portfolio, risk & capital allocation | Senior | ⬜ |
| Lifetime | 18 | Leading research — agenda, prioritisation, platform | Senior / founder | ⬜ |
| Lifetime | 19 | Interview mastery & career strategy | **Hire-ready** (runs alongside from L2) | ⬜ |

---

# FOUNDATION — "I can judge plans and results on KCMME" + Junior-ready

## Level 0 — How a MM Desk Works: the Research → Production Loop

**Why first (impact)**: names the loop you are already running alone, shows which steps
need human judgment (research note, research review, daily attribution) and why an LLM
cannot supply judgment nobody in the loop has. Every later level slots into this loop.

- [ ] The four roles (QT / QR / QD / Core Eng) and how they hand work to each other
- [ ] The loop: research note → research review → implementation → sim/backtest
      reproduction → small-size live (often A/B) → daily attribution → scale or kill
- [ ] What a "research note" contains: hypothesis, mechanism, predicted effect as a
      number, evidence, kill criteria
- [ ] Where judgment lives in the loop vs where execution lives
- [ ] Crypto MM vs TradFi prop vs bank desk — how the roles collapse at small firms

**KCMME exercise**: map one closed feature (e.g. M8) onto the loop; mark which steps
had human judgment and which were AI-only.
**Job-readiness**: Junior — can describe the loop and their place in it on day one.
**Interview**: "Walk me through how a strategy change goes from idea to production."
**LLM-judgment unlock**: "Which step of the loop is this AI output, and who should
have reviewed it?"
**Cross-links**: market-making.md Level 0 (Mental Model), Level 20 (Institutional Reality).

## Level 1 — P&L Attribution & Markouts

**Why (impact: highest)**: the debugger of a trading system. Without it, "we lost
money" can't be traced to a cause, so no fix can be judged. Unlocks reading every
KCMME run yourself.

- [ ] Gross vs net P&L; realised vs unrealised; mark-to-market
- [ ] The waterfall: spread capture − adverse selection − inventory MTM − fees
      (± rebates, funding) = net
- [ ] Markouts: price move after a fill at fixed horizons (100ms / 1s / 5s / 60s);
      reading a markout curve
- [ ] Per-fill → per-asset → per-session aggregation; why averages hide tails
- [ ] Reconciliation: engine P&L vs exchange truth (and why they diverge)

**KCMME exercise**: build (by hand, in a notebook) the waterfall for one recent
session from fills + diag; explain the biggest bar.
**Job-readiness**: Junior — produces an attribution for a session. Mid — owns the
daily attribution dashboard. Senior — decides strategy changes from it.
**Interview**: "Your MM made +$10k gross and lost $3k net. Where do you look?"
**LLM-judgment unlock**: "Which waterfall bar is this change supposed to move, by how
much, and did that bar actually move?"
**Cross-links**: MM Level 3 (Maker Economics), Level 6 (Adverse Selection);
Profitability L1, L12.

## Level 2 — Probability & Statistics for Noisy Outcomes

**Why (impact)**: in quant work "is it right?" mostly means "is the effect real or
noise?". This level is the single biggest gap between frontend judgment and quant
judgment.

- [ ] Random variables, distributions (normal, fat-tailed), mean, variance, standard
      deviation
- [ ] Standard error and why it shrinks with √n (the square root of the sample size)
- [ ] Confidence intervals; "how many fills do I need to trust +$0.02/fill?"
- [ ] Expected value and its link to P&L per fill
- [ ] Fat tails, outliers, median vs mean; why one bad fill can flip a session
- [ ] Conditional probability & Bayes (the language of adverse selection)
- [ ] Correlation vs causation; autocorrelation (why fills aren't independent)

**KCMME exercise**: compute the confidence interval of mean P&L-per-fill for one
asset; state whether the session result is distinguishable from zero.
**Job-readiness**: Junior — computes and reads a CI. Mid — sizes experiments before
running. Senior — catches statistical errors in others' research.
**Interview**: probability puzzles (dice / coins / expected value); "a strategy made
money 6 of 10 days — is it good?"
**LLM-judgment unlock**: "Is the sample big enough for this effect to beat noise?
What's the interval, not the point estimate?"
**Cross-links**: MM Level 14 (Statistical Validation) — this level is its prerequisite.

## Level 3 — Experiment Design & Hypothesis Testing

**Why (impact)**: turns runs from "see what happens" into evidence. Fixes the KCMME
failure class "the result looked good but was an artifact" (GH#109, same-scenario
multi-seed).

- [ ] Hypothesis → prediction-as-a-number → kill criteria, written BEFORE the run
- [ ] Baseline and control; changing one thing at a time
- [ ] A/B testing, interleaving, paired comparisons on the same market
- [ ] p-values, statistical power, minimum detectable effect — in plain words
- [ ] Confounders: regime, asset, time of day, latency
- [ ] Ablation: proving which component of a change caused the effect

**KCMME exercise**: write a pre-registration (prediction + kill criteria) for the next
KCMME feature run, then grade the run against it.
**Job-readiness**: Junior — follows the protocol. Mid — designs the experiment.
Senior — rejects a result for a design flaw.
**Interview**: "Design an experiment to test whether a new skew logic reduces adverse
selection."
**LLM-judgment unlock**: "What's the control? What else changed? What result would
have killed this?"
**Cross-links**: MM Level 13 (Simulation), Profitability L13 (validation ladder).

## Level 4 — Python Research Stack on Real Trading Data

**Why (impact)**: the working tool of every quant role; also the hands for Levels 1–3.
Your existing ATQF-with-python notes are the base.

- [ ] numpy, pandas (groupby, merge_asof for time joins, resample), polars basics
- [ ] Loading jsonl/parquet logs; timestamps and timezones
- [ ] Plotting distributions, markout curves, time series (matplotlib/plotly)
- [ ] Reproducible notebooks: fixed inputs, no hidden state, results that re-run
- [ ] Vectorised vs loop code; memory for large tick files

**KCMME exercise**: a reusable notebook that loads one session's fills + diag and
produces the Level 1 waterfall + Level 2 CI. Becomes your personal analysis kit.
**Job-readiness**: Junior — answers an ad-hoc question from data in an hour. Mid —
builds shared tooling. Senior — sets data/analysis standards.
**Interview**: live pandas exercise (join trades to quotes as-of time, compute markouts).
**LLM-judgment unlock**: "Can I reproduce this number myself from raw logs?"

## Level 5 — Market Data Engineering

**Why (impact)**: every model sits on market data; bad data = confident wrong answers.

- [ ] Feeds: L2 snapshots + diffs, trades/aggTrades, sequence numbers, gaps, resyncs
- [ ] Order-book reconstruction and validation
- [ ] Timestamps: exchange vs receive vs process time; clock sync; latency measurement
- [ ] Data quality checks: crossed books, stale quotes, duplicate/missing messages
- [ ] Storage: tick data formats (parquet, columnar DBs, kdb+/q awareness)

**KCMME exercise**: audit one session's market data for gaps/staleness; quantify how
often the engine quoted on a stale book.
**Job-readiness**: Junior — finds data issues. Mid — owns a feed handler/validator.
Senior — designs the data platform.
**Interview**: "How do you rebuild an order book from a diff feed and know it's correct?"
**LLM-judgment unlock**: "Which clock is this timestamp? Could this signal be using
data the engine didn't have yet (look-ahead)?"
**Cross-links**: MM Level 2 (LOB), Level 9 (Latency/Staleness).

## Level 6 — Reading C++ for Review

**Why (impact)**: you don't need to write the hot path to judge it, but you must read a
diff with confidence. Your existing cpp.md is the base.

- [ ] Types, units and numeric precision (double, integer ticks, overflow, rounding)
- [ ] Ownership & lifetime: stack vs heap, references, RAII, unique/shared_ptr
- [ ] const-correctness, pass-by-value vs reference — what costs allocations
- [ ] Concurrency basics: threads, atomics, mutexes, data races
- [ ] Common trading-code bugs: unit mismatch (bps vs fraction), sign errors on
      side, stale-state reads, integer division, uninitialised fields
- [ ] Reading CMake/build output and compiler warnings

**KCMME exercise**: review one real KCMME diff (from git log) with a written review
comment list — as you would for an Angular PR.
**Job-readiness**: Junior — reviews safely, asks the right questions. Mid — writes
production C++ (Level 12). Senior — owns hot-path standards.
**Interview**: "What's wrong with this snippet?" (C++ code reading questions)
**LLM-judgment unlock**: "Units? Side sign? Thread that writes vs threads that read?"

## Level 7 — System Map & Code Review in a Trading Engine

**Why (impact)**: closes "implementation theater" (code exists but its output is never
used). After this you can draw KCMME from memory and trace any parameter to its use.
**Completing L0–7 = Junior Quant Developer bar.**

- [ ] Canonical MM engine architecture: market data → fair value → signals → quoting
      → risk checks → order gateway → fills → position/P&L → hedging
- [ ] Invariants and where they're enforced (position limits, kill switch, hedge)
- [ ] Tracing a parameter end to end: config → load → consumer → decision → log
- [ ] Trading-specific review checklist (safety, units, state machine, failure paths)
- [ ] How to review AI-written code at scale: diff → claims → evidence

**KCMME exercise**: hand-drawn KCMME data-flow map + trace 3 parameters to their
decision point; flag any that are computed but never consumed.
**Job-readiness**: Junior — onboards onto a firm's engine fast. Mid — owns a component.
Senior — owns architecture.
**Interview**: "Design a market-making system for one venue" (trading system design).
**LLM-judgment unlock**: "Where is this new output CONSUMED? Show me the decision path."
**Cross-links**: MM Level 10 (Execution Engineering).

---

# INTERMEDIATE — "I own a component" + Mid-ready

## Level 8 — Backtesting & Simulation Methodology
- [ ] Event-driven vs vectorised backtests; why MM needs event-driven
- [ ] Fill models (queue position, trade-through), latency models, fee models
- [ ] Look-ahead bias, survivorship bias, data snooping
- [ ] Sim-vs-live fidelity: measuring the gap; when a sim result can be trusted
- [ ] Multi-seed done right (scenario regeneration, not just RNG)

**KCMME exercise**: measure sim-vs-live gap for one asset; write the fidelity verdict.
**Interview**: "Your backtest says +20% and live loses. List the causes in order."
**Cross-links**: MM Level 8 (Queue/Fill Probability), Level 13 (Simulation).

## Level 9 — Regression & Time Series for Signals
- [ ] Linear & logistic regression — what coefficients mean, R², residuals
- [ ] Stationarity, autocorrelation, EWMA, half-life
- [ ] Microstructure features: OFI, microprice, imbalance, trade sign, volatility
- [ ] Predicting short-horizon returns and fill probability; evaluating with
      out-of-sample data
- [ ] Calibration curves and reliability buckets for probabilities (e.g. p_tox)

**KCMME exercise**: regress 1s markout on OFI/imbalance for one asset; report
out-of-sample predictive power.
**Interview**: "Build a signal that predicts the next mid move. How do you know it works?"
**Cross-links**: MM Level 4 (Fair Value), Level 6 (Adverse Selection).

## Level 10 — Overfitting & Robust Validation
- [ ] In-sample vs out-of-sample; walk-forward; purged time-series cross-validation
- [ ] Multiple testing and the "best of N trials" trap; deflated Sharpe
- [ ] Regime dependence; testing across assets and periods
- [ ] Parameter stability and sensitivity analysis
- [ ] When a fix's "win" is a bug artifact (re-baseline discipline)

**KCMME exercise**: walk-forward test of one tuned KCMME parameter; report stability.
**Interview**: "You tried 200 parameter sets and the best has Sharpe 3. Is it real?"
**Cross-links**: MM Level 14 (Statistical Validation), Level 15 (Adaptive Control).

## Level 11 — Research Notes & Research Review
- [ ] Writing a research note: question, mechanism, evidence, prediction, risks,
      kill criteria, rollout plan
- [ ] Reviewing others' research: the senior-reviewer question list
- [ ] Pre-mortems; communicating uncertainty to traders and management
- [ ] Turning a KCMME feature contract into a research-note-shaped plan

**KCMME exercise**: write the research note for the next KCMME feature BEFORE the AI
plans it; compare with the AI plan and log the differences.
**Interview**: "Present a project where your hypothesis was wrong. What did you learn?"

## Level 12 — Writing Performant Modern C++
- [ ] Modern C++ (17/20): move semantics, templates basics, constexpr, std containers
- [ ] Cache-friendliness, allocation-free hot paths, object pools
- [ ] Lock-free queues / SPSC ring buffers; memory ordering basics
- [ ] Profiling (perf, flame graphs) and micro-benchmarking
- [ ] Testing C++: unit tests, sanitizers (ASan/TSan/UBSan)

**KCMME exercise**: profile one KCMME hot path and make one measured improvement.
**Interview**: C++ coding + "implement an order book with O(1) best-price access."

## Level 13 — Production Trading Engineering & Risk Controls
**Completing L8–13 = Mid Quant Developer bar.**
- [ ] Pre-trade risk checks, position/notional limits, kill switches, fat-finger guards
- [ ] Monitoring & alerting: what to watch live (fills, markouts, latency, rejects)
- [ ] Deployment: canary, rollback, config management, feature flags
- [ ] Reconciliation with exchange; incident response and blameless postmortems
- [ ] Exchange rules: rate limits, self-trade prevention, order-to-trade ratios

**KCMME exercise**: write a postmortem for one past KCMME incident in firm format.
**Interview**: "Engine is live and position is growing unexpectedly. First 5 minutes?"
**Cross-links**: MM Level 17 (Risk), Level 18 (Operations).

---

# LIFETIME — "I set direction" + Senior / founder

## Level 14 — Optimal Market-Making Models (Stochastic Control)
- [ ] Avellaneda–Stoikov, Guéant–Lehalle–Fernandez-Tapia, Cartea–Jaimungal
- [ ] Reservation price, optimal spread, inventory penalty — derivation intuition
- [ ] Calibrating model parameters (arrival intensity, volatility, risk aversion) from data
- [ ] Where models break in crypto (fat tails, regime shifts, multi-venue)
**Cross-links**: MM Levels 5, 7.

## Level 15 — Machine Learning for Microstructure
- [ ] Gradient boosting, feature engineering, label design (markout-based labels)
- [ ] Online learning, concept drift, model monitoring
- [ ] Latency-aware inference; when ML beats a hand model and when it doesn't

## Level 16 — Low-Latency Systems
- [ ] Network stack, kernel bypass, NIC timestamping, colocation
- [ ] Tick-to-trade measurement; jitter; FPGA awareness
- [ ] Crypto venue realities (REST/WS limits, cloud regions)
**Cross-links**: MM Level 9.

## Level 17 — Portfolio, Risk & Capital Allocation
- [ ] Cross-asset/cross-venue hedging, correlation, beta
- [ ] VaR/CVaR, stress tests, drawdown control
- [ ] Capital allocation across assets by risk-adjusted return
**Cross-links**: MM Levels 16, 17, 19.

## Level 18 — Leading Research: Agenda, Prioritisation, Platform
- [ ] Ranking research ideas by expected value × probability × cost
- [ ] Building research platforms other people use
- [ ] Mentoring, setting review standards, hiring
- [ ] Founder lens: when to build vs buy, what makes a MM business viable

## Level 19 — Interview Mastery & Career Strategy
Runs ALONGSIDE from Level 2 onward (each level's interview drill feeds it).
- [ ] Probability & brainteasers, mental math, market-making games (quote a market
      on an unknown quantity)
- [ ] Coding rounds (Python data, C++), trading system design
- [ ] Telling the KCMME story: from `qre-career-portfolio.md`, STAR-format
- [ ] Target firm map: crypto MMs (Wintermute, GSR, Keyrock, Flowdesk, Auros, B2C2)
      → TradFi prop (Optiver, IMC, Jane Street, HRT, Citadel Securities)
- [ ] Resume, referrals, how to get past screening with a non-quant degree path

---

## Capstone — "Day One at a MM Firm" Simulation

After Level 13: given an unfamiliar MM engine (KCMME treated as if new), within one
working session: (1) draw its system map, (2) produce yesterday's attribution,
(3) spot one statistically-real issue, (4) write the research note for its fix,
(5) review an AI-written implementation of that fix and accept or reject it with reasons.
Pass = Mid Quant Developer, day-one ready.
