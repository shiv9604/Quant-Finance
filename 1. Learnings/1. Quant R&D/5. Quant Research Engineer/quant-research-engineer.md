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
*(Pending)*

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
