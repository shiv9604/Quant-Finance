# KCMME Profitability Learning Roadmap

Goal: understand end-to-end why the engine is gpnl-negative and what to do about it.
Work through each layer in order. Mark `[x]` when done.

---

## Layer 0 — Fair Value / Microprice Quality

**Why first**: spread is placed around fair value. If fair value is wrong, spread cannot protect you. Bad fair value = adverse selection even with zero informed flow. Everything downstream assumes fair value is correct.

- [ ] Understand the difference between last traded price, mid price, and fair value
- [ ] Learn microprice: how order book imbalance shifts fair value above/below mid
- [ ] Learn cross-exchange anchoring: which exchange is the price leader? (Binance in KCMME's case)
- [ ] Understand momentum adjustment: repeated aggressive flow shifts fair value in flow direction
- [ ] Learn what "stale BBO" means and how often KCMME quotes on one
- [ ] Answer: is KCMME using raw mid or microprice? What adjustments are active?
- [ ] Core question to answer: **is the adverse selection we observe from informed flow, or from a lagging fair value estimate?**

**Files**: `src/fair_value*.cpp`, `diag_*.jsonl` (fair_value, mid, microprice fields)

---

## Layer 1 — Fill Markout Analysis

**Why**: without markouts, everything else is guessing. Markouts tell you whether the fill was toxic, whether inventory carry caused the loss, and whether the spread was wide enough.

- [ ] Understand what a fill markout is: price movement against fill direction at fixed horizons
- [ ] Learn the horizons: 100ms, 500ms, 1s, 5s — each captures a different risk component
  - 100ms: immediate adverse selection (was the fill sniped?)
  - 500ms–1s: short-term informed flow
  - 5s: inventory carry regime
- [ ] Run markout analysis per asset using `scripts/analysis/adverse_selection_report.py`
- [ ] Read fills from `fills_*.jsonl` and cross-reference with `diag_*.jsonl`
- [ ] Answer for each asset: what is the average adverse move at 100ms / 500ms / 1s / 5s?
- [ ] Identify which assets have toxic fills vs which have near-zero post-fill drift

**PRE-CHECK BEFORE RUNNING**: verify session is not a Potemkin first (Layer 0.5 below).

**Core equation**:
```
fill_ev = half_spread - adverse_markout
```
If adverse_markout > half_spread → negative EV per fill even if spread capture looks fine.

---

## Layer 0.5 — Potemkin / Engine vs Infra Metric Check

**Why before markout**: if the session data is a Potemkin (engine claims dispatches that never reached exchange), markout analysis is fabricated. Check this before trusting any session data.

- [ ] Understand engine metric vs infra metric:
  - Engine metric = did engine decide to dispatch? (`dispatch_called` count)
  - Infra metric = did venue actually place? (exchange `placed_count` from REST)
  - These can diverge completely — engine shows 128 dispatches, exchange shows 0
- [ ] Learn to run exchange truth cross-check:
  ```bash
  python scripts/verify/exchange_truth/cross_venue_truth.py --cyc <N> --checkpoint T+1h --env testnet
  ```
- [ ] Understand the 6 axes: placed_truth, filled_truth, per-symbol Potemkin, position residue, open order imbalance, rate-limit budget
- [ ] Learn the rule: if placed_count_truth diverges >25% from engine-reported → session data cannot be trusted for profitability analysis
- [ ] KCMME history: this happened in cyc111, cyc115, cyc136, cyc138 — it is recurring, not rare

---

## Layer 2 — Adverse Selection / TailScore

**Why**: the biggest profitability layer. If we can price adverse selection before the fill happens, we can quote worse on the toxic side and avoid negative-EV fills.

- [ ] Understand p_tox: probability a fill is from informed/toxic flow
- [ ] Learn TailScore: toxicity × severity (expected loss magnitude, not just probability)
- [ ] Learn VPIN (Volume-synchronized PIN): volume-bucket-based flow imbalance measure
- [ ] Learn OFI (Order Flow Imbalance): aggressive buy volume minus aggressive sell volume
- [ ] Understand CVaR99 tail loss: expected loss in the worst 1% of fills
- [ ] Learn how toxic fill buckets work: repeated fills on same side = clustering, not random
- [ ] Understand the three toxicity signals in KCMME's defensive alpha layer:
  - Flow toxicity (leading signal): `tox_flow = |EWMA(trade_sign)|`
  - Drift toxicity (realized signal): `tox_drift = max(0, -drift_after_fill)`
  - Volatility risk (uncertainty signal): `tox_vol = sigma_short / sigma_long`
- [ ] Understand why global thresholds are dangerous: AAVE ≠ SUI ≠ TRUMP ≠ NEO
- [ ] Current KCMME state: VPIN weakly active, burst/OFI weights = 0 (regressed sim) — know why

**Core question**: can we quote worse on the toxic side before the fill happens?

---

## Layer 3 — Latency / Stale Quote Exposure ✅ Done

**Why here (moved from #5)**: stale quote exposure is a mechanism of adverse selection — both arise from information lag. Structurally adjacent, not a separate topic.

- [ ] Understand what a stale quote is: quote whose price no longer reflects fair value
- [ ] Learn quote age: time between last update and fill event
- [ ] Learn cancel ack latency: time between cancel request and exchange acknowledgment
- [ ] Learn stale fill probability: P(fill before cancel ack completes)
- [ ] Core equation:
  ```
  stale_loss = P(fill before cancel ack) × expected adverse move in that window
  ```
- [ ] Understand that at 10ms AWS Tokyo RTT, KCMME is much better than old Delta India (750–1000ms), but still exposed during cancel/replace windows
- [ ] Learn that faster cancel speed requires tighter spreads to remain competitive — infra advantage translates directly to EV
- [ ] Read `diag_*.jsonl` for `cancel_latency`, `quote_age`, `stale_fill_count` fields

---

## Layer 4 — Spread vs Adverse Move ✅ Done

**Why**: this is where EV lives. The spread must be wide enough to cover expected adverse move, or every fill is a slow leak.

- [ ] Understand half-spread capture: we earn half-spread at fill time, not full spread
- [ ] Learn that round-trip spread is not guaranteed (second leg may never fill)
- [ ] Learn spread floor: minimum spread below which EV is structurally negative regardless of signals
- [ ] Understand volatility spread: wider spread required when price is jumping
- [ ] Understand toxicity spread: wider spread required when flow is informed
- [ ] Understand asset-specific spread width: each asset has a different equilibrium
- [ ] Core equation in practice:
  ```
  fill_ev = half_spread - expected_adverse_move
  ```
- [ ] For each asset: at current spread settings, is fill_ev positive at 100ms horizon? At 1s horizon?
- [ ] Identify which assets have structurally thin spreads relative to their adverse move

---

## Layer 4.5 — Queue / Fill Quality

**Why here (moved from #6)**: queue position determines P(fill), which is an input to EV. EV = P(fill) × half_spread − P(fill) × EAM. Cannot compute spread vs adverse move properly without understanding P(fill) by queue depth.

- [ ] Understand BBO fill vs deeper fill: quoting at BBO = higher P(fill) + more toxic fills
- [ ] Understand the tradeoff: 1–2 ticks deeper = lower P(fill) + less toxic fills
- [ ] Learn queue priority: FIFO ordering means early queue position = less toxic fills (sweepers fill the back)
- [ ] Learn cancel/replace churn: every cancel+replace moves you to back of queue at that price level
- [ ] Understand fill-after-sweep: being filled when the level is swept = almost certainly toxic
- [ ] Core question: are we being filled because our quote is good, or because the level was swept?
- [ ] Learn KCMME's BBO-relative quoting: quotes placed around BBO, not raw mid — understand why (CKS 2011 queue-aware P(fill))

---

## Layer 5 — Inventory Carry — Single Venue

**Why**: the second major gpnl layer. Even if fills are good, holding inventory against price drift causes losses.

- [ ] Understand inventory = net position from executed trades
- [ ] Learn inventory age: how long a position has been held
- [ ] Understand mark-to-market loss: unrealized PnL as price moves against inventory
- [ ] Understand realized vs unrealized gpnl split
- [ ] Learn how quote skew pushes inventory back toward flat
- [ ] Learn when unwind is too expensive (spread wider than skew benefit)
- [ ] For each fill, split the PnL attribution:
  - spread capture component
  - adverse markout component
  - inventory carry component
  - exit cost component
- [ ] Understand inventory compounding: if flow stays one-sided, inventory builds nonlinearly
- [ ] Core question: is gpnl negative because fills are bad, or because inventory carried against us after fill?

---

## Layer 5.5 — Cross-Venue Delta Neutrality (KCMME-specific, critical)

**Why here**: KCMME quotes on Binance, Bybit, and BitMEX simultaneously. Per-venue inventory can look flat while cross-venue net is a large directional position. This is causing real losses on mainnet right now.

- [ ] Understand that per-venue "flat" ≠ system flat
  - Bybit: flat
  - Binance spot: +5 SUI
  - BitMEX: -80 SUI
  - Net system exposure: -75 SUI directional short — completely undetected by per-venue analysis
- [ ] Learn that hedge controller's job is to maintain cross-venue neutrality
- [ ] Understand when hedges fail: venue connectivity, rate-limit exhaustion, bad dispatch (Potemkin)
- [ ] Learn the cross-venue delta formula:
  ```
  net_delta(symbol) = sum of signed_position(symbol, venue) across all venues ≈ 0
  ```
- [ ] Understand what happens when net_delta grows unchecked: running an unintentional directional book that compounds losses
- [ ] Read `state/analyses/exchange_truth_*.json` for per-venue positions and cross-venue net
- [ ] KCMME history: cyc131 SUI net -70, cyc138 SUI net -110 — this is an active, recurring issue (bug_class_014)
- [ ] Core question: at any point in time, what is the true cross-venue net exposure per symbol?

---

## Layer 6 — Funding Rate / Basis in Perpetuals

**Why**: KCMME trades perpetual futures (Bybit perps, BitMEX perps). Funding payments are a systematic PnL drain unrelated to fill quality. They explain slow consistent bleed even when individual fills look OK.

- [ ] Understand what funding rate is: payment between longs and shorts every 8 hours
- [ ] Understand funding direction:
  - Positive funding → longs pay shorts
  - Negative funding → shorts pay longs
- [ ] Understand that if KCMME is long SUI and funding is negative → paying every 8h regardless of fills
- [ ] Learn basis: price difference between spot and perpetual
  - Positive basis (perp > spot) → market is bullish, longs pay funding
  - Negative basis (perp < spot) → market is bearish, shorts pay funding
- [ ] Understand that inventory carry analysis at Layer 5 will look like "engine holds too long" but the real cause may be funding eating carry
- [ ] For each asset: what is the typical funding regime? Does holding inventory in the hedge-required direction compound or offset funding cost?
- [ ] Core question: how much of KCMME's inventory carry loss is adverse price movement vs funding payments?

---

## Layer 7 — Cancel/Replace Churn Ratio

**Why**: operational efficiency. High churn = doing a lot of work to capture few fills, and it exhausts venue rate limits which then blocks flatten/hedge dispatches.

- [ ] Learn cancel/fill ratio: number of cancels per actual fill
- [ ] Understand that high churn has two costs:
  - API rate limit exhaustion (directly caused GH#477: Bybit per-UID limit exhausted → naked short)
  - Moving to back of queue on every cancel+replace (reduces fill quality)
- [ ] Learn to read `placed_count`, `fill_count`, `cancel_ratio` from PCIV metrics
- [ ] Understand rate limit budget: `rl_pct` field in diag — what % of budget is being consumed?
- [ ] Learn the rule: if rl_pct > 80% consistently → engine is churn-heavy, fix quoting stability
- [ ] Core question: what is KCMME's cancel/fill ratio per venue per asset? Is it within healthy bounds?

---

## Layer 8 — Asset-Wise Profitability

**Why**: some assets are structurally quoteable for this engine right now; others are not. Global metrics hide this.

- [ ] For every active asset, build a per-asset profile:
  - fill_count
  - gpnl
  - adverse markout (100ms, 1s, 5s)
  - CVaR99 tail loss
  - stale quote loss
  - inventory carry component
  - funding cost
  - spread capture
  - TailScore effectiveness
  - VPIN reliability
  - burst/OFI reliability
- [ ] Identify SUI as a known loss driver across sims — understand why structurally
- [ ] Identify which assets have features that help vs which are globally-hurt by current thresholds
- [ ] Understand that some features help basket-wide but worsen specific assets → global thresholds are dangerous
- [ ] Core question: which assets are structurally quoteable for this engine right now?

---

## Layer 9 — Per-Asset Calibration

**Why**: same controller, different weights per asset. Profitability probably improves most here after the basic stack is understood.

- [ ] Understand per-asset TailScore thresholds vs global thresholds
- [ ] Learn per-asset VPIN reliability: VPIN works well on some assets, not others
- [ ] Learn per-asset burst/OFI reliability: which assets respond predictably to OFI?
- [ ] Understand cold-start protection: new session has no calibrated state → conservative defaults
- [ ] Learn adaptive threshold mechanics: how thresholds update as session data accumulates
- [ ] Understand reliability buckets: when does a signal earn trust vs when is it noise?
- [ ] Core idea: AAVE ≠ SUI ≠ TRUMP ≠ NEO — treating them identically is leaving money on the table

---

## Layer 10 — Market Regime Classification

**Why**: trending vs mean-reverting vs choppy regimes have completely different EV profiles. Quoting in a trending regime without regime-awareness is structural adverse selection.

- [ ] Understand the three market regimes relevant to a market maker:
  - **Trending**: adverse selection is structural, EV per fill is systematically negative regardless of spread — spreads must be much wider
  - **Mean-reverting / choppy**: inventory mean-reverts, fills are less toxic, EV is positive even at tighter spreads
  - **Volatility spike**: fair value jumps discontinuously, stale quote exposure dominates
- [ ] Learn VPIN as a regime detector: high VPIN → trending / informed flow; low VPIN → choppy
- [ ] For each historical session: classify regime and compute per-asset EV by regime
- [ ] Understand that some assets may only be quoteable in specific regimes (SUI candidate for "chop-only")
- [ ] Core question: in what regime was the session, and was the spread appropriate for that regime?

---

## Layer 11 — Post-Fill Monetization ✅ Done

**Why**: after being filled, what does the engine do with inventory? This is the second decision after the fill.

- [x] Understand hold vs immediate exit tradeoff
- [x] Learn skew: pushing reservation price to encourage opposite-side fill
- [x] Learn passive recycle: posting on opposite side to naturally unwind inventory
- [x] Learn aggressive exit: IOC or market order to immediately flatten at cost — confirmed always a net loss at standard tier, ~4 ticks cost round-trip on Binance USDT-M
- [x] Learn predictive exit: exit based on signal prediction before adverse move completes
- [x] Learn trailing stop: hold while profitable, exit when giveback exceeds threshold
  - KCMME thresholds: trail_peak_min_natural_mult=0.5×spread (arm), trail_giveback_frac=0.20 (20% giveback), Layer A forced exit ramp 30→60s, Layer B drift stop 3.0→6.0 ticks
- [x] Learn Poisson maker-first timer: t* = −ln(0.05)/λ_exit_side per asset; SUI 500/hr → 21s, thin token → 18min; regime-adjusted + carry-bounded
- [x] Learn inventory aging: when does carry risk exceed the cost of forced exit?
- [x] Cross-venue hedge lifecycle: hedge position becomes independent inventory; double-duty for subsequent fills; never pay two takers for one fill
- [x] Mode A (same-venue exit chain) vs Mode B (cross-venue hedge chain) — end-to-end flow for both
- [x] Break-even math: Mode B via BitMEX only beats Mode A when P(maker fill cross-venue) > 71%; below 71%, same-venue IOC (0.05%) cheaper than BitMEX IOC (0.075%)
- [x] A/B measurement framework: tag exit_mode + exit_method per fill, 200-fill rolling cost window per asset, hysteresis mode selector
- [x] Implementation stack: λ_exit_side tracker (foundational) → t* per asset → HedgeRouter maker-first phase → per-fill exit tags → per-asset mode selector
- [x] Core question: after a fill, is KCMME monetizing inventory or letting it drift into loss? → KCMME has strong post-fill stack (trailing, drift stop, forced exit), but no maker-first timer, no λ_exit_side tracker, no per-fill exit mode tagging for A/B comparison, and no per-asset σ-calibrated carry threshold

---

## Layer 12 — GPNL Attribution Decomposition ✅ Done

**Why**: "the engine is gpnl-negative" is not actionable. This framework breaks down WHY.

- [x] Learn the per-fill PnL decomposition formula: GPNL = spread_captured − adverse_5s − inv_holding − hedge_slippage − exit_cost − fees + residual
- [x] Understand what each component measures and what drives it
- [x] Learn fill-type classification: Type A (profitable) / Type B (break-even) / Type C (catastrophic — adverse > spread)
- [x] Learn root-cause tagging per Type C fill: VPIN high / σ_spike / queue position back / trending regime
- [x] Learn the attribution waterfall presentation and how it maps to layer fixes
- [x] Understand the reconciliation residual as a falsification signal — non-zero = measurement bug, not noise
- [x] Core question: does KCMME have attribution? → M1 system is institutional-quality (7 components, falsifiable residual, all logged to diag.jsonl). Missing: per-session waterfall report script (data exists, reader absent), fill-type classification script, per-fill root-cause snapshot (tox_raw/regime_idx not in FillRecord at fill time), B5 inventory half-life parser
- [ ] Learn KCMME's 3-method gpnl reconciliation (method A, B, C) — why 3 methods and what they each capture
- [ ] Core question: per session, per asset — which component caused the loss?

---

## Layer 13 — Validation Discipline

**Why**: a change is not good if it only reduces fills. A change is good if it improves fill quality, adverse loss, inventory carry, or gpnl without hidden regression.

- [x] Learn the validation ladder: Sim (floor) → Testnet (real flow) → Mainnet (ground truth). Cannot skip rungs.
- [x] Learn what makes a sim result trustworthy: ±25% fidelity gate + scenario-regen multi-seed + multi-regime + baseline comparison on identical inputs
- [x] Learn multi-seed correctly: same scenario + different seed only tests engine RNG, NOT robustness. Must regenerate full scenario per seed.
- [x] Understand live/sim divergence: sim must track live within ±25% before any change is validated. Broken fidelity = fix fidelity first.
- [x] Learn MinTRL: minimum fills before Sharpe is statistically meaningful (~60–80 fills at SR=1.0, 95% confidence). Below MinTRL, positive SR could be luck.
- [x] Learn Deflated Sharpe (DSR): adjusts raw Sharpe for skew, kurtosis, and number of prior trials. More parameter sweeps before picking the winner → lower DSR.
- [x] Learn validate-freeze: one layer at a time (toxicity → EV hold → P(fill) → spread). Simultaneous changes make attribution impossible.
- [x] Learn the key invalidations: bug-induced prior wins / same-scenario seed / single-session overfit / sim diverged / simultaneous changes
- [x] Learn attribution delta: validate that the TARGET component (e.g. adverse_5s) improved, not just total GPNL
- [x] KCMME check: strong DSR + MinTRL + ±25% gate + scenario-regen multi-seed + TailScore walk-forward + capital-safety gate. Gaps: no walk-forward gate for TOML strategy params (L9-GAP-1), n_trials not tracked for DSR (may understate multiple-testing), attribution delta not formally gated

---

## What You Should Be Able To Answer (Final Checklist)

After completing all layers, you should be able to answer these for any session:

- [ ] Was the session a Potemkin? Did dispatches actually reach the exchange?
- [ ] What was the fair value anchor? Was it accurate?
- [ ] Why did this fill lose money? Isolate the cause:
  - Was the quote stale?
  - Was the spread too thin?
  - Was the fair value wrong?
  - Was the fill toxic (informed flow)?
  - Did inventory carry create the loss?
  - Was funding draining the carry?
  - Was this asset unsuitable in this regime?
  - Did our controller predict it?
  - Was cross-venue delta building up undetected?
- [ ] Did the sim prove the change or fool us?
- [ ] Is the sample large enough to trust the verdict?

---

## The One Fill End-to-End Skill

Master reading a single fill completely:

**Before fill:**
- p_tox
- TailScore
- VPIN
- OFI
- quote age (stale?)
- spread width
- inventory (per-venue AND cross-venue net)
- d_star
- fair value vs exchange mid

**At fill:**
- side (bid fill or ask fill)
- fill price vs fair value at time of fill
- queue position estimate
- was level swept or did we get normal fill?

**After fill:**
- markout at 100ms / 500ms / 1s / 5s
- inventory change (per-venue and net)
- skew response: did quotes adjust?
- exit/unwind behavior
- gpnl impact decomposed: spread_captured / adverse_markout / carry / funding

---

## Progress Tracker

| Layer | Topic | Status |
|-------|-------|--------|
| 0 | Fair Value / Microprice Quality | ✅ Done |
| 0.5 | Potemkin / Engine vs Infra Check | ✅ Done |
| 1 | Fill Markout Analysis | ✅ Done |
| 2 | Adverse Selection / TailScore | ✅ Done |
| 3 | Latency / Stale Quote Exposure | ✅ Done |
| 4 | Spread vs Adverse Move | ✅ Done |
| 4.5 | Queue / Fill Quality | ✅ Done |
| 5 | Inventory Carry — Single Venue | ✅ Done |
| 5.5 | Cross-Venue Delta Neutrality | ✅ Done |
| 6 | Funding Rate / Basis in Perpetuals | ✅ Done |
| 7 | Cancel/Replace Churn Ratio | ✅ Done |
| 8 | Asset-Wise Profitability | ✅ Done |
| 9 | Per-Asset Calibration | ✅ Done |
| 10 | Market Regime Classification | ✅ Done |
| 11 | Post-Fill Monetization | ✅ Done |
| 12 | GPNL Attribution Decomposition | ✅ Done |
| 13 | Validation Discipline | ✅ Done |
