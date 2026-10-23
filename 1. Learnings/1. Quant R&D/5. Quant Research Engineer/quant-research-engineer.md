# Quant Research Engineer

The engineering, statistics and research-method half of working on a market-making desk —
the skills that let a Quant Developer / Quant Research Engineer contribute to a firm's MM
engine from day one, and judge any plan or result (human- or AI-written) on it.
The market-microstructure half lives in `../../5. Market Making/market-making.md`.

## Foundation

> Onboarding read — the have-to-know basics, good enough for juniors.
> Grows as Foundation levels are taught; full depth lives in the Level sections below.

### The research → production loop (Level 0)
Ideas reach live trading through: research note (hypothesis with a predicted number + kill
criteria) → independent research review → implementation → reproduction → small-size live
A/B → daily attribution → scale or kill. Four roles run it: Quant Trader (live P&L), Quant
Researcher (ideas + proof), Quant Developer (research → production, proves the code matches
the research), core engineer (latency/plumbing). The reviewer is never the author.

### A/B testing (Level 0)
Old (A) and new (B) run at the same time in the same market — interleaved time blocks,
symbol split, or size split — so the market cancels out and only the change remains.
Before-vs-after cannot separate your change from the market's change.

### The P&L waterfall (Level 1)
Every fill's result splits into bars that add up exactly: spread capture s×(m₀−p)×q,
adverse selection s×(m_H−m₀)×q, inventory MTM s×(m_T−m_H)×q, minus fees (s = +1 buy / −1
sell, p = fill price, q = qty, m₀ = mid at fill, m_H = mid H later, m_T = mid at end).
+ = earned, − = lost. Markouts at several horizons show *what kind* of adverse selection.
Reconcile to the exchange before trusting any bar.

## Levels 0–19 — Full Depth

> One section per roadmap level (`learning-roadmap/qre-roadmap.md`), in order, each
> written end-to-end per `learning-template/qre-topic-template.md` (sections 1–11).
> *(Pending)* = not yet taught.

### Level 0 — How a MM Desk Works: the Research → Production Loop

**Status: ✅ Taught 2026-10-21.**

#### 1. What It Is
A market-making desk turns ideas into live trading through a fixed loop of stages, each
owned by a specific role. The loop exists because trading correctness is **statistical**
(only visible as an average over many fills) and **adversarial** (other traders adapt),
so "build → test → ship" — which works when correctness is visible, like a UI button —
lets wrong ideas reach real money. Getting it wrong means paying for mistakes at the most
expensive stage (full-size live) instead of the cheapest (on paper).

#### 2. Simple Example
Idea: "fills right after a burst of aggressive buying lose money — quote wider after bursts."
- **Lone loop** (build → backtest → ship): built in 2 days, backtest says +$1,200/month,
  shipped full size → week 1 −$900, week 2 −$700, turned off, nothing learned. Total −$1,600.
- **Desk loop**: research note predicts "adverse-selection loss (loss from trading with
  better-informed traders) $0.04 → under $0.02 per fill; kill if under $0.01 better after
  5,000 fills" → review asks "what else causes bursts?" and finds 30% are liquidations and
  the firm's own hedges → filter added → 10%-size A/B shows $0.04 → $0.025 → scaled up.
  Slower to go live (~3 weeks vs 3 days), faster to something that actually works.

#### 3. Why the Naive Approach Fails
A strong software engineer runs the loop they know: idea → build → test → ship. In trading
the "test" step (a backtest — replaying past market data through the code) flatters you:
history does not react to your orders, and trying many variants makes one look good by
luck. Nobody challenged the idea, nobody wrote down what result would prove it wrong, so
bad weeks get explained away ("weird market") instead of stopping the change.
*Analogy:* a student who writes the exam, sits it and marks it — every step done, the
grade means nothing, because the marker shares the writer's blind spots.

#### 4. How It Works (Simple → Sophisticated)
- **Layer 1 — build → backtest → ship.** Fast. *Still misses:* backtests flatter; nobody
  challenges the idea before money is spent.
- **Layer 2 — + research note.** Before code: hypothesis **with a number**, mechanism (why
  it should work), evidence, **kill criteria** (the pre-written result that proves it wrong).
  A number makes the claim falsifiable — "$0.04 → under $0.02" can fail; "should help" cannot.
  *Still misses:* the author's own blind spots.
- **Layer 3 — + research review.** Seniors attack the note: what else explains it? is the
  sample big enough to beat noise? does it hold in another month? Most ideas die here,
  which is the cheapest place to die. *Still misses:* live-market reality.
- **Layer 4 — + small-size live A/B + daily attribution + scale-or-kill.** Run at ~10% size,
  as an **A/B test** (below); each morning split the P&L into its cost bars and check the
  predicted bar moved by about the predicted amount; compare to the kill criteria → scale
  up step by step, or switch off and record what was learned. **This is the professional loop.**

```
research note → research review → implementation → backtest/sim reproduction
      → small-size live (A/B) → daily attribution → scale or kill
```

**Cost ladder — why the order is fixed:** a bad idea dying at note/review costs ~1 day and
$0 trading loss; at backtest ~1 week; at small-size live a few hundred dollars; at full-size
live $10,000–$100,000+. Cheap filters first.

**The four roles and their hand-offs** (one idea, end to end):

| Step | Who | Produces |
|---|---|---|
| Notice | Quant Trader (owns live behaviour + daily P&L) | message to research |
| Investigate | Quant Researcher (owns ideas + statistical proof) | research note |
| Challenge | senior QR + QT | review comments → revised note |
| Build | Quant Developer / Research Engineer (research → production; tooling) | code + **reproduction report**: replaying history through the new code reproduces the research numbers within a margin |
| Plumbing | Core / trading-systems engineer (gateways, hot path, latency) | latency sign-off |
| Trial | QT + QD | daily attribution on a small-size A/B |
| Decide | QT + QR | scale or kill vs the pre-written criteria |

The Quant Developer's job is not "write the code" — it is **proving the code matches the research.**

**A/B testing.** Run the old version (A) and the new one (B) **at the same time, in the same
market**, so the market cancels out and only your change remains. *Before vs after* fails:
last week calm (−$0.02/fill, old logic) vs this week volatile (−$0.05, new logic) looks
2.5× worse — but the market changed too; the new logic may have saved you from −$0.08.
On one engine you usually cannot run A and B on the same coin at the same instant — two
quoters compete for the same fills, see each other's orders as market data, and two own
accounts filling each other is **wash trading** (trading with yourself — banned by
exchanges, treated as manipulation). Desks instead:
- **interleave in time** — 10 min A, 10 min B, all day (the market cancels out best; the
  usual choice for quoting changes);
- **split by symbol** — A on some coins, B on others, balanced and swapped halfway;
- **split by size** — B on 10% of quoting size (limits damage).

Worked example (interleaved, 1 week): A 2,400 fills at −$0.040/fill, B 2,350 at −$0.026 →
B saves ~$0.014/fill. A/B rules out **the market** as the explanation; statistics (Level 2)
rules out **luck** — is $0.014 bigger than the random wobble between two groups of ~2,400
fills? You need both, and a minimum sample: 40 vs 52 trades cannot be trusted even in a
perfect A/B.

**Where judgment lives:** research note, research review, deciding whether to trust a
backtest, explaining why an attribution bar moved, scale-or-kill — **judgment**.
Implementation, running the backtest, deploying, computing the bars — **execution**.
An LLM is strong on execution and can produce judgment-shaped text, but judgment means
predicting before seeing the result and seeing what the author missed. AI reviewing AI adds
**checking**, not **independence** — similar training, similar blind spots.

**How roles collapse by firm type:**

| Firm | Examples | Roles |
|---|---|---|
| TradFi prop (trades own money) | Optiver, IMC, Jane Street, HRT | fully separate, formal review |
| Large crypto MM | Wintermute, GSR, Keyrock | blur — QDs research, QTs code |
| Small crypto MM (10–30 people) | many | QR + QD often one person; head of trading reviews |
| Bank desk | big banks | client-driven; risk/compliance layers; slowest |

As firms shrink, roles combine — but the **reviewer is never the author**.

#### 5. Why Should You Believe This? — The Same Idea, Run Two Ways

| | Lone loop | Desk loop |
|---|---|---|
| Day 1 | building | research note with prediction + kill rule |
| Day 2 | backtest +$1,200/month | review finds 30% burst contamination → filter |
| Day 3 | shipped full size | building; reproduction matches research within 10% |
| Week 1 | −$900, "weird market" | 10%-size A/B: −$0.04 → −$0.027 |
| Week 2 | −$700, live tweaks (now nobody knows which change did what) | −$0.025, kill rule not hit |
| Week 3 | turned off, nothing learned | 50% → 100% |
| Result | −$1,600, no knowledge | small trial cost, real improvement, written record of why |

#### 6. Professional Standard (Jane Street / Optiver / Citadel Securities / Wintermute)
Every economic change has a written, reviewed research note with a predicted effect and
pre-written kill criteria; the reviewer is independent of the author; the developer proves
reproduction; live starts small and concurrent (A/B); attribution is daily and tied to the
prediction; scale-or-kill is decided against criteria written before the test; the note is
graded afterwards and feeds the next idea.

#### 7. Summary + Sees vs Misses

| | |
|---|---|
| **What it is** | The fixed research → production loop and the four roles that run it |
| **Why it matters** | Trading correctness is statistical and adversarial — only this loop catches wrong ideas cheaply |
| **Professional standard** | Predicted number + kill criteria up front, independent review, reproduction, small concurrent A/B, scale-or-kill |

| Loop | Sees | Misses |
|---|---|---|
| Build → ship | whether code runs | whether the idea is right; noise vs effect |
| + backtest | rough historical effect | history doesn't react; luck across many variants |
| + research note | a falsifiable claim + kill criteria | the author's blind spots |
| + research review | what the author couldn't see, cheaply | live-market reality |
| + small A/B + attribution + scale/kill | real effect, which bar moved, a stop rule | — (the standard) |

Three distinctions to keep: **prediction vs result** · **parameter setting vs outcome
claim** · **tests passing vs code matching the research.**

#### 8. Industry Practice — How a Desk Does This Manually
- **Owners:** QT notices (live P&L), QR writes the note, senior QR/QT review, QD builds +
  reproduces, core engineer signs latency, QT+QR decide scale-or-kill.
- **Rituals:** research review meetings (often weekly); morning P&L attribution review
  daily; post-trial grading of the note; blameless postmortem when something goes wrong live.
- **Tooling:** notes in a shared doc/wiki; Python/Jupyter for evidence; internal sim/backtester;
  feature flags + size controls for small-size live; attribution dashboards.

#### 9. Job-Readiness by Seniority

| Bar | Can do | Day-one contribution |
|---|---|---|
| **Junior** | describe the loop, the roles and their place in it; follow the protocol | implement from an approved note; ask "what's the predicted number and kill rule?" |
| **Mid** | own a change end to end: write the reproduction report, design the A/B, run attribution | turn a researcher's note into a reproduced, small-size A/B with a clean verdict |
| **Senior** | review others' notes; reject a result for a design flaw; set the kill criteria | run research review; push back on deadlines ("trial by Friday; scaling depends on results") |

#### 10. Interview Drill
- **Concept:** "Walk me through how a strategy change goes from idea to production." —
  *Junior:* researcher → review → developer → infra check → small A/B → scale. *Mid adds:*
  the QT often notices first; the QD's reproduction report; daily attribution; pre-written
  kill criteria and an explicit kill path, not only scale-up.
- **Numeric:** "+$0.01/fill, 20,000 fills/day. Yearly value? If it really loses $0.02/fill,
  cost of one full-size week? As a 10%-size trial?" — $73,000 (365 days — read the spec);
  $2,800; $280. *Senior adds:* a bad full-size week is ~4% of a year's upside, so the trial
  is cheap insurance — but 10% size gives 14,000 fills/week instead of 140,000, so the trial
  must still be big enough to beat noise.
- **Scenario:** "Day 3 as a QD: 'quote tighter on SOL, backtest +$4,000/month', ship by
  Friday." — *Before:* define "tighter" exactly (ticks from mid, by how much); challenge
  adverse selection (tighter quotes get picked off more); ask for the evidence and kill
  criteria. *After (Mid/Senior):* replay the backtest through your code — does it reproduce
  ~+$4,000?; question the backtest — fill models assume you're filled whenever price touches
  you, which flatters tight quoting more than anything; is +$4,000/month bigger than normal
  monthly swings?; propose a 10%-size A/B by Friday, scaling on results.

#### 11. LLM-Judgment Checklist
Ask of any AI plan or result:
1. Is there a predicted **outcome** number (not just parameter settings)? From what, to what, why?
2. Were kill criteria written **before** the test? What exact result would stop it?
3. Who reviewed it, and did they attack the **idea** or only the implementation? Same model as the author?
4. Does "tests pass" claim more than "the code does what the coder intended"? Where is the reproduction against the research numbers?
5. Is the comparison concurrent (same time, same market) or before-vs-after? How many fills per side?
6. Is more than one thing changed at once?
7. Does the rollout skip the small-size step?
8. Was a bad result explained away instead of judged against the pre-written rule?


### Level 1 — P&L Attribution & Markouts

**Status: ✅ Taught 2026-10-23.**

#### 1. What It Is
P&L attribution splits a trading result into its causes — bars that add up exactly to the
total. A market maker's core bars: **spread capture** (traded better than fair at the instant
of the fill), **adverse selection** (the price moved against you right after — the other side
knew more), **inventory MTM** (ordinary drift while you keep holding), **fees**. Markouts —
the price move at fixed horizons after a fill — measure adverse selection. Without
attribution, "we lost money" cannot be traced to a cause, so no fix (human or AI) can be judged.
Sign convention: **+ = earned, − = lost.**

#### 2. Simple Example
Two days, both −$50:

| | Day A | Day B |
|---|---|---|
| Spread captured | +$400 | +$200 |
| Adverse selection | −$380 | −$50 |
| Inventory MTM | −$40 | −$170 |
| Fees | −$30 | −$30 |
| **Net result** | **−$50** | **−$50** |

Day A: picked off → widen/skew on informed flow. Day B: held inventory too long → unload or
hedge faster. Same total, opposite fixes; widening on Day B cuts the +$200 spread and makes it worse.

#### 3. Why the Naive Approach Fails
Looking only at the total (the restaurant owner who sees −$2,000 and raises prices when the
real cause was food waste) tells you *that* you lost, not *why*, so you fix the wrong thing.
Profit-per-round-trip is next most common and still mixes spread with price move, ignores open
inventory, and can't tell an instant loss (sniped) from a slow one (drift).

#### 4. How It Works (Simple → Sophisticated)

**Layer 1 — total P&L = realised + unrealised (mark-to-market).** Unrealised counts open
positions at the current mid; without it you can look profitable by never closing losers.
*Still misses:* why.

**Layer 2 — profit per round trip.** *Still misses:* spread vs move; open inventory; instant vs slow.

**Layer 3 — the per-fill waterfall.** Symbols: **s** = your side (+1 bought, −1 sold) · **p** =
your fill price · **q** = quantity · **m₀** = mid at the fill, (best bid + best ask) ÷ 2 ·
**m_H** = mid a fixed time H later · **m_T** = mid at the end / at close.

```
spread capture    = s × (m₀  − p)   × q     how much better than fair you traded
adverse selection = s × (m_H − m₀)  × q     price move against/for you right after
inventory MTM     = s × (m_T − m_H) × q     drift while you kept holding
fee bar           = − fee                   fees are always money lost
─────────────────────────────────────────
net result        = s × (m_T − p) × q − fee
```

- **Why × s:** "good" is opposite for buyers (pay less than fair; want the price to rise after)
  and sellers (receive more than fair; want it to fall). s = −1 flips a seller's numbers so every
  bar reads + = good for me, − = bad for me. Without it a good sell (sold at $102, mid $100:
  100 − 102 = −2) shows as a loss.
- **Why × q:** (m₀ − p) is per coin; × q turns it into dollars for the size traded.
- **Why − fee:** fees are recorded as an amount paid (positive); for you it's a loss.
- **Why the bars add up exactly:** each bar starts where the previous stops (fill price → mid at
  fill → mid at H → mid at end), so the middle prices cancel. Adding signed bars *is* how costs
  get subtracted. **Classic error:** measuring adverse from the fill price instead of the mid —
  it then contains the spread, and spread + adverse counts the spread twice (or, if spread is
  computed against the fill price, spread reads 0 and all of it lands in "adverse").
- **Worked buy:** bought 1 at p $149.98, m₀ $150.00, m_H $149.94, m_T $149.80 → spread +$0.02,
  adverse −$0.06, inventory −$0.14, total −$0.18 = 149.80 − 149.98 ✓.
- **Worked sell:** sold 1 at $150.02, m₀ $150.00, m_H $150.05 → spread +$0.02 (sold above fair),
  adverse −$0.05 (price rose after selling).
- **Sanity check:** price never moves → only spread capture remains. ✓

*Still misses:* everything depends on the horizon H — too short mislabels slow informed moves
as inventory; too long blames ordinary drift on adverse selection.

**Layer 4 — the markout curve (several horizons).** Average markout per fill at
100 ms / 1 s / 5 s / 60 s; the shape names the cause:

| Curve | 100 ms | 1 s | 5 s | 60 s | Means | Fix direction |
|---|---|---|---|---|---|---|
| A | −0.05 | −0.06 | −0.06 | −0.06 | **sniped** — faster traders hit stale quotes | speed: cancel/reprice faster |
| B | −0.01 | −0.03 | −0.06 | −0.07 | **informed flow** | widen/skew on flow signals |
| C | −0.03 | −0.02 | 0.00 | +0.01 | temporary pressure that **reverts** | fine; maybe exiting too early |
| D | ~0 | ~0 | ~0 | ~0 | **benign** flow | quote tighter here |

Choose H for the waterfall where the curve flattens. Compare across assets in **bps**
(1 bp = 0.01% of price): $0.02 on $150 = 1.33 bps. *Still misses:* tails and which asset/venue.

**Layer 5 — slicing and tails.** Averages hide tails: 950 fills at +$0.005 and 50 at −$0.295
average −$0.01 ("mild") while 5% of fills do all the damage — the fix is avoiding those 50, not
widening everywhere. Look at the **distribution**: median (middle value), percentiles (e.g. the
5th percentile — only 5% of fills are worse). Slice by **maker vs taker**, asset, venue, hour:
a session −$50 can be BTC +$30 and DOGE −$80; a near-zero total can be makers +$0.29 vs takers
−$0.30. *Still misses:* whether the input numbers are true.

**Layer 6 — reconcile with exchange truth.** The waterfall is only as good as its fills.
Reconcile daily against the exchange: fill count (maker/taker), commission, realized P&L,
position. Add an **unexplained** bar:
`spread + adverse + inventory − fees + unexplained = exchange-reported change`.
If unexplained ≉ 0, fix the data before trusting any other bar. A log that silently drops
taker exits — the most expensive fills — makes the whole picture too kind.

#### 5. Why Should You Believe This?
Without attribution, two −$50 days → "widen spreads" → on Day B spread capture falls
+$200 → ~+$120 while the inventory bleed (−$170) stays → ~−$130, and the next step is "widening
didn't help, try something else" — a random walk through changes. With attribution each fix is
aimed at one named bar, and tomorrow's waterfall says whether that bar moved. This is the
Level 0 link: a hypothesis says *which bar moves by how much*; the waterfall checks it.

#### 6. Professional Standard
Per-fill waterfall + multi-horizon markouts in bps against a fair-price reference (mid or
microprice); morning review sliced by asset/venue/hour/fill type with tail statistics;
reconciled to exchange/clearing daily with unexplained ≈ 0; an independent recompute of the
bars (labels, not just sums); changes judged by which bar moved vs the predicted bar.

#### 7. Summary + Sees vs Misses

| | |
|---|---|
| **What it is** | Splitting P&L into spread, adverse selection, inventory MTM and fees that add up exactly |
| **Why it matters** | Different bars → different fixes; the total alone sends you to the wrong fix |
| **Professional standard** | Reconciled, multi-horizon, sliced, independently recomputed attribution every day |

| Method | Sees | Misses |
|---|---|---|
| Total P&L | whether you made money | why |
| Per round trip | average trade quality | spread vs move; inventory; instant vs slow |
| Waterfall (one H) | spread / adverse / inventory / fees, exact sum | mislabels if H badly chosen |
| Markout curve | kind of adverse selection | tails; which asset/venue |
| Slicing + distributions | where it bleeds; few-fills tails | whether the data is true |
| + reconciliation | every bar is real (unexplained ≈ 0) | — (the standard) |

#### 8. Industry Practice — How a Desk Does This Manually
- **Owners:** Quant Developers build and own the attribution pipeline and reconciliation;
  Quant Traders read it every morning; researchers use markouts to build and test signals;
  operations/finance own reconciliation with the clearing/exchange statement.
- **Rituals:** daily morning P&L attribution review; daily reconciliation break report (any
  unexplained difference is chased the same day); markout review per strategy change.
- **Tooling:** tick/fill stores (kdb+/q, ClickHouse, parquet), Python/pandas notebooks,
  dashboards (Grafana/internal), the exchange/clearing statement as the reconciliation source.

#### 9. Job-Readiness by Seniority

| Bar | Can do | Day-one contribution |
|---|---|---|
| **Junior** | compute the waterfall per fill with correct signs; split maker/taker; read which bar dominates | rebuild yesterday's attribution from raw fills and match the dashboard |
| **Mid** | own the pipeline: multi-horizon markouts, slicing, daily reconciliation, catch definition bugs | find why the dashboard and the exchange disagree, fix the definition |
| **Senior** | judge strategy changes from it; set the canonical definitions; decide H per strategy | reject a "−40% adverse selection" claim that only moved cost between bars |

#### 10. Interview Drill
- **Concept:** "+$10k gross, −$3k net — how do you find out why?" — *Junior:* break into bars,
  split maker/taker. *Mid:* $13k sits between gross and net → costs; reconcile first (is the
  +$10k real?), fees by maker/taker and tier, slice asset/venue/hour. *Senior:* "gross positive
  means the edge works — this is a cost problem, not a strategy problem."
- **Numeric:** bought 2 at $99.95, m₀ $100.00, m_1s $99.90, fee $0.04 → spread +$0.10,
  adverse **−$0.20** (sign!), net **−$0.14** (fee always comes off); bad fill — picked off within a second.
- **Scenario:** "AI: new feature cut adverse selection 40%, recommend default-ON." Check:
  (1) fills reconciled to the exchange; (2) recompute the bars — adverse measured from the mid or
  from the fill price?; (3) other bars and net — widening often cuts adverse *and* fills/spread,
  moving cost between bars; (4) Level 0: concurrent A/B, sample, predicted number, kill rule.

#### 11. LLM-Judgment Checklist
1. Were the fills reconciled to the exchange (count, maker/taker, commission, realized P&L)? Is unexplained ≈ 0?
2. Is adverse selection measured from the **mid at fill** — or from the fill price (which swallows the spread)?
3. Does a bar read exactly 0? Suspect a definition artifact before believing it.
4. Is there a maker/taker split and per-asset breakdown, or only a total/average?
5. Which markout horizons? One short horizon can't rule out informed flow.
6. Are assets compared in bps / per fill, or in raw dollars?
7. Does the proposed fix target the bar that actually dominates — and what does it do to the other bars and the net?


### Level 2 — Probability & Statistics for Noisy Outcomes
*(Pending)*

### Level 3 — Experiment Design & Hypothesis Testing
*(Pending)*

### Level 4 — Python Research Stack on Real Trading Data
*(Pending)*

### Level 5 — Market Data Engineering
*(Pending)*

### Level 6 — Reading C++ for Review
*(Pending)*

### Level 7 — System Map & Code Review in a Trading Engine
*(Pending)*

### Level 8 — Backtesting & Simulation Methodology
*(Pending)*

### Level 9 — Regression & Time Series for Signals
*(Pending)*

### Level 10 — Overfitting & Robust Validation
*(Pending)*

### Level 11 — Research Notes & Research Review
*(Pending)*

### Level 12 — Writing Performant Modern C++
*(Pending)*

### Level 13 — Production Trading Engineering & Risk Controls
*(Pending)*

### Level 14 — Optimal Market-Making Models (Stochastic Control)
*(Pending)*

### Level 15 — Machine Learning for Microstructure
*(Pending)*

### Level 16 — Low-Latency Systems
*(Pending)*

### Level 17 — Portfolio, Risk & Capital Allocation
*(Pending)*

### Level 18 — Leading Research: Agenda, Prioritisation, Platform
*(Pending)*

### Level 19 — Interview Mastery & Career Strategy
*(Pending)*
