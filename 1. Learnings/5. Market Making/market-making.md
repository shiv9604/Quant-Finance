

# Market Making

Market making is way to provide liquidity on perticular asset or in market provide to keep that instrument tradeable and earning profit from the bid and ask spread.

## Foundation

> Onboarding read — the have-to-know basics, good enough for juniors.
> Full end-to-end depth per topic lives in the Lifetime Depth section below.

### Bid & Ask Price 
Bid is price buyer is willing to pay for asset & ask is price sellers willing to pay for selling an asset.

---
### Spread & Slippage
Highest bid = best buyer
Lowest Ask = best seller
The difference = spread.

Whenever we want to buy or sell any asset in financial market we dont get same buying and selling price, that difference between buying and selling price is called as spread, ie if we want to buy an share its at 100 and if we want to sell that share then we get 99 price, its spread.

Slippage is difference between at price you have place order and the price you get filled, ie When we buy an asset when its trading at 100 but we get filled at 100.10

---
### Orderbook
Orderbook is live list of buyers and sellers listed with their intent buy price aka Bid price & sell intent aka Ask price at specific prices.

We get to see orderbook at each and every asset and its usually exchange level order book, but retail brokers shows limited depth where exchanges have deep order books

`Note - Orderbook is only list of intent, but it does not show who is serious buyer, who will cancel, who is informed, who is toxic.`

---
### Depth of market
The bigger list of buyers and sellers around a price its harder to move that price, but if its smaller its easier to move the price.

Note - This walls can disappear in milliseconds because market makers can cancel quotes in milliseconds.

---
### Market Makers vs Takers

**🟢 Taker**
- Uses market order
- Crosses the spread
- Demands liquidity
- Pays the spread

**🔵 Maker**
- Places limit order
- Waits
- Provides liquidity
- Earns the spread (if not adversely selected)

---
### Why spreads exist?
**Spread exists because:**
- Inventory risk
- Adverse selection risk
- Information asymmetry
- Latency disadvantage
- Spread = compensation for risk.

---
### Market makers & Institutions

Market makers and institutions arent same, market makers provides liquidity in poorly liquid market to make it efficient ie Jane street, Citadel securities, Jump Trading etc. & institutions are people which have potential to buy and sell assets in humongus quantity ie Hedge Funds, Mutual Funds, Family offices.

---
### Liquidity
Liquidity is how easily an asset can be bought and sold without causing much price change, in high liqudit asset such as BTCUSD if you buy $1M it wont cause any change in price but if you trade with same capital in low liquidity like RANDOM MEME COIN or Alt Coin it might cause price increase is called as liquidity.

Liquid market has more buyers and sellers which make it easy to trade with low slippage and spread and in low liquidity market we have less buyers and sellers due to which its hard to trade or bigger slippages and spreads.

**Types of Orders -**
1. **Limit orders -** Its orders are waiting to be filled.
2. **Market orders -** Move price by consuming limit orders.
3. **Deep order book (High liquidity) -** Easy to trade, low spread & slippage and high fill rate.
4. **Shallow order book (Low liquidity) -** Hard to trade, high spread & slippage and low fill rate.

**How liquidity moves price :-**
<img src="./assets/how-liquidity-move-price.png">

For Example - If a person is willing to sell 10 stocks, and in order book 0.01, 0.53, 0.05, 6, 0.01 in bids in first 5 rows, as you can see it will move the price till 1068.46 or in orderbook until our 10 quantity is bought and fully bought and vice versa for buy example.

**Types of Liquidity -**
1. **Active vs Passive -** Market orders is active & passive is limit orders.
2. **Retail vs Institutional -** Retail are small players and institutions are big players, both can provide/take liquidity.
3. **Hidden -** Iceberg orders, ie if we have 1000 quantity in order book only 100 will posted, once its filled again 100 will appear until full quantity filled. its smart way to fill big orders without causing big price change.
4. **Latent -** This are stop orders until they are triggerd like stop loss orders or tp orders.
5. **Fake -** As called as spoofing as well, where people put big orders intentionally to mislead others and cancel it before executed.

**Liquidity Pools & Voids -**
1. **Liquidity pools -** Cluster of stoploss or tp orders at obvious highs and lows based on retail trading concepts.
2. **Liquidity voids -** Thinkly traded zones where price moves fast.

---

## Intermediate to Advance — Lifetime Depth (Levels 0–20)

> The senior read. One section per Lifetime Roadmap level, in chronological
> order, each written end-to-end — navigate to a level and learn it inside out.
> Program restarted from Level 0 on 2026-07-10.
> *(Pending)* = not yet taught. *(Interim)* = content moved from Foundation,
> to be rewritten to full depth when its level is taught. The standalone
> terminology entries at the end of this section fold into their home levels
> as those levels are taught.

### Level 0 — Mental Model

**Status: ✅ Taught 2026-07-23.**

#### 1. What It Is

A market maker doesn't sell predictions — it sells *immediacy*. Someone wants to trade *right now* without waiting for a natural counterparty to show up; the MM is the counterparty who's always there, and the bid-ask spread is the price of that service. But spread collected is not spread kept: everything that can go wrong between opening a position and closing it eats into that spread. The mental model a market maker needs is not "buy low, sell high" — it's a full accounting of what the spread has to pay for.

What breaks if you get this wrong: you treat every fill as a clean toll collection, you can't explain a losing day when the spread you charged looks perfectly reasonable, and you have no framework to tell whether a bad day was "the market moved" or "we got picked off" — two problems with opposite fixes.

---

#### 2. Simple Example

Quote ETH 3,000.00 bid / 3,000.60 ask. Fill on the bid (buy 1 ETH at 3,000.00), fill on the ask (sell 1 ETH at 3,000.60) — a completed round trip, $0.60 captured. That's the model working correctly: symmetric, instant, isolated.

Now the failure case: buy 1 ETH at 3,000.00, but the next fill on the ask doesn't come for 45 seconds — in that time fair value drifts to 2,999.70, and you finally sell at 3,000.10 (your ask, now repriced lower because the market moved). Spread capture on paper looks like $0.10, but you also ate a $0.30 markdown from holding through the drift. Net: −$0.20 on a trade that "should" have earned $0.60. Nothing exotic happened — the position was simply exposed to price risk for the 45 seconds it existed.

---

#### 3. How It Works (Simple → Sophisticated)

##### Basic approach — "spread is profit"

`PnL = spread × number of round trips`. Quote a $0.60 spread, complete 100 round trips a day, PnL = $60/day. Clean, and completely blind to time — it assumes the buy-fill and sell-fill happen at the same instant, at the same fair value, with no gap.

**What this still misses:** real fills don't happen simultaneously. You buy now, and the matching sell might come 4 seconds later or 4 minutes later. The basic model has no term for what happens to price *during that gap*.

##### Intermediate approach — spread minus inventory carry

`PnL = spread capture − inventory carry cost`, where carry cost = (holding time) × (adverse price drift while held). This explains the 45-second ETH example above: $0.10 nominal capture − $0.30 carry = −$0.20. A real improvement — but it treats the adverse move as symmetric random noise, like weather, with no reason to expect it to be biased against you specifically.

**What this still misses:** it can't explain why fills themselves aren't a random sample. In real markets, more buy-fills happen right before price *drops* than chance would predict — the counterparties trading against you are, on average, better informed than random noise. That's not carry risk; that's a structurally biased selection of *which* trades you get filled on.

##### Professional approach — the full identity

`PnL = spread capture − adverse selection − inventory carry cost − fees/infrastructure`

Four terms, each owning a distinct failure mode:
- **Spread capture** — the basic model's entire universe: gross toll per completed round trip.
- **Adverse selection** — the cost of *who* chooses to trade with you; fills are concentrated among informed counterparties, not randomly distributed (full mechanics: Level 6).
- **Inventory carry cost** — the cost of *when* your round trip completes; price can move against you purely from holding time, even against a perfectly neutral counterparty (full mechanics: Level 7).
- **Fees/infrastructure** — the toll on your own toll: exchange fees, plus the infrastructure cost of competing for fills at all.

**Why four separate terms, not one combined "risk" bucket?** They're driven by different things and need different defenses. Adverse selection is a counterparty-information problem — fixed by pricing and skewing against toxic flow. Inventory carry is a time-and-volatility problem — fixed by holding less, for less time, with tighter reservation pricing. Merge them and you can't tell whether a bad day was "the market moved" or "we got picked off" — and the fix for one can worsen the other (holding inventory longer to avoid a badly-timed exit reduces adverse-selection exposure but increases carry exposure — a real trade-off, invisible if the terms are merged).

**Sanity check at the edge case:** set adverse selection = 0 (every counterparty a random tourist), inventory carry = 0 (instant round trips), fees = 0. The formula collapses to `PnL = spread capture` — exactly the basic model. The professional model doesn't discard the basic one; it contains it as the special case where nothing goes wrong. That containment is the check that the formula is built correctly, not just plausible.

---

#### 4. Professional Standard (Jane Street / Citadel Level)

A senior MM trader doesn't ask "did we make money today?" — they ask "how much was spread capture, how much did adverse selection cost, how much did carry cost, what were fees?" — because each answer routes to a different team and a different fix (pricing model, risk limits, or infrastructure).

The other structural difference from retail intuition: **risk warehousing is priced continuously, not discovered at exit.** A retail mental model treats a position as "bought, now waiting to sell," with the P&L verdict arriving only when it's closed. An institutional desk marks every open position to market continuously — inventory carry is a running cost accruing every millisecond a position exists, and it feeds back into the *next* quote (the seed of the Avellaneda-Stoikov reservation price, Level 7). Adverse selection is handled the same way: not measured after the fact from realized markout, but estimated *predictively* per counterparty flow pattern, before the fill even happens, so quotes can skew in advance. The retail model is purely retrospective ("how'd we do?"); the professional model is predictive and defensive at every quote.

---

#### 5. Summary

| | |
|---|---|
| **What it is** | The MM business decomposed into four honest terms: `PnL = spread capture − adverse selection − inventory carry − fees`, not "buy low, sell high." |
| **Why it matters** | Every later level is a microscope on exactly one of these four terms — without this frame, nothing found later has anywhere to file. |
| **Professional standard** | Institutions track and defend each term separately and continuously (predictive, not retrospective) — never treat PnL as one undifferentiated number. |

---

#### 6. Structural View — The Three Pillars

A complementary lens on the same model: three interacting variables a quoting system optimizes continuously.

- **Fair value** — the internal estimate of what the asset should trade at right now (not the last traded price). Determines *where* to quote. If wrong, the MM gets picked off regardless of how well the other two pillars are tuned. (Full mechanics: Level 4.)
- **Spread** — the risk premium charged around fair value. Determines *how much* to charge for the four-term risk above. Widens with volatility and adverse-selection risk. (Full mechanics: Level 5.)
- **Inventory** — the position accumulated from imbalanced fills. Determines *how aggressively* to lean quotes back toward neutral (skew, size reduction, hedging). (Full mechanics: Level 7.)

Fair value determines where to quote, spread determines the premium, inventory determines the lean — and all three interact continuously under uncertainty. This is the architectural skeleton the rest of the roadmap fills in, level by level.

---

#### Sees vs Misses

| Model | What it sees | What it misses |
|---|---|---|
| Basic ("spread = profit") | Gross toll per completed round trip | Time exposure, counterparty information, fees — assumes instant, risk-free round trips |
| Intermediate (spread − carry) | Cost of holding time and price drift | Treats fills as a random sample; can't see that fills are biased toward informed counterparties |
| Professional (spread − adverse selection − carry − fees) | Full decomposition: gross revenue and three independently tracked, independently defended cost terms | Nothing structural at Level 0 — each term is shallow here and gets its own full mechanism later (adverse selection → L6, inventory → L7, spread/fee economics → L3/L5) |

---

### Level 1 — Market Structure

**Status: ✅ Taught 2026-07-24.**

#### 1. What It Is

Market structure is the actual machinery of *how* trading happens at a given venue — the matching algorithm, the order-type menu, the fee schedule, the price/quantity increments, the margin regime, the trading calendar. It's not a strategy choice; it's the physics every strategy has to operate inside, whether it accounts for that or not.

What breaks if you get it wrong: your strategy logic can be perfectly sound and still fail mechanically — an order gets rejected, rounds to a worse price than intended, silently pays a fee you didn't budget for, or behaves completely differently than it did on the venue you tested it on. Market structure bugs don't look like strategy bugs; they look like "the exchange is being weird," and they're invisible until you go looking for them.

---

#### 2. Simple Example

Two fruit stalls in the same town both sell apples, and a naive trader assumes "a market is a market" — buy where cheap, sell where pricier, done.

- **Stall A**: sells only by the full crate (a fixed lot size), closes at 5pm sharp every day, charges a flat $2 entry fee per visit regardless of how much you buy.
- **Stall B**: sells single apples (fine-grained sizing), open 24 hours, and actually pays *you* $0.05 per apple if you're the one who shows up first and offers to sell (a maker rebate, to attract sellers).

A trader who sees "Stall A apples are $1.00, Stall B apples are $1.10" and thinks "buy 10 loose apples at A, sell at B for a $1 profit" runs straight into two structural walls: Stall A won't sell 10 loose apples — only full crates (lot size mismatch), and if this idea occurs to them at 6pm, Stall A is already closed (session mismatch). The "price gap" they saw was real; the plan built on top of it was structurally impossible before a single trade happened.

---

#### 3. How It Works (Simple → Sophisticated)

##### Basic approach — "a market is a market, only price matters"

The naive model treats every venue as functionally identical: a single number (the price) is all that's needed to compare opportunities or place a strategy.

**What this still misses:** it assumes continuous matching (an order sent now, matched now) and price-time priority (first-come-first-served at a price level) everywhere — neither is universal. Some markets run periodic auctions instead of continuous matching (batch up orders, match once at a scheduled instant). Some derivatives markets use pro-rata matching instead of price-time — at the same price, size determines your share of the fill, not who arrived first, which means "queue position" as a concept doesn't even apply there. A strategy built assuming continuous price-time matching, dropped onto a pro-rata or auction venue, doesn't fail loudly — it just behaves nothing like intended.

##### Intermediate approach — "I'll account for the visible parameters"

This model checks the obvious mechanical facts before trading: tick size (round prices correctly), lot size (round quantities correctly), and the fee schedule (budget for it). A real improvement — it catches the Stall A crate problem.

**What this still misses:** the parameters that aren't a single visible number. Filters compose — a venue can enforce LOT_SIZE, MIN_NOTIONAL, and PRICE_FILTER *simultaneously*, and satisfying one says nothing about the others. Concretely: symbol XYZ requires quantity in multiples of 1 unit (LOT_SIZE ✓), order value ≥ $5 (MIN_NOTIONAL), and price within ±10% of last trade (PRICE_FILTER). An order for 0.001 XYZ at $2.00 = $0.002 notional satisfies LOT_SIZE trivially and PRICE_FILTER easily — but fails MIN_NOTIONAL by 2,500×. A trader who validates only against the filter they remember to check gets silently rejected, over and over, and the failure looks like nothing in particular — not "wrong price," not "wrong size," just rejected. The fix isn't checking harder against one filter; it's checking the *intersection* of all filters that apply, every time.

Beyond filters, the intermediate model also misses regime-level facts: whether margin is cross (all positions share one collateral pool) or isolated (each position's risk is walled off — losing one position can't cascade into liquidating another), and how the venue computes its mark price (an index blended from multiple external venues resists manipulation; a mark price sourced from thin local last-trade doesn't — the same nominal position can be safe on one venue's mark-price formula and liquidatable on another's).

##### Professional approach — market structure as a maintained specification

Institutions treat each venue's structure as a versioned specification sheet, not a set of facts memorized once: matching algorithm, full order-type menu (which of IOC/FOK/Post-Only/GTC it actually supports — not every venue supports every TIF), the complete filter set and how filters compose, the fee tier ladder (volume-based — your effective fee this month depends on last month's volume, not a static number), margin mode, mark-price formula, circuit-breaker/halt behavior, and self-trade-prevention mode.

**Why "maintained" and not "known"?** Because venues change these rules — fee tiers shift with volume, filters get updated, new order types roll out — without necessarily notifying every counterparty in a way that reaches your system automatically. A specification memorized once and hard-coded silently goes stale. Professional systems ingest venue limits continuously (auto-fetched, not hand-typed) and validate live orders against the current spec before sending — the intersection-of-all-filters check from above isn't a one-time audit, it's a standing gate every order passes through.

---

#### 4. Professional Standard (Jane Street / Citadel Level)

At institutional scale, market structure isn't background knowledge a trader keeps in their head — it's encoded as machine-readable configuration, auto-refreshed from the venue's own API, and treated as a first-class input the same way price is. A senior infrastructure engineer's mental model: "the venue's rulebook can change under me at any time, and my system has to notice before it sends an order, not after it gets rejected."

This is also where cross-venue operation gets structurally serious: running the same strategy on two exchanges means maintaining two (or more) separate specification sheets simultaneously, because nothing guarantees they match — different tick sizes, different fee ladders, different margin regimes, different matching algorithms for the *same* nominal instrument. Professional multi-venue systems don't assume parity; they explicitly model each venue's structure independently and only unify at the strategy-decision layer above it, never below.

---

#### 5. Summary

| | |
|---|---|
| **What it is** | The matching rules, order-type menu, fee schedule, and quantity/price constraints a venue enforces — the physics a strategy operates inside, not a strategy choice itself. |
| **Why it matters** | Structural mismatches fail silently and look nothing like strategy bugs — rejected orders, wrong-priced fills, or an unbudgeted fee, all traceable to a spec fact the system never checked. |
| **Professional standard** | Treat venue structure as continuously-ingested, versioned configuration validated before every order — never a memorized, one-time fact. |

---

#### 6. Re-anchoring Level 0 — Fees, With a Real Number

Level 0's PnL identity had a `fees` term that stayed abstract. Here it earns a number: on a $3,000 notional trade, a 0.05% taker fee costs $1.50; a 0.02% maker fee costs $0.60; a maker *rebate* of 0.01% at a high volume tier *pays you* $0.30. Same trade, same size, three different fee outcomes purely from market-structure facts (which side of maker/taker you land on, which fee tier you've earned) — a $1.80 swing on one trade that has nothing to do with your spread or your fair-value estimate. Run that gap across a few thousand trades a day and market structure alone — not strategy skill — can be the difference between the `fees` term being a rounding error or the dominant term in the PnL identity.

---

#### 7. Order Types in Depth — IOC, FOK, Post-Only/GTX

These three answer three different questions, and are easy to blur together. One shared order book makes the contrast concrete:

| Side | Price | Qty | Owner |
|---|---|---|---|
| Ask | 3000.70 | 5 ETH | Trader B |
| Ask | 3000.60 | 2 ETH | Trader A |
| *(spread)* | | | |
| Bid | 3000.00 | 3 ETH | Trader C |

**IOC — "grab what's there right now, forget the rest."** Executes immediately against whatever's available at your price or better; the quantity you couldn't fill instantly is cancelled, never left resting. Analogy: you want 5 apples at up to $1 each — the shop has 2 at that price, you buy the 2 and leave, no standing order for restock.

Example — **BUY, IOC, limit 3000.60, qty 5**: only the 2 ETH @ 3000.60 qualifies (3000.70 exceeds the limit). Fills 2 instantly; the remaining 3 are cancelled immediately, never rest. Partial fill, done in one instant.

**FOK — "all 5, right now, or none at all."** Same instant-or-cancel behavior as IOC, but no partial fills — either the full requested quantity fills immediately, or the whole order is killed with zero fill. Analogy: you need exactly 5 matching dining chairs right now — 2 is useless, so if the shop only has 2, you walk out with nothing.

Example A (fails) — **BUY, FOK, limit 3000.60, qty 5**: only 2 ETH available at or below the limit; can't fill the full 5 instantly → entire order killed, 0 filled. (IOC would have taken the 2. FOK refuses even that.)
Example B (succeeds) — **BUY, FOK, limit 3000.70, qty 5**: both levels now qualify (2 @ 3000.60 + 5 @ 3000.70 = 7 ≥ 5 needed) → executes 2 @ 3000.60 + 3 @ 3000.70 instantly; Trader B's remaining 2 @ 3000.70 stays in the book untouched.

**Post-Only / GTX — "I only ever want to be the one waiting, never the one grabbing."** A different axis entirely — not about fill quantity, but a maker-only guarantee checked *before acceptance*. If the order would match immediately against the opposite side (i.e., act like a taker), the exchange rejects it outright — doesn't reprice it, doesn't partial-fill it, just refuses it. Analogy: you're setting up a stall to sell apples at $1.20, planning to wait for a buyer — but if someone's already standing there offering $1.30, placing your $1.20 stall would mean instantly selling to them (you'd be the one grabbing an existing offer, not the one waiting). Post-only says: don't even let me set up the stall if that's what would happen.

Example A (accepted) — **SELL, Post-Only, price 3000.50**: best bid is 3000.00, so a sell at 3000.50 matches nothing resting → no immediate trade, order rests normally as the new best ask.
Example B (rejected) — **SELL, Post-Only, price 2999.50**: best bid (3000.00) is *higher* than this sell price → it would instantly match, taking liquidity → the exchange rejects the entire order at submission. Nothing fills, nothing rests.

IOC and FOK are about *your own aggressive orders* — used when you need to take (an emergency hedge leg, exit dispatch where certainty matters more than fee treatment). Post-Only is about *your resting quotes* — the mechanism that guarantees you stay a maker on every quote posted, which is literally how Level 0's "spread capture" term stays real rather than accidentally becoming a taker and paying the spread you meant to earn.

| | Rests in book? | Partial fill allowed? | What it guarantees |
|---|---|---|---|
| **IOC** | Never | Yes | Immediate execution of whatever's available, nothing left dangling |
| **FOK** | Never | No — all or nothing | Full-size execution or nothing; no partial exposure |
| **Post-Only / GTX** | Yes (if accepted) | N/A — it's about acceptance, not fill quantity | You are never the taker; crossing orders get rejected, not filled |

---

#### Sees vs Misses

| Model | What it sees | What it misses |
|---|---|---|
| Basic ("price is all that matters") | The quoted price on each venue | Matching algorithm differences (continuous vs auction vs pro-rata), meaning "queue position" and "instant fill" don't universally apply |
| Intermediate (checks visible params) | Tick size, lot size, a single fee number | Filter *composition* (must satisfy the intersection, not one filter), margin mode, mark-price formula, and that fee tiers move with volume |
| Professional (maintained spec sheet) | Full venue rulebook, auto-ingested and continuously validated, per venue independently in multi-venue setups | Nothing structural — the residual risk is operational (staying current as venues change rules), not conceptual |

---

### Level 2 — Limit Order Book

**Status: ✅ Taught 2026-07-24.** Interactive visual companion (same numbers as below):
https://claude.ai/code/artifact/6923c022-d95a-402a-b1d5-ffd1b1233ee2

#### 1. What It Is

The order book is the live stack of all resting bid and ask orders at a venue for one symbol — a record of *intent to trade*, not of trades. Everything a market maker decides — fair value, spread, sizing — is read off this one structure in real time, and it is read two ways at once: as **shape** (depth, imbalance) and as **flow** (the stream of adds, cancels, and trades changing it). Because nobody trades off raw exchange messages, the book you actually use is a *local replica* — and replicas can silently drift from reality, which makes book integrity an engineering discipline, not an assumption.

What breaks if you get it wrong: every downstream system reads from this instrument, so one corrupted or misread book poisons fair value, toxicity, queue estimates, and execution simultaneously — and the failure mode is never an error message, it's an unexplainable bad fill minutes later.

#### 2. Terminology (with visuals)

All examples use one book: best bid 3000.00, best ask 3000.60.

**Order book** — asks stacked above the spread, bids below; every row is waiting, none of it has traded:

```
         price      qty
  ask    3000.90    ████████ 8
  ask    3000.80    ████     4
  ask    3000.70    █████    5
  ask    3000.60    ██       2     ← best ask
         ────── spread $0.60 — no resting orders ──────
  bid    3000.00    ███      3     ← best bid
  bid    2999.90    ██████   6
  bid    2999.80    ████     4
```

**Price level** — a level is a *sum*, not a list: three traders each resting 1 ETH at 3000.60 appear as one row, `3000.60 : 3 ETH`. Who it belongs to is invisible at this granularity.

**L1 / L2 / L3 / L4 — the data-tier staircase** (four views of the same book):

```
  L1 (top only)      L2 (aggregated)       L3 (3000.60 exploded, arrival order)
     ?      ?        3000.90   8            #8841  1.0   10:00:00.001  ← fills 1st
     ?      ?        3000.80   4            #8842  1.0   10:00:00.418  ← fills 2nd
  3000.60   2        3000.70   5            #8907  1.0   10:00:01.250  ← fills last
  ─────────          3000.60   2
  3000.00   3        ─────────             L4 (explicit queue position — ~nobody publishes)
     ?      ?        3000.00   3            @3000.00: [ahead 12 ETH][YOU 2][behind 6]
     ?      ?        2999.90   6            "you are 4th — 12 ETH fills before you"
```

L1 = best bid/ask only. L2 = every level, quantity summed per price (what most venues publish). L3 = individual orders with identity and sequence (what makes true queue knowledge possible — many venues don't publish it). L4 = your exact queue position stated directly (essentially never published — must be estimated probabilistically from L2 + fill patterns).

**Depth of Market (DOM)** — the shape of L2 read as "how far does an order push price?":

```
  thin book:   3000.00 █ 1   2999.90 ██ 2   2999.80 █ 1   2999.70 ██ 2
               → sell 6 ETH eats four levels → price moves 4 ticks
  thick book:  3000.00 ████████████ 12   2999.90 ███████████████ 15  ...
               → same sell 6 ETH absorbed at first level → 0 ticks
```

**Book imbalance** — lopsidedness is information (full formula treatment as OFI at Level 6):

```
  bids ◀████████████████████ 40 ETH │ 8 ETH ████▶ asks
  bid share = 40 / (40+8) = 0.83 → book leans hard toward buyers
```

**Snapshot vs. incremental (delta) update** — one full picture at connect, then tiny edits applied to your local copy; miss one and the book is silently wrong:

```
  snapshot (once)   +   delta stream (continuous)
  full top-N book       u=4880  cancel 0.5 @ 3000.60   applied
                        u=4881  add    2.0 @ 3000.70   LOST — never seen
                        u=4882  add    1.0 @ 2999.90   applied
                        → local book now wrong at 3000.70, no error fired
```

**Aggregation (publishing boundary)** — the exchange's matching engine tracks every individual order internally (L3); publishing only L2 is a *choice*. The L2/L3 gap is a wall the venue built, not a fact of nature.

**Book depth (N-level sum)** — size questions are answered by cumulative sums, never single levels:

```
  3000.00   3    Σ 3
  2999.90   6    Σ 9
  2999.80   4    Σ 13   → "sell 20 ETH within 3 ticks?" 13 < 20 → NO (7 short)
```

**Slippage from depth consumption ("walking the book")** — an order bigger than the top level fills level by level; the average price is worse than the price on the screen:

```
  3000.70   5   ← 3 taken
  3000.60   2   ← 2 taken
  market BUY 5 → avg = (2×3000.60 + 3×3000.70)/5 = 3000.66
  slippage $0.06/ETH vs top-of-book — decided entirely by depth
```

**Phantom liquidity** — visible depth is intent, and intent can cancel faster than your order travels:

```
  t0 you look:      3000.60 │ 12 ETH offered — looks like plenty
  t1 in flight:     your IOC BUY 10 travelling (~10ms); 11 ETH cancels
  t2 arrives:       3000.60 │ 1 ETH → filled 1, other 9 die unfilled (IOC)
```

#### 3. Why the Naive Approach Fails

**The naive model:** "The book tells me the price. Best bid 3000.00, best ask 3000.60 — ETH is worth about 3000.30. Done."

**Analogy — the parking lot sign.** A garage displays "47 SPACES FREE." You drive in relaxed... and the spaces are on the roof, half are compact-only, and 30 are gone by the time you reach the ramp because the sign updates every five minutes. The sign was *true when printed* — but it was a summary of a changing situation, not a guarantee about your outcome. The order book is that sign at millisecond speed:

- **The book is intent, not commitment** — the 12 ETH offered can cancel during the milliseconds your order spends travelling (phantom liquidity above: looked at 12, filled 1).
- **The mid of a lopsided book is not the fair price** — 40 ETH on bids vs 8 on asks: simple mid says 3000.30, but that imbalance is pressure; true value is almost certainly higher. Naive mid-reading misprices exactly when it is most expensive.
- **A photo misses the movie** — two books can look identical right now while one just had 50 ETH of bids *added* and the other 50 ETH *cancelled*. Same photo, opposite futures.

#### 4. How It Works (Simple → Sophisticated)

##### Basic — read the top, compute the mid

`mid = (best_bid + best_ask) / 2` → (3000.00 + 3000.60)/2 = 3000.30. Genuinely useful — the least-biased instant summary, and all that L1 data offers. **What it misses:** everything behind the top. Thin and thick books can share an identical top-of-book while a 6 ETH sell moves one 4 ticks and the other 0 — same mid, radically different cost of trading.

##### Intermediate — read the whole shape: depth and imbalance

Sum depth within N ticks (Σ column above: 13 ETH within 3 ticks → a 20 ETH exit can't happen at acceptable cost, knowable *before* trying). And upgrade the mid with imbalance — the **weighted mid**:

```
weighted_mid = (bid_qty × ask_price + ask_qty × bid_price) / (bid_qty + ask_qty)
```

**Why cross-weighted?** Size on the bid is upward pressure — if 40 ETH wants to buy and 8 wants to sell, the next trade is far more likely to happen up at the ask. So each side's price is weighted by the *opposing* side's quantity: the side with more force drags the estimate toward the price it's pushing against.

Concrete: bid 3000.00 × 40, ask 3000.60 × 8 → (40×3000.60 + 8×3000.00)/48 = **3000.50**. Simple mid said 3000.30 — quoting an ask off 3000.30 means offering cheap to exactly the buyers about to push price up. (Doorstep of the *microprice* — full treatment at Level 4.)

Sanity check: balanced book (10 v 10) → 3000.30 = the simple mid. No imbalance, no adjustment — the formula contains the basic model as its special case.

**What it misses:** it's still a photo. No dynamics, and visible quantity taken at face value — 40 ETH of bids that would cancel at the first sign of trouble is not 40 ETH of support.

##### Professional — the book as a maintained, distrusted instrument

**Upgrade 1 — engineering: your book is a replica, and replicas drift.** The local book = one snapshot + every delta since, and the discipline is around *every*. Exchange deltas carry **sequence numbers**; the local book checks them. Getting update 4882 after 4880 means 4881 is gone — the book is now wrong somewhere, with no error message. Mechanical response: detect gap → declare the book dirty → stop trusting it (widen/hold quotes) → fresh snapshot → rebuild → resume. Not checking doesn't fail loudly; it fails as an unexplainable fill three minutes later.

Some venues add a second detector: the **checksum**. Periodically the exchange runs its true book's top levels through a fixed formula (e.g. CRC32 over "price:qty|price:qty|...") and sends the result; you run the same formula over your replica and compare. Sequence numbers catch *missed messages*; the checksum catches *any* divergence — including your own book-maintenance bugs, where every message arrived but one was mis-applied. Neither says *where* the error is, only *that* one exists — and that's enough, because the response is identical: rebuild.

| | Sequence number | Checksum |
|---|---|---|
| Catches | A message that never arrived / arrived out of order | Any divergence, any cause — including your own bugs |
| Fires | The instant the gap happens | At the next periodic check |
| Analogy | Numbered pages of a letter | Comparing letter-count totals of two recipe copies |
| Can't do | Catch corruption when messages arrived but were mis-applied | Say where the error is |

**Upgrade 2 — reading: flow, not just state.** The book only ever changes via three event types — **add**, **cancel**, **trade** — and the stream of them is its own signal. Same-shape books, different recent flow: heavy adds on the bid = confidence arriving; heavy cancels = confidence fleeing; heavy trades eating the ask = aggressive buying. The 40-ETH bid wall built by adds over ten minutes that held through two sell-offs is support; the same wall that appeared 400ms ago from serial cancellers is decoration. Identical photo, opposite conclusions — recoverable only from the movie. (Raw material for OFI at Level 6 and queue mechanics at Level 8.)

Binding discipline: **visible liquidity is conditional liquidity** — size plans against what the book has historically *delivered* at that depth, never what it currently shows.

#### 5. Why Should You Believe This? — One Fill, Read Three Ways

Same moment: the 40-vs-8 book, and your resting ask at 3000.60 just got hit — you sold 1 ETH.

- **Basic reader:** "Sold at 3000.60, mid 3000.30 — captured $0.30 of half-spread. Great fill."
- **Intermediate reader:** "Weighted mid was 3000.50 — real edge was $0.10, not $0.30." Same fill, one-third the edge — and that's the difference between a strategy that looks profitable and one that is.
- **Professional reader:** "Weighted mid 3000.50, *and* the event stream shows the ask side eaten by trades for 900ms while the bid side grows by adds — this buyer is part of a wave. My $0.10 is about to be negative. Reprice *now*, not after the next fill."

One fill, three readings, three actions. The naive reader felt richest and was most wrong — and every difference came purely from how much of the book each could see and trust. Misreading the book converts directly into adverse selection (Level 0's second term, now with a mechanism attached).

#### 6. Professional Standard (Jane Street / Citadel Level)

The book is treated as a **sensor requiring calibration and health-monitoring**, not a data field:

- **Integrity verified, not assumed** — sequence-gap detection on every message; checksum re-computation where the venue offers it. A dirty book means quoting defensively or not at all — no decision may read a known-broken instrument.
- **Latency of book knowledge measured** — the local book is always slightly stale; institutions measure that staleness continuously, because a 10ms-old book in a fast market is a different instrument than in a quiet one (heart of Level 9).
- **The book feeds everything** — fair value reads its shape, adverse-selection signals read its flow, queue estimates read trades-vs-cancels, execution reads depth. One corrupted book poisons all downstream systems at once — which is why integrity discipline is absolute.
- **Own-impact awareness** — a market maker's quotes are *in* the book it reads. Institutions separate "the book" from "the book minus us," or the engine ends up reading its own resting size as market support — a quiet feedback loop of self-reassurance.

#### 7. Summary

| | |
|---|---|
| **What it is** | The live, aggregated stack of resting intent — read as shape (depth, imbalance) *and* flow (adds/cancels/trades) — maintained locally as a replica that can silently drift. |
| **Why it matters** | Every downstream system reads this one instrument; misreading it becomes adverse selection, and a corrupted replica poisons everything at once. |
| **Professional standard** | Sequence-verified, checksum-validated, staleness-measured local book; visible liquidity treated as conditional; flow read as a first-class signal beside state. |

#### Sees vs Misses

| Reading | What it sees | What it misses |
|---|---|---|
| Basic (top-of-book mid) | Instant price summary, the spread | Depth behind the top — can't price the cost of any real size |
| Intermediate (depth + weighted mid) | What size costs (Σ within N ticks), which way the book leans | Dynamics — same shape, opposite meanings depending on flow; takes visible size at face value |
| Professional (maintained replica + flow) | Book integrity (sequence/checksum), event-stream pressure, own-quote separation, staleness | Nothing structural — what remains is *interpreting* the signals (fair value L4, toxicity L6, queue L8) |

---

### Level 3 — Maker Economics

**Status: ✅ Taught 2026-07-24.** (Supersedes the interim "Expected Value Per Fill Framework" moved from Foundation — its content is absorbed and deepened below.)

#### 1. What It Is

Level 0 gave the business identity; Level 3 zooms all the way into a **single maker fill** and prices every part of it. The unit economics of one fill — what it captures, what it costs conditional on having happened, and what a resting quote is worth *before* anyone fills it — is the number the entire business multiplies from: daily PnL ≈ fills_per_day × EV_per_fill, and turnover is merciless in both directions.

What breaks if you get it wrong: quoted-spread accounting books storm losses as profit, greenlights scaling a strategy whose worst segment loses money per fill, and hides a bleeding ask side behind a profitable bid side. The wrong ledger doesn't just mismeasure — it points business decisions in the wrong direction.

#### 2. Terminology essentials

- **Entry edge** — earned at fill instant, measured against fair value *at fill time* (FV 3000.30, ask fills 3000.60 → $0.30; if FV had drifted to 3000.50, same fill earns $0.10). Never against the quote's original intent.
- **Per-fill accounting** — each fill booked individually against FV, per side. Round trips complete unpredictably or never (inventory gets hedged or carried); aggregates hide which side bleeds.
- **Markout** — the truth serum: FV drift at 100ms/500ms/1s/5s after each fill. Entry edge is what you think you earned; markout is what you kept.
- **P(fill)** — probability a resting quote fills within a horizon (touch ≈ 40%/min, 3 ticks deep ≈ 8%). Every edge gets multiplied by it.
- **E[adverse | fill]** — average FV move against you *conditional on being filled*. Unconditional drift $0.02; conditional on your ask being hit, $0.18 — 9×, because fills are a biased sample.
- **Breakeven half-spread** = E[adverse|fill] + costs. Below it, every fill feels like revenue and is a loss.
- **Realized vs quoted spread** — quoted $0.60; after post-fill drift you keep maybe $0.24. The gap *is* adverse selection in spread units.
- **gpnl vs npnl** — gross (price + spread only) vs net (after fees). Strategy must be gpnl-positive first; fees are a deployment question (venue, tier), never a pricing input.
- **Inventory cost per fill** — each fill hands you inventory (~$0.03/fill at 45s typical hold). Level 7 owns the machinery.

#### 3. Why the Naive Approach Fails

**The naive model:** "I quote a $0.60 spread; every round trip earns $0.60; more fills, more money."

**Analogy — the umbrella shop.** Buy umbrellas at $10, sell at $12: "$2 margin, guaranteed by arithmetic." But watch *when* they sell: sunny days, nobody buys. The moment a storm warning hits, the shop sells out in an hour — and an hour later wholesale is $15, because every supplier saw the same storm. He "earned $2" per umbrella on stock now costing $15 to replace: a $1 loss each, booked as profit by his margin math.

The error, precisely: **his sales are not a random sample of days — they cluster exactly on the days his prices are about to be wrong.** Customers didn't cheat; they responded to information faster than his price tags. Posted margin real, realized margin negative — and "sell more umbrellas" deepens the loss. That's a maker fill: posted margin = quoted half-spread, storm = informed flow, wholesale jump = post-fill adverse move. Maker economics computes what a fill is worth *given that it happened* — the happening itself is information.

#### 4. How It Works (Simple → Sophisticated)

##### Basic — quoted-spread accounting

`PnL = fills × quoted_half_spread` → 400 × $0.30 = "$120/day." Not insane — if counterparties were random tourists it would be exactly right. Its single hidden assumption: fills arrive independently of whether the price is about to be wrong. **Misses:** the conditioning; it can't tell a fill that kept its edge from the first tick of a storm.

##### Intermediate — condition on the fill, measure with markout

```
EV_per_fill = entry_edge − E[adverse | fill]
```

The adverse term is conditional because of who chooses to trade: unconditional 5s drift $0.02, conditional-on-your-ask-being-hit $0.18 — the fill moments are enriched with informed moments. Measure it by averaging markout over your own fills. Concretely: $0.30 − $0.18 = **+$0.12/fill** → 400 fills = $48/day, not $120. The other $72 was quoted-minus-realized — adverse selection in dollars. Breakeven falls out: any quote capturing < $0.18 donates money. **Misses:** it's post-hoc (no P(fill) — can't price a *placement*), and it blends one constant across market states that differ 11×.

##### Professional — decision-time EV, per quote, per state

```
EV(quote at depth d) = P(fill at d) × ( capture(d) − P(adverse|fill) × severity )
                       + inventory_effect
```

- **P(fill) multiplies everything** — uncollected edge is worth zero. P(fill) falls with depth while capture rises: the best quote is the argmax of the product, computable, not intuitable.
- **Frequency × severity split** — calm: 20% × $0.15 = $0.03; storm: 60% × $0.55 = $0.33 — 11× swing under an identical quoted spread. A blended $0.18 is wrong in both states: too timid in calm, too brave in storm. They also have different defenses (frequency → who you stand near; severity → how deep you stand).
- **Inventory term** — a fill that reduces your position is worth more than its capture alone (Level 7).
- **Sanity check:** P(adverse|fill)=0, inventory flat → EV = P(fill) × capture — the naive ledger survives as the special case where nobody knows anything. (Same containment signature as Level 0's identity and Level 2's weighted mid.)

Discipline pair: **per-fill, per-side booking** (the unit of analysis is one fill on one side), and **gpnl first** — fees ($0.60/fill at 0.02% on $3,000 notional — 2× our entry edge!) decide *where* to deploy, never *how* to quote.

#### 5. Why Should You Believe This? — The Same Day, Three Ledgers

400 fills, quoted half-spread $0.30. Underneath: 340 calm fills (adverse $0.05) + 60 storm fills (adverse $0.60).

| Ledger | Computation | Verdict |
|---|---|---|
| Basic (quoted) | 400 × $0.30 | **+$120** — "great day" |
| Intermediate (blended markout $0.1325) | 400 × $0.1675 | **+$67** — "decent day" |
| Professional (state-split) | 340×($0.30−$0.05) + 60×($0.30−$0.60) | **+$85 − $18 = +$67** — calm earned $85, storm **lost $18** |

Intermediate and professional agree on the total; the split changes *what you do next*. Blended: "average fill earns $0.17, quote more." Split: **15% of fills destroy 21% of gross capture** — fix is state-conditional pricing (charge $0.30 in calm, ≥$0.60 in storm or quote deeper), an instruction a blended number literally cannot express. And the basic ledger's $120-vs-truth-$67 would greenlight scaling the losing segment. Wrong ledgers don't mismeasure — they mis-decide.

#### 6. Professional Standard (Jane Street / Citadel Level)

- **Markout curves computed continuously, segmented ruthlessly** — by side, symbol, depth-at-fill, state, counterparty class. The question is never "average markout" but "*which segment* is deteriorating" — averages bury the next loss.
- **EV computed at decision time, per quote cycle** — on live estimates, before every placement. The storm surcharge arrives before the storm fills, not in the post-mortem.
- **Every input is a living, decaying estimate** — P(fill), P(adverse|fill), severity maintained EWMA-style and validated against realized markout in a feedback loop. A constant in this formula is a bug waiting for a regime change.
- **The per-segment EV sign gates everything upstream** — size, symbol selection, venue allocation. Negative-EV segments get repriced or exited, because turnover converts per-fill sign into monthly P&L direction with mechanical certainty.

#### 7. Summary

| | |
|---|---|
| **What it is** | The unit economics of one maker fill: EV = P(fill) × (capture − P(adverse\|fill) × severity) + inventory effect — per fill, per side, against FV, with markout as truth serum. |
| **Why it matters** | Turnover multiplies the per-fill EV sign into monthly P&L; a wrong ledger reports profit while the strategy bleeds and scales the losing segment. |
| **Professional standard** | Decision-time EV on live state-conditional estimates; ruthlessly segmented markout; gpnl-first with fees as deployment. |

#### Sees vs Misses

| Ledger | What it sees | What it misses |
|---|---|---|
| Basic (quoted × fills) | Gross capture at quote prices | Fills cluster on moments prices are about to be wrong — books storm losses as profit |
| Intermediate (markout, blended) | True average EV; realized-vs-quoted gap; breakeven floor | No P(fill) (can't price placement); state variation — can't express "reprice the storm segment" |
| Professional (decision-time, state-split) | Depth-vs-P(fill) optimization; frequency × severity; per-segment signs gating decisions | Nothing structural — the estimation of each input is the remaining problem: P(fill) → L8, adverse prediction → L6, fair value → L4 |

---

### Level 4 — Fair Value

**Status: ✅ Taught 2026-07-31.** (Supersedes the interim "Fair Value Estimation Mechanics" moved from Foundation — its content is absorbed and deepened below.)

#### 1. What It Is

A market maker sells **immediacy** at prices centered on an **opinion**. Levels 0–3 priced the immediacy (spread, EV, adverse selection); this level builds the opinion: **fair value (FV)** — the internal, private, continuously-recomputed estimate of what the asset is worth *right now*. Not the last trade, not any single visible price: a number that exists only inside the engine, built from observable references plus adjustments.

Everything hangs off it. Level 3's EV formula — `EV = P(fill,d) × (capture − P(adverse|fill) × severity)` — measures capture and adverse **relative to FV**; if FV is wrong, every term is silently wrong too. And the brutal asymmetry: **the spread only protects against people who know *less* than your FV implies. Against anyone with a better opinion, your spread is a discount coupon.** Adverse selection is mostly just FV error, monetized by someone else.

Distinction pros keep sharp: a **reference price** is something observable you anchor to (mid, index, another venue). **FV is your opinion, built FROM references plus adjustments.** Quoting straight off a reference with no adjustment means everyone with a better opinion trades against you.

#### 2. Terminology essentials

- **Fair value (FV)** — the engine's private estimate of true worth right now. Last trade printed 3000.20 (a 0.01-lot sell into a thin bid); model says 3000.45 → quote around 3000.45, treat the print as noise.
- **Mid price** — `(best bid + best ask)/2`. Bid 3000.00, ask 3000.60 → 3000.30. Size-blind: a 40-lot bid vs a 0.5-lot ask produces the same mid as a balanced book.
- **Weighted mid** — `(bid_qty×ask_px + ask_qty×bid_px)/(bid_qty+ask_qty)`. Same book with 40×bid, 8×ask → 3000.50: shifts FV **toward the heavy side's opposite price** (heavy bid = buyers pressing = true price nearer the ask).
- **Microprice** — the weighted mid with the assumption removed: defined as **E[mid a moment from now | current book]** (Stoikov), with imbalance→drift weights **calibrated from this asset's data**, not assumed. On BTC an 80/20 imbalance might predict +0.15 spreads of drift; on a thin alt, +0.45.
- **Book imbalance (OBI)** — `bid_qty/(bid_qty+ask_qty)`, top-of-book or top-N. 40 vs 8 → 0.83. The most-studied short-horizon predictor in microstructure: high OBI → next tick more likely up.
- **Trade-flow adjustment** — the book is *stated* intent (cancellable, spoofable); a trade is *committed* intent (taker fees paid). Recent aggressive flow nudges FV in its direction. (Full machinery — OFI, VPIN — at Level 6.)
- **Lead-lag / leader venue** — price discovery concentrates; the leader's price is a preview of the follower's near future (typically 50–300ms). Quoting on a follower without watching the leader = volunteering as exit liquidity.
- **Basis / funding** — a perp's FV ≠ spot: funding sustains a premium (**basis**). Spot 3000.00, funding holds perp ~0.02% rich → perp FV ≈ 3000.60. Anchoring to raw spot is a systematic 0.60 error.
- **Staleness vs noise** — the update-speed dial: too slow → picked off; too twitchy → chase noise, burn queue position. Smoothing buys noise-immunity at the price of lag.

#### 3. Why the Naive Approach Fails

**The naive model:** "Fair value = the market price. Use the mid (or last trade) and center quotes on it."

**Analogy — the used-car dealer.** A dealer quotes buy and sell prices on a car whose true price is posted nowhere. How does he decide it's worth $30,000? *Last auction print?* Might have been a rusted unit or a desperate seller. *Average of buyer offers and seller asks?* That's the mid — but 40 buyers lined up outside vs 2 sellers means the average is already stale. *The big-city auction house?* If prices there jumped 5 minutes ago, quote off the old local price and flippers buy his whole lot and truck it to the city. *Are people actually paying, or just haggling?* Ten who paid asking price today beat fifty who are "interested."

Every professional FV pipeline is these four instincts — imbalance, lead-lag, committed flow, better references — made numerical and fast. The naive model has none of them: it treats one stale, size-blind, single-venue reference as an opinion. **Misses:** everything that predicts the next move; it describes where the market *was*.

#### 4. How It Works (Simple → Sophisticated)

##### The estimator ladder — one book, three answers

ETH-perp, top of book: **bid 3000.00 × 40, ask 3000.60 × 8**

```
                 3000.00×40                    3000.60×8
  BID  ████████████████████████████████│██████  ASK
                                       │
        mid            3000.30 ────────┤   size-blind average
        weighted mid   3000.50 ────────┤   leans toward heavy side's
                                       │   opposite price (assumed weights)
        microprice     3000.30–3000.55 ┤   E[next mid | book], weights
                                       │   CALIBRATED per asset from data
```

- **Rung 1 — Mid (3000.30):** an average of *now*, when what's needed is an estimate of *next*. Reads this lopsided book exactly like a balanced one.
- **Rung 2 — Weighted mid (3000.50):** encodes "buy pressure → price about to rise." Quoting the ask around 3000.50 instead of 3000.30 stops selling 0.20 cheap to exactly the people about to push price up. But it *assumes* imbalance maps linearly, at full strength, identically on every asset.
- **Rung 3 — Microprice:** **measures** it — "when OBI = 0.83 on this asset, where is the mid 1s later, on average?" A forecast, not a fancier average. The level's core idea: **fair value is a prediction problem, not an averaging problem.**

##### Layer 2 — Flow: the book can lie, trades can't

Same book, but the last 2s printed 15 aggressive buys vs 2 aggressive sells → FV leans up *even if the book looked balanced* — takers vote with money. Simple form: `FV = microprice + k × flow_imbalance` over a short window, `k` calibrated like the microprice weights. **State says where the market rests; flow says where it's going. FV needs both.**

##### Layer 3 — The leader venue: someone else's present is your future

Binance ETH jumps 3000.30 → 3001.10; the follower venue's book hasn't moved; your ask rests at 3000.60. For ~100ms anyone watching both venues buys it and instantly holds 3001.10 — +0.50 for them, −0.50 markout for you, and (Level 3's 9× conditioning) these are exactly the fills you *do* get. Arbitrageurs run this as a full-time job. The fix is architectural: **subscribe to the leader; blend follower book with leader price, weighted by measured lead-lag** (which drifts — it too is calibrated, not assumed).

##### Layer 4 — Basis: a perp's fair value is not spot

Funding tethers perp to spot without equalizing them. Perp held ~0.02% rich → FV = spot + 0.60. Skip this and you're *systematically* 0.60 low: ask looks cheap all day, bid never fills, and the one-sidedness looks like bad luck when it's a forgotten constant. Basis moves slowly (minutes–hours) — a slow anchor under the fast layers, but skipping it makes every fast layer precisely wrong.

##### Layer 5 — The dial: staleness vs noise

The raw FV signal ticks ~10×/s and is jittery. Two bad extremes:

- **Follow it raw** → cancel/replace on every flicker, lose queue position each time (Level 8 preview: queue position is an asset bought by waiting), pay message costs, get whipsawed by noise that mean-reverts before filling.
- **Smooth it hard** (long EMA) → calm quotes, but FV lags ~400ms behind the real move — Layer 3's pick-off, self-inflicted.

Standard resolution: **smooth the quote anchor, plus a fast-path override** — if raw FV gaps beyond a threshold (leader-venue jump, sweep), bypass the smoothing and reprice *now*. Small moves → patience wins; big moves → speed wins. Set per asset, revisited as regimes change.

#### 5. Why Should You Believe This? — How FV Error Shows Up in Money

FV error is almost never observed directly — only its symptoms, all Level 3 instruments:

| Symptom | Diagnosis |
|---|---|
| Persistent one-sided fills (all buys fill, sells never) | FV sits below the market's — cheapest ask in town. Random flow fills both sides; **biased fills mean biased FV.** |
| Systematically negative markouts on one side | FV updating too slowly (staleness) or missing a layer entirely (leader venue, basis). |
| One-sidedness that never mean-reverts, constant size | A *constant* error — the basis-layer signature (a forgotten 0.60 looks like permanent bad luck). |

The professional loop: **quote → fill → markout → attribute the loss to a layer → recalibrate that layer.** FV is never "done" — it's a model under continuous audit by your own fill tape. And the containment check (Level 0/2/3 signature): balanced book + no flow + no leader move + zero basis → every layer's adjustment is 0 and FV collapses to the mid — the naive model survives as the special case where nothing is happening.

#### 6. Professional Standard (Jane Street / Citadel Level)

- **FV is a per-asset calibrated forecast, not a formula with defaults** — imbalance→drift weights, flow coefficients, and lead-lag times are fitted from each asset's own tape and refitted as they drift. A constant weight in the FV pipeline is a bug waiting for a regime change.
- **Multi-venue by construction** — the leader venue's feed is a first-class FV input for every follower venue quoted; who leads is itself measured, not assumed.
- **All slow anchors priced in** — basis, funding expectations, index composition: the systematic constants are removed so the fast layers fight only genuine noise.
- **The dial is engineered, not defaulted** — smoothed anchor + gap-triggered fast-path repricing; re-quote suppression below meaningful moves to preserve queue position; per-asset settings.
- **FV audited by its own fills** — markout curves segmented by side/venue/state, one-sided-fill monitors, and losses attributed back to the specific layer that mispriced.

#### 7. Summary

| | |
|---|---|
| **What it is** | The engine's private, continuously-recomputed opinion of true worth: calibrated microprice + flow + leader venue + basis, smoothed with a fast-path override. |
| **Why it matters** | Every EV term is measured relative to FV; adverse selection is mostly FV error monetized by someone else. The spread is a moat — FV decides where the castle is. |
| **Professional standard** | Prediction not averaging: per-asset calibrated weights, leader-venue blend, slow anchors removed, engineered staleness/noise dial, audited by markout. |

#### Sees vs Misses

| Estimator | What it sees | What it misses |
|---|---|---|
| Last trade / mid | Where the market was; a symmetric reference | Size, imbalance, flow, other venues, basis — everything predictive |
| Weighted mid | Top-of-book pressure direction | Assumes the imbalance→drift mapping instead of measuring it; single venue; no flow |
| Microprice + flow | Calibrated short-horizon forecast from state + committed intent | The leader venue's preview; slow anchors (basis/funding) |
| Full pipeline (+ leader, + basis, + dial) | All of the above, with noise-immunity and a fast path | Nothing structural — the remaining work is estimation quality: adverse prediction → L6, queue value → L8, latency floor → L9 |

---

### Level 5 — Spread Design

**Status: ✅ Taught 2026-08-02.**

#### 1. What It Is

Level 4 built the anchor; Level 5 builds the **distance from it** — per side, per moment. Thesis: **the spread is a price, not a setting.** It's the price charged for immediacy, built up from costs plus margin, optimized against demand (fill rate), and repriced when inputs move. Desks that treat it as a tunable constant ("we quote 2 ticks") are selling a product without ever computing its cost of goods.

#### 2. Terminology essentials

- **Half-spread (δ)** — distance from FV to *one* quote; pros think per-side because the two sides will usually differ. FV 3000.45, ask 3000.75 → δ_a = $0.30.
- **Spread decomposition** — `δ = adverse-selection cost + inventory-risk premium + ops costs + margin`. Each component moves independently, on its own clock.
- **Breakeven floor** — the cost components with margin = 0. Below it every fill is a donation. A *floor*, not a target — and state-dependent (calm ≈ $0.13, storm ≈ $0.68 in the running example).
- **Reservation price (r)** — the quote center, which is NOT FV once you hold inventory: *the price at which I'm indifferent, given what I already hold.* Long → r below FV; short → r above.
- **Skew** — what the shifted center looks like from the quotes: one quote friendlier, one harsher. **Discount the exit door, tax the entrance.** Long 5 lots, FV 3000.45, center 3000.35 → ask $0.20 from FV (attractive → inventory shrinks), bid $0.40 (rare, and paid extra when it fills). Both sides always stay quoted.
- **Inventory-risk premium** — holding costs even without adverse selection: σ√t risk over expected holding time (σ=$2/min held 45s ≈ $1.75 warehoused per lot).
- **Avellaneda–Stoikov (A-S, 2008)** — the canonical framework: from FV, inventory q, risk aversion γ, volatility σ, and fill-decay k, it *derives* r = FV − q·γ·σ²·T and the optimal width. Its lesson: **spread and skew are outputs of one optimization, not style choices.**
- **γ / k / T** — the A-S knobs: γ = how much I hate holding risk; k = how fast P(fill) dies with distance from the touch (the demand curve of the immediacy shop); T = how long I'm stuck holding what a fill gives me.
- **Fill-rate/width tradeoff** — widening raises capture per fill and kills P(fill); the optimum is an interior argmax of the product, not a maximum of either.
- **Widen vs pull** — hostile-conditions menu, in order: skew → widen → size-damp → post deeper. Pulling quotes is the retail reflex and the anti-pattern.
- **Dynamic spread** — every input is a living estimate; a static spread is wrong in both directions within the hour.

#### 3. Why the Naive Approach Fails

**The naive model:** "Pick a spread that feels safe — say 2 ticks — and quote it symmetrically, always."

**Analogy — the insurance premium.** An insurer prices a policy as expected claims + capital cost for warehoused risk + operating cost + margin. Underprice → every policy loses money with certainty at scale. Overprice → healthy customers leave and the ones who stay are exactly the sick ones — adverse selection *worsening* as you misprice. A quote is a policy insuring the counterparty against having to wait; the claim event is the price moving against you after the fill. Same components, same failure modes.

The static-spread desk fails all of it at once: no floor computation (can't tell if 2 ticks even covers E[adverse|fill]), no state-dependence (one premium for sunny days and hurricanes), no inventory tilt (keeps buying while long), no demand curve (never asks what width maximizes revenue per minute). **Misses:** everything — it isn't pricing, it's a habit.

#### 4. How It Works (Simple → Sophisticated)

##### Step 1 — Decompose: what a half-spread must pay for

Running scenario: FV = 3000.45, σ = $2/min, expected hold 45s, E[adverse|fill] = $0.18 (Level 3's conditional number), fees deferred (gpnl-first).

```
δ  =  adverse selection  +  inventory risk   +  ops costs  +  margin
      $0.18 (E[adv|fill])   ~$0.07 (σ√t)        ~$0.01        what's left
      ────────────────────────────────────────────────────
      breakeven floor ≈ $0.26  →  quote δ ≈ $0.30 → ~$0.04/fill margin
```

Three consequences: (1) the floor is **state-dependent** — calm E[adv|fill] $0.05 → floor $0.13; storm $0.60 → floor $0.68; one number is wrong in every state. (2) Components move on **different clocks** — adverse in seconds, inventory risk in minutes, ops never — so repricing needs fast components on fast inputs. (3) **Margin is what's left, not what's aimed** — if competitors quote below your floor, the answer is deeper/smaller/skewed, never "match them" and never absent.

##### Step 2 — Center: the reservation price

Flat → center on FV. Long 5 lots → each buy adds risk, each sell removes it → the indifference point sits below FV: **r = FV − q·γ·σ²·T** — *shift = (how much I hold) × (how much I hate risk) × (how dangerous it is) × (how long I'll hold it).*

```
     bid 3000.05           r = 3000.35    FV = 3000.45      ask 3000.65
          │◄── $0.40 from FV ──┤              │◄── $0.20 ──►│
            discount the exit door · tax the entrance
```

The elegance: skew isn't a bolt-on mechanism — it's what *symmetric quoting around the honest center* looks like once the center accounts for inventory. A-S's second output, width `δ* = γσ²T/2 + (1/γ)·ln(1+γ/k)`, prices inventory risk and the fill-rate tradeoff in one expression: **center and width are both outputs of one optimization — not two independent knobs.**

##### Step 3 — Width: the argmax, not the maximum

| δ from FV | capture/fill | P(fill)/min | rev/min | EV/min (adverse $0.18) |
|---|---|---|---|---|
| $0.20 | $0.20 | 55% | $0.110 | **+$0.011** |
| $0.30 | $0.30 | 40% | $0.120 | **+$0.048** |
| $0.45 | $0.45 | 15% | $0.0675 | **+$0.041** |
| $0.60 | $0.60 | 6% | $0.036 | **+$0.025** |

Tight ($0.20, below the $0.26 floor): maximum activity, $0.011/min — busy and broke. Wide ($0.60, "safe"): $0.42 kept per fill, starving — $0.025/min. The optimum is interior (~$0.30), found by search over the product, and it *moves* when P(fill,d) or E[adverse|fill] moves. "Wider is safer" is true per fill and false per minute.

##### Step 4 — The defense ladder

Storm: E[adverse|fill] → $0.60, floor jumps past current width. Escalation order — every step stays in the book:

1. **Skew** — trouble is directional → slide r; discount the exit, tax the entrance.
2. **Widen** — the floor rose → δ follows it. Fewer fills is the point: the ones you get are paid enough. Every tick of widening should have a justification — the floor computation *is* the justification.
3. **Size-damp** — cut quoted size so a sweep through the taxed side hits 0.3 lots, not 2. Width prices *each* fill; size caps the *sum*. Size→small is allowed; size→0 is a pull.
4. **Post deeper** — further from the touch: P(fill) falls most for informed sweeps, and you build queue position (Level 8).

**Not on the menu: pulling quotes.** It forfeits revenue, dumps queue position (an asset paid for by waiting), and blinds measurement — no fills → no markouts → estimates go stale exactly when the regime changes fastest. Decisively: *there is always a width at which quoting is +EV* — hostile conditions change the price of immediacy, not the presence. The pull reflex usually means the desk has no working floor computation: it can't price the storm, so it flees it.

Skew's boundary (documented anti-pattern): defensive skew *repricess* both doors (tax the endangered side, discount the exit; drift capture is a bonus riding on the reprice). The offensive one-sided lean — "trend is down, quote only asks" — *removes* a door, converting the book into a naked momentum bet paid maker-style. Verified loss pattern; the distinction is reprice vs remove.

##### Step 5 — Dynamic by construction

Per quote cycle: FV (L4) → live E[adverse|fill], σ, q → per-side floor → r → δ per side via the argmax → place/keep through the re-quote dial (L4), so sub-noise repricing doesn't churn queue position. Every input is a living estimate; a static number anywhere in the chain is a bug waiting for a regime change.

#### 5. Why Should You Believe This? — The Symmetric-Widening Trap

Toxicity spikes, concentrated on the bid side (aggressive selling). A desk that widens **both** sides $0.30 → $0.80 "for safety": fills collapse (6%/min territory and below), revenue ≈ 0, measurement goes dark, and the barely-endangered ask was repriced out of the book for nothing. The precise response — skew (tax the bid, discount the ask) + size-damp on the bid — keeps revenue flowing on the safe side, keeps markouts flowing on both, caps the damage a sweep can do, and holds queue position. Blunt symmetric fear pays for "safety" twice: in revenue and in blindness. The containment check, as always: flat inventory + calm state + no signals → r = FV, δ_bid = δ_ask = calm floor + margin — the naive symmetric fixed spread survives as the special case where nothing is happening.

#### 6. Professional Standard (Jane Street / Citadel Level)

- **Spread as computed price** — decomposed components, each estimated live on its own clock; the floor recomputed per side per cycle; margin read as the residual, not assumed.
- **A-S descendants everywhere** — center and width derived from one optimization; skew emerges from the honest center rather than a hand-tuned tilt.
- **Constants that would notice reality changing** — γ backed out from capital limits, k fitted from own quote outcomes (fill rate by depth bucket), T measured from actual holding times, per asset. The test for any number in the pipeline: *if reality changed, would this number notice?*
- **The full defense ladder, no pull rung** — skew / widen / size-damp / post-deeper, each continuous; quote-absence mechanisms deleted, not merely discouraged.
- **Per-minute accounting** — width evaluated by EV per unit time (the argmax), never per-fill safety.

#### 7. Summary

| | |
|---|---|
| **What it is** | Pricing the distance from FV per side: decomposed floor + A-S center (reservation price) + width from the fill-rate argmax + the skew/widen/size-damp/post-deeper ladder. |
| **Why it matters** | The spread is the product's price tag: below the floor every fill donates; past the argmax the shop starves; symmetric when it shouldn't be, it accumulates inventory into the move. |
| **Professional standard** | Spread as computed, state-conditional price; constants measured per asset; defense that repricess and never absents. |

#### Sees vs Misses

| Approach | What it sees | What it misses |
|---|---|---|
| Static symmetric spread | Simplicity; survives only calm | No floor, no states, no tilt, no demand curve — a habit, not a price |
| Decomposed floor + widen-on-fear | Cost coverage per fill | Per-minute revenue (argmax); directionality (skew); measurement blackout when width kills fills |
| A-S center + width | Inventory-honest center; one optimization for both knobs | Its constants (γ, k, T) are assumed — right shape, unmeasured inputs |
| Full dynamic ladder | State-conditional floors, measured constants, per-minute optimization, complete defense menu | Nothing structural — remaining work is input quality: adverse prediction → L6, inventory machinery → L7, queue value → L8 |

---

### Level 6 — Adverse Selection

**Status: ✅ Taught 2026-08-09.** *(Folds in the former standalone entries: VPIN · OFI · p_tox · TailScore · Adverse Markout.)*

#### 1. What It Is

Level 5 kept writing E[adverse|fill] into the floor as if someone hands it to us; Level 6 is where that number is born. Thesis: **a fill is not income — it is an information event, and adverse selection is its price.** You sell immediacy to whoever wants it, and the counterparties who want it most urgently are precisely the ones who know *why* price is about to move. So the trade doesn't just happen *before* the adverse move — it happens *because* of it: P(informed | they chose to trade with me) is far above P(informed) in the crowd. This is not bad luck and not a risk to eliminate; it is the cost-of-goods of the liquidity business, and the level's whole job is the professional treatment of a cost: **measure it (markouts), forecast it (p_tox), price it (probability × severity into the floor), learn it (your own fills as labeled data), and defend against it (skew / widen / damp / deeper — never absence).**

#### 2. Terminology essentials

- **Adverse selection** — losses to counterparties with better short-term information. The offer selects its takers: whoever accepts your standing quote is disproportionately someone for whom it's mispriced.
- **Adverse markout** — the measurement instrument: post-fill drift *against* your side at a fixed horizon. Bought at 100.00, mid 5s later 99.85 → markout −15 ticks. Engine canon: 5-second horizon; drift ≥1 tick against you flags the fill adverse. Positive markout = the fill was actually good.
- **E[adverse | fill]** — the mean of the markout distribution *conditional on being filled* — Level 3/5's floor input. "Conditional" is the entire point: not "how much does price move," but "how much does it move given someone chose to trade with me."
- **Toxic label** — the teacher signal: did this fill's markout cross the adverse threshold? Every fill becomes a labeled training example for the forecaster.
- **VPIN** — flow toxicity read from *completed trades*: chop the tape into fixed-**volume** buckets (volume, not time — a bucket is the same amount of trading whether it took 4 seconds or 4 minutes), per bucket take |aggressive buys − sells| / total, roll the average. Informed traders trade one way; noise roughly cancels. High VPIN → one-sided, likely informed tape. The *confirming* signal.
- **OFI (order-flow imbalance)** — pressure building in the *book* before trades fire: net (bid adds − bid cancels) − (ask adds − ask cancels). A quiet accumulator shows up here first. The *leading* signal; VPIN confirms it; markouts settle it.
- **p_tox** — per-side probability that the *next* fill is informed, from a logistic score over live signals (book imbalance, momentum, flow/VPIN, trade acceleration). Per side because toxicity is directional: a large seller makes **bid** fills toxic while ask fills stay clean — one symmetric number would tax the wrong door.
- **q99 (tail severity)** — how bad the bad case is: the 99th-percentile adverse markout, estimated *per toxicity bucket* so calm fills don't dilute storm tails. Thin books have violent q99; deep books don't.
- **TailScore** — probability × severity in one number: p_tox × q99 (normalized). Asset A: p 0.8, q99 3 ticks. Asset B: p 0.3, q99 60 ticks. B is the dangerous one despite the lower probability — p_tox alone ranks them backwards.
- **Toxic-flow clustering** — informed flow arrives in runs, not independently: repeated same-side fills while price drifts is the signature, and defense must escalate *during* the run, not after it.

#### 3. Why the Naive Approach Fails

**The naive model:** "Volatility is risk — widen with σ. And every fill is income: getting filled means my price was attractive."

**Analogy — the standing offer on the car lot.** A dealer posts: *"I buy any Model X for $10,000, no questions asked."* The average Model X is worth $10,500 — the offer looks +$500 per car. But the cars that *show up* are not average cars: the owner who knows hers is worth $12,000 keeps it; the owner who knows the gearbox is dying sells within the hour. The standing offer is accepted exactly when it's wrong — the average car *offered* is worth $9,000, and the dealer loses on precisely the trades he wins. Note what the fix is **not**: refusing to buy (that's closing the shop). It's pricing the selection — inspect what you bought (markouts), watch who's hurrying toward the lot (OFI, VPIN), lower the standing price as sellers cluster (p_tox into the floor), and reserve for the rare engine-fire wreck (q99).

The naive desk fails on both of its beliefs. σ measures how much price wiggles *for everyone*; adverse selection is about *who trades with you* — flow can be lethal under calm σ (a patient accumulator picking off your asks) and benign under wild σ (noise churn you're paid to intermediate). And "fill = income" has the conditioning backwards: the fill is the moment the informed reveal themselves. Count fills as wins and you will maximize exactly the events that carry the loss.

#### 4. How It Works (Simple → Sophisticated)

##### Step 1 — Measure it: the markout is the instrument

Record every fill; at +5 seconds compute `drift = (mid − fill_price)/tick × side`. The distribution of these numbers *is* the cost-of-goods report of the shop. Keep it live per side as fast rolling averages over the last ~100 fills: the **adverse rate** (share of fills ≥1 tick against) and the **adverse size** — together, E[adverse|fill]. This is where Level 5's $0.18 came from: accumulated, never assumed. One discipline point: measure from your *own* fills, not the public tape — the selection acting on *your* quotes is the thing being priced.

##### Step 2 — Price it: probability × severity, per side

The mean is not enough — two assets with identical average markout can differ 20× in the tail, and the tail is what ends sessions. So decompose the floor's adverse component the way an insurer prices catastrophe:

```
δ_adv (per side) = k · p_tox(side) · q99(current toxicity bucket)     [capped]
                    ────────────────   ─────────────────────────
                    chance the next     how bad "informed"
                    fill is informed    gets when it happens
```

Severity is estimated per toxicity bucket so that storm tails are priced from storm data. Before enough fills exist, a coarse fallback (½ · p_tox · realized adverse average — the Glosten–Milgrom shape) holds the floor up; the measured machinery takes over as evidence arrives.

##### Step 3 — Forecast it: p_tox from live signals

```
score(side) = bias + w1·(signed book imbalance) + w2·momentum + w3·flow(VPIN) + w4·acceleration
p_tox(side) = sigmoid(score)        — the sign of the signals flips between sides
```

The same sell pressure that endangers the bid *protects* the ask — per-side by construction, which is what makes skew (Step 5) automatic rather than bolted on. The signals sit on a time ladder: **OFI leads** (pressure building in the book, before any trade), **VPIN confirms** (executed one-sidedness), **markouts settle** (the realized outcome). The engine reads the earlier signals so it doesn't have to pay the later one.

##### Step 4 — Learn it: your own fills grade the forecaster

Each matured markout hands back (features at fill time, toxic label) — a free training example. Online logistic update: `w ← w − lr · (p_tox − label) · features`. What makes this institutional adaptation rather than a curve-fit are the guardrails: the learning rate shrinks with fill rate (a busy hour must not mean 100× faster drift); weights are pulled gently toward structural seeds and clamped to a band around them (the *shape* of the model is fixed; only its *sensitivity* adapts); and separate weight sets per flow regime — quiet / normal / toxic, classified by VPIN terciles — so storm learning never overwrites calm learning. Level 5's test is passed the honest way: if reality changed, these numbers notice — through your own fills, within the session — and they cannot run away from their structure.

##### Step 5 — Defend it: the ladder, now with its wiring

Level 5 gave the ladder; Level 6 supplies what each rung listens to:

1. **Skew** — toxicity is directional, and p_tox is per-side, so the endangered side's δ_adv rises while the safe side's doesn't: the tax lands on the door being attacked, the exit stays discounted.
2. **Widen** — δ_adv flows straight into the per-side floor: storm E[adverse] $0.60 → floor $0.68 (Level 5's numbers), automatically, side by side.
3. **Size-damp** — quoted size × exp(−k · p_tox): smooth in the signal, small under stress, never zero.
4. **Post deeper** — severity-scaled: reprice depth grows with q99, and the queue amplifier prices L8's gradient (back-of-queue fills are the sweeps).

Plus the clustering response: a fill that marks out badly triggers a temporary extra widening **on the hit side only**, decaying over seconds — runs cluster, and the next one is usually coming. Every response is continuous, per-side, and *present*: no rung is "stop quoting" — the pull stays off the menu (Level 5's argument, now with its measurement: no fills → no markouts → the estimates go blind exactly when the regime moves fastest). Containment check: benign tape → p_tox → floor value, q99 small, scars decayed → δ_adv ≈ calm baseline; the naive desk survives as the special case of a market with no informed flow.

#### 5. Why Should You Believe This? — The Clean-Average Time Bomb

Two assets, both averaging −5 ticks of markout. Asset A: every fill −5, like clockwork. Asset B: 99 fills clean, then one −80 (thin book — when a sweep comes, it's violent). A mean-based floor prices them identically; B then detonates roughly once per hundred fills and hands back the day. Probability × severity separates them *before* the wreck: A is high-p/tiny-q99, B is low-p/huge-q99 → B's TailScore dominates → wider floor, damped size, deeper posting on B while A keeps quoting tight. And you don't have to take the model's word for it — the check is in your own blotter: bucket your fills by the p_tox printed at fill time. If high-p_tox fills mark out systematically worse than low-p_tox fills, the forecaster is real; if the buckets look the same, it's decoration. Reality grades it either way — that's the property to demand of every number in this level.

#### 6. Professional Standard (Jane Street / Citadel Level)

- **Markout tables as the desk's primary report** — per side, per horizon, per regime; fills treated as labeled data first and revenue second.
- **Adverse priced as probability × severity** — per side, tails estimated per bucket; never a single mean, never symmetric by assumption.
- **A time-ladder of signals** — book pressure leads, executed flow confirms, markouts settle; the desk reads the earliest signal it can trust.
- **Learning with structure** — seeded shapes, banded adaptation, regime-split weights, activity-scaled steps: adapts to reality, cannot chase noise.
- **Continuous defense only** — skew / widen / size-damp / post-deeper as smooth functions of p_tox and q99; quote-absence mechanisms deleted, not discouraged.

#### 7. Summary

| | |
|---|---|
| **What it is** | The cost-of-goods of liquidity provision: fills as information events, measured by markouts, forecast per-side by p_tox, priced as probability × severity (p_tox × q99) in the floor, learned online from your own fills, defended by the continuous ladder. |
| **Why it matters** | The counterparty chooses when to trade — so the fills you get are exactly the ones most likely to hurt. Unpriced, this converts fill count into loss count; mean-only pricing leaves the tail to end the session. |
| **Professional standard** | Own-fill markout accounting; probability × severity per side; leading→confirming→settling signal ladder; structured online learning; defense that reprices and never absents. |

#### Sees vs Misses

| Approach | What it sees | What it misses |
|---|---|---|
| σ-widening + fills-as-income | General risk level | Who it trades with: the conditioning (P(informed | fill)), directionality, the tail |
| Own-fill markouts (mean) | The realized cost, per side | The forecast (pays for adverse before knowing) and the tail hiding in the average |
| + p_tox forecast + q99 tails | Prices adverse before the fill, probability × severity, per side | Static weights go stale — the regime moves and the model doesn't |
| + online learning + regime split + full ladder | A self-grading, structure-bound forecaster wired to continuous defense | Nothing structural — inventory pressure on the same quotes → L7; queue-graded fill quality → L8; the latency component of staleness → L9 |

---

### Level 7 — Inventory

**Status: ✅ Taught 2026-08-22.** (Supersedes the interim "Inventory Risk & Inventory Dynamics" and "Inventory-Optimal Quoting" sections — absorbed and deepened below.)

*Symbol key, restated at every use per the accessibility rule: **q** = how much inventory I currently hold (as a fraction of my allowed maximum: q = +0.5 = half my long limit) · **σ** (sigma) = how much the price typically wanders per minute — the asset's jumpiness · **γ** (gamma) = how much I personally hate holding risk (a dial, not a market fact) · **T** = how long I typically stay stuck holding a position · **FV** = fair value, my live estimate of true worth.*

#### 1. What It Is

Inventory is the **exhaust of market making** — the net position that filling leaves behind. Not a choice: the only way to hold nothing is to never fill, and never filling is not a business. This level is the storeroom discipline: what holding actually costs, how the response must escalate as the position grows, when to stop managing it with quotes (get paid to shrink) and start paying to remove it, and how much position the operation may carry at all. The reframe everything descends from: **inventory is not an asset you own — it is risk you are warehousing until someone pays you to take it away.** Desks rarely die of a thin spread; they die holding a large position through a large move.

#### 2. Terminology essentials

- **Inventory (q — my held fraction of the allowed maximum)** — net position from fills, expressed as a fraction of the cap (+0.5 = half the long limit). Fractions, not lots: "3 lots" means nothing without the cap; half-full is half-full in any warehouse.
- **Directional exposure / delta** — what inventory is, risk-wise: long 5 lots at $3,000 = $15,000 riding on the next move. "Net delta ≈ 0" = positions summed across all venues per symbol hover near zero — earn the spread, not the direction.
- **Carry cost** — what holding charges even when nothing goes wrong: warehoused price-wander ≈ σ (jumpiness per minute) × √t. *Plain words on √t (square root of time): wandering doesn't grow in a straight line — 4× the holding time gives only 2× the wander, because random moves partly cancel.* At σ=$2/min, 45s hold: ~$1.75 of "could be anywhere" risk per lot. Real cost, no invoice.
- **The q² law** — *plain words on "squared" (quadratic): a number multiplied by itself — 2²=4, 5²=25 — so the thing grows faster the bigger it gets.* Pain grows with the square of the position: the same $1 drop costs $1 per held lot AND lands on top of losses the earlier lots already took. Consequence: defenses escalate **progressively** (a dimmer switch — response rising smoothly with the problem), never as a **cliff** (a light switch — nothing, nothing, everything at once). Markets punish cliffs: undefended right up to the edge, overreacting at it, exploitable to anyone watching.
- **Skew-out (passive exit — get PAID to shrink)** — the shifted center: quotes centered not on FV (my fair-value estimate) but on a point pushed away from the side I hold. Long 5, FV 3000.45, center slides to 3000.35 → ask 3000.65 (only $0.20 from FV — buyers come to me first; each fill sheds inventory AND still earns spread) while bid 3000.05 ($0.40 away — rarely fills, overpaid when it does). Discount the exit door, tax the entrance.
- **Hedge-out (active exit — PAY to be done)** — cross the spread myself, here or elsewhere: instant, certain, and priced (taker fee + spread crossed + the dent my own selling makes). The level's core choice: get paid slowly vs pay to be done now.
- **Hedge band (no-hedge zone)** — inside ±X% of cap, quotes handle it; beyond, active hedging fires. The inside exists because hedging every lot instantly refunds the whole earned spread as taker fees — small inventory must breathe.
- **Inventory half-life** — *plain words: the time for something to shrink to half its size.* If 6 lots typically becomes ~3 in 60s of normal two-way flow, half-life = 60s. It is the measured version of T (stuck-time) — and an alarm: half-life stretching means the exit side stopped filling → flow turned one-sided.
- **Inventory cap** — the hard boundary, set by survival math (worst plausible move × max position must be a shruggable loss), never by confidence. At the cap the growing side stops quoting — the one legitimate quote-absence: a risk limit binding, not a market opinion.
- **Adverse inventory** — toxic flow *gives* you inventory precisely when it's about to lose value (they sold to you because it's going down). Position built during high-p_tox moments (p_tox = estimated probability a fill is from informed flow) is born already losing. "Inventory is neutral holding" fails like "a fill is income" failed.
- **Mark-to-market** — count inventory PnL at current FV every cycle, not at exit. The loss already exists and updates live; the question is never "how do I get back to breakeven" (a gambler's prayer) but "what does the next second of holding cost vs the price of flat."

#### 3. Why the Naive Approach Fails

**The naive model:** "Inventory is fine — I only lose if price moves against me; flat-PnL holding is free, and I'll get out at breakeven eventually."

**Analogy — the fish stall.** A fishmonger buys at 90 from the boats, sells at 110 to customers. Between the two, fish sits on ice and **spoils** — holding itself costs, no bad day required (= carry). Ten unsold crates at dusk is worse than 10× one crate: the same price drop hits every crate at once, on top of losses already taken (= the q² law). Overstocked by afternoon, he rewrites the board — sale price for customers, stingy price to the boats (= skew-out: paid to shrink). At 6pm with 8 crates and a storm coming, he calls a restaurant and sells at 85 — below his 90 cost — because certain small loss now beats expected bigger loss overnight (= hedge-out). And however good the boat price, he never buys past what the ice-box holds — capacity set by what one bad night can cost, never by confidence in tomorrow (= the cap).

The naive desk books none of this: carry uncounted (over-holds — every hold looks free until it isn't), escalation absent or cliff-shaped, no paid-exit preference, no band, no honest ledger ("waiting for breakeven" while the mark-to-market loss already exists). **Misses:** the position is the risk; the PnL is just its shadow.

#### 4. How It Works (Simple → Sophisticated)

##### Step 1 — Price the holding: carry

While holding q = 5 lots (five units of my inventory) at σ = $2/min (typical wander) for T = 45s (stuck-time), plausible wander ≈ σ×√T ≈ $1.75/lot → ~$8.75 of warehoused "anything can happen." Charge it forward: a fill that *reduces* the position is worth more than its spread capture — it refunds warehoused risk (the inventory term in the maker-economics EV formula). What this alone still misses: the charge must *escalate* with position.

##### Step 2 — Escalate like a dimmer: the q² curve

Center shift = **q × γ × σ² × T** — *(how much I hold) × (how much I hate risk) × (jumpiness, squared — because wander compounds) × (how long I'll be stuck)*. Sanity checks: flat (q=0) → no shift, quote around FV ✓. Sleepy asset (σ tiny) → tiny shift even loaded ✓. Slow-turnover asset (T long) → bigger shift for the same holding ✓. Each extra lot shifts the center further than the last one did (the q² law acting), and size tilts follow the same curve. Never a cliff: a threshold in a risk response is a bug unless it is the final hard cap. What this still misses: escalating quotes only *shrinks slowly* — it needs two-way flow.

##### Step 3 — The default exit is the paid one: skew-out

Preference order, always: **get paid to shrink before paying to shrink.** The tilted quotes do three jobs: the discounted exit side attracts the flow that reduces me (still earning spread over FV on the way out); the taxed entry side slows accumulation and overpays me when it fills; both scale automatically with the q² pressure. Add size asymmetry (bigger on the exit side, smaller on entry) and the position acquires a natural half-life (6 lots → ~3 in 60s of two-way flow). Watch that half-life live: it is a cost input (stretching = T rising = carry rising = skew harder) and an alarm (frozen = exit side stopped filling = flow one-sided). What skew-out misses: **in a trend it fails** — the discounted exit barely fills while the taxed entry keeps getting hit. Waiting becomes a bet.

##### Step 4 — When passive fails: the hedge band

```
inside band (|q| ≲ 0.3 of cap)  →  quotes handle it: skew + size tilt
outside band                    →  active hedge: cross the spread, pay
                                   fee + spread + impact, be flat NOW
```

Why the inside exists: hedging every lot refunds the earned spread as taker fees. Why the outside exists: beyond some q (held fraction), the per-second carry cost — growing with q², the square of the holding — exceeds the *one-time certain* cost of exit; the restaurant call becomes mathematically cheap. Professional refinement: **the band is not static** — it tightens when toxicity is high (adverse inventory is born losing), when σ (jumpiness) spikes, when stuck-time stretches. A fixed band is a calm-day tool in all-weather clothes.

**Where to hedge — the cheapest door, itemized.** Same-venue unwind is a candidate, not a taboo; compare all-in:

```
same venue:   spread crossed + taker fee + impact on MY OWN book (+ self-trade risk)
cross venue:  spread crossed + taker fee + impact there + basis risk + funding + later unwind
```

Three reasons the away door often wins in exactly the moments it's needed: (1) **in a crisis the home book is the worst book** — the same one-sidedness that broke skew-out makes the home exit thin and expensive, while another venue has a different crowd; (2) **dumping into your own market bombs your own shop** — it moves the FV you quote around, trips your own defenses, marks down the rest of your inventory; (3) **self-trade** — your aggressive exit can hit your own resting quote (prohibited or pointless). And netting counts: +5 here and −5 there IS flat in direction; the residual (basis — the two prices drifting slightly apart) is a far smaller, mean-reverting risk than naked direction.

##### Step 5 — The boundary and the crisis

**Cap:** survival arithmetic (worst plausible move × max position ≤ shruggable loss). Approaching it, everything escalated smoothly already; at it, the growing side stops — the one legitimate absence (solvency wall, not sentiment).

**Crisis playbook** (trend down, long q = 0.7 of cap, toxicity high, half-life frozen): survival math replaces profit math. All at once: center slides hard (q²-scaled skew, now large); entry side damps toward minimum size and deepens — *damped to near-dark, never disabled* (the tiny quote is a paid sensor; disabling is the cliff with a re-entry problem); exit side stays present at honest aggressive-but-paid prices; the band — tightened by toxicity + σ + stuck-time — fires the active hedge early through the cheapest door; mark-to-market keeps the ledger honest throughout. What survives the day is not the spread earned — it is the position that wasn't there when the move extended.

#### 5. Why Should You Believe This? — Withdraw vs Near-Dark

The strongest objection, taken seriously: *"if the market is purely one-sided and I can't exit if filled, why quote at all until conditions normalize?"* The ladder's terminal state IS almost withdrawal — endangered side at the storm floor, minimum size, posted deep: worst case is one tiny overpaid fill. So why keep the 1-lot token instead of zero? Because the difference isn't PnL — it's **information and re-entry**: (1) every estimate (markouts, p_tox — the informed-fill probability — fill rates, half-life) feeds on your own quotes; withdraw and the estimates freeze at storm values, and you're left reading the public tape, which tells you what *others* experience, not what *your quotes* would — the desk that stayed present re-tightens minutes earlier, and the post-storm minutes (wide spreads, freshly two-way flow) are historically the best of the day; (2) "return when normal" needs a re-entry threshold — a cliff that flaps at the boundary, is exploitable once observed, and can't be calibrated while absent; the continuous ladder has no re-entry decision at all — the dials that widened simply narrow; (3) queue position — withdraw and re-enter at the back of every queue exactly when priority is most valuable. Empirical seal: quote-absence mechanisms (no-trade gates, per-side disables, micro-suppression) were built into this program's engine in early iterations and removed one by one — measured over full cycles they cost more than they saved. Absence remains legitimate in exactly two rule-based forms: the inventory cap binding, and catastrophic stop events. Discretionary absence — "conditions feel bad" — is forbidden, because the machine's whole claim is that "bad" is a number, and the number goes in the price.

#### 6. Professional Standard (Jane Street / Citadel Level)

- **Carry booked continuously** — inventory PnL marked to FV every cycle; the holding cost accrues in the ledger as it accrues in reality, per position, per venue.
- **Progressive escalation, no interior cliffs** — skew/size/width respond smoothly to q (held fraction) with the response *accelerating* in the tail per the q² law; the only discontinuity is the final hard cap.
- **Band as a living function** — the hedge trigger reads σ (jumpiness), fees, toxicity, and inventory age — not a constant; passive-exit failure (frozen half-life) mechanically advances the active exit.
- **Cheapest-door routing with fail-loud** — every hedge ranked on itemized all-in cost (spread, fee, impact, basis, funding, freshness, headroom); self-trade excluded by construction; "no eligible door" is an explicit alarm, never silent unhedged exposure.
- **Net-delta accounting against exchange truth** — flat means the venue-summed position verified against exchange statements, with tolerances at least as tight as the truth oracle's.

#### 7. Summary

| | |
|---|---|
| **What it is** | The storeroom discipline: carry priced (σ√t per lot), escalation on the q² curve via the shifted center, skew-out as the paid default exit, a living hedge band choosing when to pay to be done, cheapest-door routing, and a survival-math cap. |
| **Why it matters** | Inventory is how market makers actually die: unpriced carry over-holds, cliffs lurch, frozen half-lives unnoticed become trend-riding positions, and the cap is the difference between a bad day and the last day. |
| **Professional standard** | Continuous mark-to-market, progressive q²-shaped response, signal-conditional band, itemized all-in exit routing, truth-verified net delta. |

#### Sees vs Misses

| Approach | What it sees | What it misses |
|---|---|---|
| "Flat PnL = free holding" | Realized wins and losses | Carry — the warehoused wander (σ√t) charged invoice-free; adverse inventory born losing |
| Fixed skew per lot (linear) | Inventory influences quotes | The q² acceleration — same response at q=0.1 and q=0.8 is wrong at both ends |
| Skew-only exits | The paid exit; spread earned while shrinking | Trend failure: passive exit needs two-way flow; frozen half-life = waiting became a bet |
| + hedge band + routing + cap | Paying-to-exit priced and routed through the cheapest door; solvency boundary | Nothing structural — remaining work is input quality: queue value of the resting quotes → L8, latency of the exits → L9, cross-venue machinery at depth → L16 |

---

### Level 8 — Queue / Fill Probability

**Status: ✅ Taught 2026-08-09 · retaught + deepened 2026-08-25.**

*Symbol key (glossed at every use per the accessibility rule): **P(fill)** = the chance (0–100%) a resting quote actually trades within a window · **q_pos** = my estimated place in the line (0 = front, 1 = back) · **V_ahead** = the lots standing in front of me that must leave before my turn · **λ** (lambda) = how many aggressive orders arrive per minute · **k** (fill-decay) = how fast fill rate dies with distance from the mid · **FV** = fair value, my live estimate of true worth · **EV** = expected value, the average profit of a decision repeated many times.*

*Plain words on "gradient" (used throughout): a value that changes gradually and steadily as you move along something — a slope, not a jump. A hill's steepness, a color fading blue→red. The fill-quality gradient: fills worsen smoothly position-by-position toward the back of the queue — 1st in a 40-lot line maybe 15% of fills toxic, 20th maybe 30%, 39th maybe 70% — because the only event that reaches the back is one big enough to eat everyone ahead first, which is a sweep, and sweeps are informed. The dimmer/cliff distinction from Level 7 is the same family: a gradient is what the dimmer produces.*

#### 1. What It Is

Level 5 priced the distance from FV — and kept promising that "post deeper builds queue position" and that the re-quote dial protects it. Level 8 is that promise, paid: **a resting order's value is its price AND its place in line.** At each price level the exchange fills orders first-come-first-served (price-time priority): price gets you into the room; arrival time decides your place in the queue. So two desks quoting the *identical* price own different products — the one at the front gets filled by ordinary flow; the one at the back gets filled only when something eats everyone ahead of it. P(fill) is not a function of your price. It is a **race** between the aggressive flow arriving and the wall of volume standing ahead of you — and where you stand in that wall changes both how often you fill and *which* fills you receive.

#### 2. Terminology essentials

- **Price-time priority (FIFO)** — within a price level, fills go in arrival order. The book is a room of lines, not a wall of prices.
- **Queue position (q_pos)** — normalized place in line: 0 = front, 1 = back. On an L2-only venue (Binance publishes level totals, no order IDs, no queue API) it is *never observable* — it must be estimated.
- **V_ahead** — visible volume standing ahead of you. Place-time worst case: everything at your level arrived before you.
- **Fill intensity (λ) / flow window** — aggressive volume per minute hitting your side; λ × horizon × avg trade size = the expected "chew" through the wall over your holding window.
- **Share-form P(fill)** — the race as a share: `p ≈ V_flow / (V_ahead + V_flow)`. The textbook `exp(−V_ahead/λ̄)` treats the queue as passively decaying; the share form treats it as a *contested resource* — the professional choice.
- **Trade vs cancel attribution** — a level shrinking means either a trade (consumes the FRONT — you advance by 100% of it) or a cancel (could be anywhere in the line — credit yourself only ~half). Botch this split and q_pos is systematically wrong in one direction.
- **Position-dependent cancels** — cancels aren't uniform: the back of the queue is where the repricers live. Model the cancel's position as `p(x) = x·(1 − k(1−x))` with k learned from your own fill outcomes (Moallemi–Yuan).
- **Queue value** — the option value of your current place: what you forfeit by cancelling. ≈ (your position's share of near-term fills) × (capture net of adverse). An asset, paid for with waiting.
- **Churn** — cancel/replace so frequent you live permanently at the back of every line. Fresh price, worthless position.
- **Queue-toxicity gradient** — fills that reach the back of the queue are conditionally worse: only a sweep big enough to eat the whole level gets there.

#### 3. Why the Naive Approach Fails

**The naive model:** "I'm quoting at the best bid, so I get filled at the market's fill rate. If FV moves a tick, cancel and re-post at the better price — fresher is better."

**Analogy — the walk-in list at a packed restaurant.** Your place on the list is an asset you bought with waiting. Step out to check the place across the street and you re-join at the back. And the vicious part: if the host calls your name while you're 15th on the list, it's because the fourteen ahead of you were all seated at once — a bus tour is emptying the restaurant. Deep in the queue, being served isn't good news; it's the signature of exactly the event you didn't want.

The naive desk fails three ways at once: it prices P(fill) off the price alone (two desks at one price ≠ one fill rate); every re-quote pays an invisible toll — back of the line — that never appears on any per-fill blotter; and it *selects itself into the worst flow*: perpetually at the back, the only fills that reach it are the sweeps that ate the level. Its markouts look "unlucky." They are structural.

#### 4. How It Works (Simple → Sophisticated)

##### Step 1 — P(fill) is a race, not a curve

Running example, our bid at one price level:

```
Wall:  12 lots visible ahead; participation haircut ×0.5 (not all visible size is real) → 6 effective
Chew:  λ = 4 aggressive sells/min × 0.9 lots avg × 1.5 min horizon ≈ 5.4 lots

p_volume = 5.4 / (6 + 5.4)        ≈ 0.47      ← the race, as a share
p_fill   = p_volume × (1 − q_pos)             ← discounted by place in line
         ≈ 0.47 × 0.2 ≈ 0.09  just joined (q_pos ≈ 0.8)
         ≈ 0.47 × 0.9 ≈ 0.42  after the line advanced (q_pos ≈ 0.1)
```

Same price, same book: joining fresh ≈ 9%, owning the front ≈ 42%. Level 5's fill-decay k is the right *shape* across depths (the demand curve of the immediacy shop); at a single price, the line dominates — so model the race, keep the exponential as a sanity diagnostic.

##### Step 2 — Estimating your place when the venue hides the line

L2-aggregated data gives level totals only. Queue position is *inferred*, rung by rung:

1. **Place-time worst case:** on arrival, assume everything visible at your level is ahead of you. Pessimistic and true.
2. **Trades at your level** consume the front — advance yourself by 100% of the traded volume.
3. **Cancels** could come from anywhere — credit only ~50% as "ahead of you." (100% and you'll believe you're at the front while you're not; 0% and you never advance.)
4. **Position-dependent refinement:** cancels come disproportionately from the back (that's where repricers live). `p(x) = x(1 − k(1−x))`; learn k per side from your own fills — predicted vs realized adverse markout, a small Bayesian update per fill, live only after ~30 observations. *Reality grades the estimator.*
5. **Regime conditioning:** the same shrink reads differently by state — in toxic regimes, cancels ahead are likelier (informed makers pulling), so k's prior shifts across {quiet / normal / toxic}.

##### Step 3 — The queue filters your customers

Level 6 taught that a fill is an information event. Level 8 sharpens it: **the severity is graded by your queue position.** For flow to reach the back of a 12-lot line, one aggressor must consume all 12 — and orders that size are rarely uninformed. Front-of-queue fills sample ordinary flow; back-of-queue fills sample sweeps. So E[adverse|fill] (Levels 3/6) is not one number — it is a function of q_pos, and the Level 5 floor for a back-of-queue quote should sit *higher* than for a front-of-queue quote at the same price. The queue changes not just how often you're paid, but what each payment costs you.

##### Step 3b — Cold start: seeding the estimators before any fills exist (added 2026-08-25 Q&A)

Both learned numbers in this level need fills to learn from — so what feeds them on a fresh run? A **ladder of fallbacks**, and the two k's start from different rungs:

- **The queue cancel-bias k** (how much of an unexplained level-shrink happened *ahead* of me) can only be graded by my own fills — so its cold start is pure priors: a hand-set conservative default → a per-regime prior (toxic regimes: informed makers pull more, so cancels skew more toward "ahead") → the learned per-side value takes over only after ~30 fill-observations, the point where its uncertainty shrinks below the prior's. Same born-with-a-safe-opinion pattern as the toxicity model's Glosten-Milgrom warmup fallback and the p_tox seed weights.
- **The fill-decay k** (how fast fill rate dies with distance from the mid) has a **public shadow** — no own fills needed for a first draft: a quote at depth d can only fill if aggressive flow *reaches* depth d, and that is visible on the public tape. Replay an hour: flow reached 1 tick 41×/hr, 2 ticks 17×, 3 ticks 6×, 5 ticks 1× — that curve's steepness is a day-zero k per asset. Bias warning: it's an *optimistic ceiling* (flow reaching your depth ≠ your fill — you'd be standing in a queue there, behind V_ahead, the wall in front); so discount it, lean pessimistic on fills (surprises arrive as gifts), and let own-fill depth-bucket measurements replace it bucket by bucket.

The cold-start discipline in one line: **a learning system must be born with a safe opinion, not a blank one — and the safe opinion must not strangle the data supply that would replace it** (a seed so pessimistic that nothing ever fills can lock itself in forever).

##### Step 4 — Queue value: the reprice toll-gate

Cancelling destroys queue position — an asset. Repricing is therefore a *purchase*: a better price, paid for with your place in line. The gate:

```
reprice only if   EV(new depth, back of line) − EV(current depth, current q_pos)  >  queue_value

queue_value ≈ 1/(q_ahead + 1) × λ × max(0, spread capture − adverse − fees)
```

Consequences: (1) near the front of a thick queue, queue value can exceed a tick of price improvement — *staying put at the "wrong" price is correct*; (2) the gate auto-loosens when the queue is thin or flow is dead (nothing to forfeit); (3) this is Level 5's re-quote dial made exact — sub-noise repricing is churning an asset for nothing.

##### Step 5 — Dynamic by construction

Every input is a living estimate: λ and average trade size as fast EWMAs off the tape; k learned per side from fill outcomes; regime priors switching the structure; participation (how much visible size is real) discounting the wall. Containment check: alone at your level → V_ahead = 0, q_pos = 0, pos_factor = 1 → p_fill collapses to the pure race share — the naive "price-only" model survives as the special case of having no line at all.

#### 5. Why Should You Believe This? — The Churner's Paradox

Two desks, same feed, same fair value. Desk A re-quotes on every tick of FV noise: always the freshest price — and its fills lose. Desk B re-quotes through the queue-value gate: sometimes a tick "stale" — and its fills earn. The mechanism is the whole level at once: A pays the reprice toll continuously (always at the back) → its p_fill collapses → the few fills that reach it are the level-eating sweeps (Step 3) → its realized E[adverse|fill] runs far above the population average its spread floor was computed from. Fresh price, poisoned fills; patient price, benign fills. The line, not the price, decided who profits — and no per-fill accounting shows the toll. Only a markout table *split by queue position* reveals it.

#### 6. Professional Standard (Jane Street / Citadel Level)

- **Queue position on the balance sheet** — resting orders carry a queue-value mark; every cancel decision is charged for it. Front-of-queue positions in thick books are treated as inventory.
- **Probabilistic estimation wherever the venue hides the line** — worst-case join, trade/cancel attribution, position-dependent cancel models (Cont–Kukanov–Stoikov, Moallemi–Yuan), every parameter passing the Level 5 test: *if reality changed, would this number notice?* (k learned from own fills does; a hardcoded cancel split doesn't.)
- **Markouts conditioned on queue position** — the toxicity gradient measured, not assumed; floors per q_pos band.
- **Reprice through a value gate, never on price noise** — churn ratio watched as a first-class health metric.
- **Simulation honors the queue** — the sim's fill model is FIFO with pro-rated cancels; a sim that fills you at price-touch overstates the whole business.

#### 7. Summary

| | |
|---|---|
| **What it is** | The line at each price: P(fill) as a flow-vs-wall race discounted by queue position; the position inferred probabilistically on L2-only venues; queue value charged on every cancel/replace. |
| **Why it matters** | Same price, different place = different business — fill rate AND fill quality are graded by the queue; churn silently converts a market maker into a sweep collector with fresh prices. |
| **Professional standard** | Queue position estimated, learned from own fills, and carried as an asset; markouts split by queue band; repricing tolled; sims FIFO. |

#### Sees vs Misses

| Approach | What it sees | What it misses |
|---|---|---|
| Price-only P(fill) ("I'm at the touch") | The demand curve across depths | The line at each depth — two desks, one price, different businesses |
| Race model, no position | Flow vs wall — the true fill contest | Where you stand: a fresh join priced like the front of the line |
| + estimated q_pos | Fill rate by place in line | Fill *quality* — the toxicity gradient; and the cost of losing the place |
| + queue value + learned cancels | The full asset: rate, quality, reprice toll, self-grading estimator | Nothing structural — input quality: staleness of the estimate → L9; machinery that preserves the queue (modify vs cancel/replace) → L10 |

---

### Level 9 — Latency / Staleness

**Status: ✅ Taught 2026-09-10.**

*Symbol key (glossed at every use per the accessibility rule): **ms** = millisecond, a thousandth of a second (a human blink ≈ 100–150ms) · **FV** = fair value, my live estimate of true worth · **RTT** = round-trip time, the full there-and-back delay of a message · **p99** = the 99th percentile — line all measurements up best to worst; the value 99% of them beat: your bad-day-but-not-rare number · **δ** (delta) = the half-spread, my quote's distance from FV.*

#### 1. What It Is

Every prior level assumed that when the engine decides, the market hears it instantly. This level removes the fiction: **you never trade in the market's present — you trade in its recent past, and your orders land in its near future.** One question asked three ways: how old is my picture, how slow is my hand, and who profits from the gap? It owns the killer Level 6's forensics identified but couldn't fix — adverse markout concentrated at 100–500ms = *you were slow* — and no amount of widening cures slow.

#### 2. Terminology essentials

- **Latency** — the delay between "something happened" and "my response took effect" — a *chain* of delays (feed → decision → send → venue processing), each with its own clock. Tokyo co-located ≈ 10ms round trip; home wifi ≈ 80–200ms; Delta REST ≈ 750–1000ms.
- **Tick-to-trade** — the full budget: exchange stamps the event → exchange stamps my resulting order. Itemized per link, because the slowest link caps the chain (a 1ms engine behind a 750ms venue API is a race car in a traffic jam).
- **RTT vs one-way** — orders need the round trip (the acknowledgment coming back ends my flying-blind window about my own state); reactions need one-way each direction, and the directions aren't equal.
- **Staleness** — quoting on an FV that no longer reflects reality. Latency is the cause, staleness the condition, the pick-off the consequence. Measured in *information*, not seconds: 5s old in a dead market = fresh; 50ms old after a leader-venue jump = lethal.
- **Pick-off race** — leader jumps 3000.30→3001.10; my ask rests at 3000.60 on the follower. Two messages race: the arbitrageur's buy toward my stale quote, my cancel toward removing it. First processed wins the $0.50.
- **Cancel latency** — the defensive critical path: slow placement costs opportunity; slow *cancel* costs money (the stale quote stays exposed).
- **Jitter** — *plain words: how much the delay itself wobbles.* Treacherous because the wobble clusters at the worst moments — event bursts flood the venue, queues swell, your cancel crawls exactly when the race is live. Hence p99 (the bad-day number), never the average.
- **Latency floor** — the venue-imposed minimum you cannot engineer away. Delta's 750–1000ms made sub-second-reaction strategies *impossible* there — a selection fact, not an engineering challenge.
- **Pricing your slowness** — the residual exposure window (my p99 reaction vs the fast crowd's) has a computable expected cost per quote → it belongs in the spread floor next to adverse selection and inventory carry.
- **Measure-first** — this program's own scar turned doctrine: "behavior bugs" that were latency in a strategy costume; every number above is real only once measured on your own path, distributions kept (median AND p99), re-measured on any change.

#### 3. Why the Naive Approach Fails

**The naive model:** "My code is fast, so I'm fast. Re-quote every X ms so quotes are never old."

**Analogy — the bettor with the delayed TV.** He takes live football bets; his feed runs 3 seconds behind the stadium. Against customers watching the same delayed TV, his odds are fair — everyone's equally behind. But a few customers are *in the stadium, on the phone*: when a goal is scored they have 3 full seconds to bet at his stale odds — and they only call in those 3 seconds. His ledger shows the signature: ordinary bets net fine; a thin stream of bets, always placed moments before his own screen shows a goal, always loses. His options: faster feed (engineering); suspend odds whenever anything *might* have happened (the pull anti-pattern — he'd take no bets at all); **widen odds by exactly the expected cost of the 3-second window** (stay in business, priced); or — if this stadium's phone crowd is too big and the feed unfixable — stop covering *this stadium* (the venue decision).

The naive desk fails both beliefs: "my code is fast" measures one link of a chain whose slowest link — often the venue itself — sets the total; and "re-quote every X ms" uses the calendar clock when staleness lives on the information clock, churning queue seats (Level 8's toll — the place in line sold for nothing) in calm while still losing the race in storms.

#### 4. How It Works (Simple → Sophisticated)

##### Step 1 — The budget audit

Clock-stamp every link, keep distributions (median and p99 — the bad-day number):

```
exchange event ─► my feed ─► decision ─► send ─► venue processes
  (t₀ stamp)      +2ms        +0.5ms     +4ms     +3.5ms        = 10ms tick-to-trade

defensive path:  FV jump seen ─► cancel decided ─► cancel lands = my exposure window
```

Audit rules: the slowest link caps the chain (fix nothing else until the bottleneck moves); the p99 is the operative number (jitter clusters exactly when the race is live — a 10ms-median/300ms-p99 path IS a 300ms path on the days that decide the month); measure on your own path, always.

##### Step 2 — The race, with numbers

Leader jumps; my ask is stale on the follower. Symmetric speed → coin flip. Realistic asymmetry: his co-located feed beats my public stream by 15ms, my decision loop adds 5ms average wait, ordinary cancel path +10ms → his attack lands t+12ms, my cancel t+42ms: **a 30ms window where my $0.50 giveaway is guaranteed.** Expected cost per hour = (jumps big enough to cross my spread) × (average giveaway) × (P(my quote at risk)) — e.g. 6 jumps/hr × $0.40 ≈ $2.40/hr of latency tax, booked at 100–500ms markouts as "adverse selection" unless the markout is split by horizon. Level 6's rule: the horizon shape names the killer; widening cures the 5s-drift killer, only speed or priced slowness cures this one.

##### Step 3 — Staleness on the information clock

Two paths, by construction: the **slow path** — routine re-anchoring through the re-quote suppression band, protecting queue seats from noise; the **fast path** — a short list of tripwires (leader-venue jump past threshold, sweep on my own book, book-integrity failure) that bypass every smoothing filter and fire the cancel NOW. Order of operations is doctrine: **cancel first, think second** — the recompute takes longer than the cancel; sequencing them the other way donates the difference. The fast path's budget is Step 2's race; it justifies engineering the cancel into the fastest message the system sends.

##### Step 4 — Price the slowness you can't remove

After engineering, a residual window remains (my p99 vs the venue's fastest crowd). Two honest responses. **Charge for it**: the window's expected cost is a per-fill cost like any other → into the spread-floor decomposition next to adverse selection and inventory carry. A 40ms desk quotes structurally wider than a 5ms desk — arithmetic, not fear. Self-assessment metric: if the latency term dominates your floor, you are not a market maker at this venue — you are prey with a spreadsheet. **Respect the floor**: some windows are venue physics (Delta's 750–1000ms REST). The walk-away bar: hard floor + no workaround + research-backed impossibility diagnosis → leave the venue, not the business. Latency is a *selection* input — it decides which venues and which assets your speed class permits (Level 12 inherits this).

Containment check: no leader venue, no fast crowd, calm tape, my p99 ≈ everyone's → the race has no runners, the latency term ≈ 0, staleness collapses to clock-age — the naive periodic re-quoter survives as the special case *nobody here is faster than me and nothing jumps*.

#### 5. Why Should You Believe This? — The Premium vs the Fear

Latency premium and fear-widening produce the same visible act (wider quotes) from opposite processes. The premium is **computed** — charged only for the measured exposure window, sized by jump frequency × giveaway × exposure probability, leaving P(fill) optimal *for your true speed class*; it narrows automatically as engineering shrinks the window. Fear-widening is **uncalibrated** — a tax on all flow including the tourists, killing P(fill) for protection you could have priced precisely. And the premium carries its own verdict: computed honestly, it sometimes reports that *no width works* — the floor is venue-imposed, unfixable, diagnosed — and the correct trade is to leave that venue. This program lived the full arc: mysterious "slippage bugs" → measure-first doctrine → Delta's 750–1000ms floor confirmed with the venue → pivot. The premium isn't theory here; it renamed the venue list.

#### 6. Professional Standard (Jane Street / Citadel Level)

- **Tick-to-trade itemized and alarmed** — every link stamped, median + p99 per link, regressions in the chain treated as production incidents.
- **Cancel as the privileged message** — the defensive path engineered fastest, measured at p99, and joined against adverse fills (slow-cancel → bad-fill correlation watched continuously).
- **Information-clock staleness** — quotes cancelled on world-movement (drift vs a skew-excluded anchor) and age both; fast-path tripwires bypass all smoothing; cancel-first-think-second.
- **Slowness priced, not hidden** — the residual window's expected cost in the floor; the term's size tracked as a first-class business metric per venue.
- **Latency as venue/asset selection** — speed class determines the tradeable universe; floors respected via measurement and diagnosis, not heroics.

#### 7. Summary

| | |
|---|---|
| **What it is** | The three clocks of slowness: the budget audit (chain, p99), the pick-off race (cancel vs attack), staleness on the information clock — and the residual window priced into the floor or, at venue floors, answered by leaving. |
| **Why it matters** | The 100–500ms markout killer is unfixable by pricing — it silently books latency as "adverse selection" and misdirects every defense until the markout is split by horizon and joined against the latency tape. |
| **Professional standard** | Itemized tick-to-trade, privileged cancel path, information-clock staleness with fast-path tripwires, computed latency premium, speed-class-aware venue selection. |

#### Sees vs Misses

| Approach | What it sees | What it misses |
|---|---|---|
| "My code is fast" | One link | The chain — feed, venue floor, jitter; the p99 hiding behind the median |
| Calendar-clock re-quoting | Quote age | The information clock: churns seats in calm, still loses the race in storms |
| + budget audit + fast-path cancel | The race, run properly | The residual window — unpriced slowness booked as adverse selection |
| + latency premium + venue selection | Slowness charged or walked away from | Nothing structural — execution mechanics that preserve the seat while repricing → L10; venue/asset selection at depth → L12 |

---

### Level 10 — Execution Engineering

**Status: ✅ Taught 2026-10-14.** (Supersedes the interim "Market Making Engine Architecture" section — absorbed and deepened below.)

*Symbol key (glossed at every use per the accessibility rule): **ack** = acknowledgment, the exchange's "received and accepted" reply · **qty** = quantity, an order's size · **FV** = fair value, my live estimate of true worth · **q_pos** = my estimated place in the queue (0 = front, 1 = back) · **RTT** = round-trip time, a message's there-and-back delay.*

#### 1. What It Is

Levels 3–9 produced decisions; Level 10 makes them **true at the exchange** — and keeps the engine's *beliefs* true while thousands of messages fly both ways with delays, losses and refusals. Thesis: **between your decision and the exchange's truth there is a gap of milliseconds and maybes — execution engineering is the discipline of never lying to yourself inside that gap.** Strategy bugs lose basis points; execution bugs lose positions. Nothing here is clever; all of it is load-bearing.

#### 2. Terminology essentials

- **Order state machine** — every order in exactly one state, transitions only on evidence: `SENT → ACKED → (PARTIALLY_FILLED →)* FILLED | CANCELED | REJECTED`. *Plain words: a diagram of allowed situations and allowed moves between them, like a traffic light that can't jump green→red.* Most execution bugs are the engine believing one state while the venue holds another.
- **In-flight window (flying blind)** — between send and ack the true state is UNKNOWABLE (the cancel may have landed, or the order filled a millisecond earlier). Level 9's RTT made operational. Cardinal sin: acting as if an in-flight request already succeeded.
- **The exchange matching ruleset** (Q&A-derived, the user's own compact form): **sell limit = floor (same or higher is better); buy limit = ceiling (same or lower is better); orders at same-or-better prices are matched and executed immediately.** Expanded: (1) a limit price is a bound, not a wish; (2) every arriving order first tries to trade against the best opposite side — only an order that CANNOT trade gets to rest (you don't choose maker/taker; the book's state at arrival chooses); (3) the resting order sets the trade price (and earns maker fees); (4) big orders walk the book level by level (the sweep, seen from the engine's side); (5) within a price, first-come-first-served (Level 8's queue as law); (6) no crossed book, ever — overlap is resolved by trading, instantly.
- **Post-only / GTX** — "maker or nothing": if the order would execute on arrival (= my price went stale in flight), the venue REJECTS it back instead of trading it. The reject is free staleness telemetry, not an error. The exchange is a vending machine, not a guardian — it executes written instructions wherever they overlap, knows nothing of my FV or intent; post-only is the one self-protection I can encode into the order itself. (TIF menu grounded: GTC = trade-then-rest · IOC = trade-now-cancel-rest · FOK = all-now-or-nothing · GTX = rest-only-or-reject. IOC and GTX are the two honest declarations — "here to take" vs "here to make" — the dangerous order is the plain one that declares nothing.)
- **MODIFY (amend) vs cancel/replace** — one message editing in place (may keep the queue seat, venue-specific — qty-decrease usually keeps, price change usually forfeits) vs two messages (seat destroyed, rejoin at back, plus a window where neither order rests).
- **Rate limits as budget** — venues cap message rates INCLUDING cancels; exhaustion converts a cost problem into a survival problem (unable to cancel when the Level 9 race starts). Allocation rule: the cancel reserve first, quoting spends the surplus.
- **Partial fill** — 3 of 10 lots trade, 7 rest (keeping their seat). The 3 are a real fill: inventory moved (L7), booking due (L3), and the partial is itself a signal — someone ate part of the level.
- **Reject taxonomy** — every reject class gets its own response; "retry immediately unchanged" converts one reject into a storm.
- **Idempotency / client order IDs** — *plain words: idempotent = safe to do twice.* My own unique ID per order makes the unknowable window RECOVERABLE: query by ID, or re-send the same ID and let the venue refuse the duplicate.
- **Reconciliation** — continuously diff believed state (orders, position, balances) against the venue's stated truth; the venue wins every disagreement. The mission line as machinery: trust nothing unverified against exchange truth.
- **Churn ratio** — messages per fill: a health gauge (budget efficiency, queue seats burned) and a venue-relations metric.

#### 3. Why the Naive Approach Fails

**The naive model:** "Send the order; it's placed. Send the cancel; it's cancelled. Keep a boolean `order_is_open`."

**Analogy — the Mars rover.** A 10-minute signal delay teaches every instinct this level needs. You command, then *wait for telemetry* — sending "turn right" assuming the drive completed puts the rover in a ditch (= never act on an assumed ack). Never re-send blindly: the lost message might have been the command OR the reply; re-send and the rover drives double into the crater — so every command carries a serial number the rover executes once, ever (= client-ID idempotency). The radio has a power budget; burn it on chatty corrections and you can't send "STOP" at the cliff (= the cancel reserve). And periodically the rover photographs its own position to re-ground your map — not because you erred, but because drift is inevitable and an operator on a wrong map crashes with full confidence (= reconciliation). Mantra: **the map is not the territory — the job is keeping the map honest.**

The boolean fails because it cannot represent *"I don't know yet"* — the single most common true state in a fast system. Every execution disaster is at root a state lie: believing CANCELED while the venue holds the order live (quoting a ghost that can still fill), or believing ACKED while rejected (you think you're quoted; you're absent and blind).

#### 4. How It Works (Simple → Sophisticated)

##### Step 1 — The state machine as the single source of local truth

```
          ┌────────── REJECTED (venue said no)
SENT ──► ACKED ──► PARTIALLY_FILLED ──► FILLED
 │          │             │
 │          └──► CANCEL_SENT ──► CANCELED
 └ (in-flight: true state UNKNOWN — the only honest label)
```

Transitions happen only on venue evidence, never on hope; every transition is auditable ("what message moved this order here?"). Ignorance is explicit — that is the design's whole gift.

##### Step 2 — The in-flight discipline

1. **Never act on an assumed outcome.** The classic kill: cancel sent → replacement placed immediately → the cancel FAILS (a fill beat it mid-flight) → both orders live → double exposure at exactly the moment the market moves (that's WHY you were repricing). Disciplined sequence: cancel → wait for the cancel's outcome → then place. Costs half an RTT of patience.
2. **Timeout silence = ambiguity, not failure.** Recovery decision tree (by client ID): venue says LIVE → my cancel was lost en route → re-send it (a second cancel of a dead order is harmlessly refused); CANCELED → only the reply was lost → done; FILLED → the cancel lost the race → the fill is MINE: book it, update inventory, THEN decide the next quote at the new position. Never: place the replacement before resolving, or "retry" under a fresh ID (the doubling bug in a retry costume). Refinement from practice: treat the venue's "duplicate order — already accepted" rejection as SUCCESS — a duplicate-rejection is a confirmation.
3. **Partials mutate state mid-flight.** The cancel that lands after a 3-of-10 fill cancels the remaining 7; the 3 are real. Partial-aware accounting is routine, not an edge case.

##### Step 3 — MODIFY vs cancel/replace: the decision is economic, and gated by WHY

| | Cancel/replace | MODIFY |
|---|---|---|
| Messages | 2 | 1 |
| Queue seat (L8's asset) | destroyed — rejoin at back | kept on qty-decrease (venue rules) |
| Gap where nothing rests | yes | no |

MODIFY looks strictly better — until the **defensive gate** (this program's −$1.5 → −$59 ETH scar; +$5.24 mean across seeds after the fix): when the reprice trigger is *defensive* — hostile momentum (price trending INTO my quote), toxicity, the Level 9 race — MODIFY's virtue is the crime: it **keeps the seat, and the seat is in the burning theater**. Front of the queue is first to be eaten by the informed wave. Rule: *optimization reprice → MODIFY (keep the seat); defensive reprice → hard cancel (abandon the seat on purpose; cancel first, think second).* Sibling scar: amend-in-place must inherit the original order's age — a MODIFY path that resets the staleness clock lets orders age half an hour on-venue while looking fresh locally.

##### Step 4 — The rate budget and the reject taxonomy

Allocation like capital: **the engine must always retain budget to cancel everything it has resting** (defensive capacity reserved first — institutionally: a reserved top band of the budget that maker placements may never consume, where cancels and risk-reducing exits ALWAYS flow); quoting spends the surplus; churn ratio is the live gauge of how much each message buys.

| Reject | Means | Response |
|---|---|---|
| GTX/post-only cross | price stale in flight (free telemetry) | re-price off fresh FV, re-send once; a STORM = market faster than my loop → step back, wider/deeper, let FV settle — never machine-gun |
| Filter violation (lot/notional/price) | order SHAPE illegal — deterministic | never retry unchanged; fix composition (ALL filters: LOT ∩ NOTIONAL ∩ PRICE — the 33-silent-rejects scar) |
| Insufficient margin | risk state desynced from venue | stop quoting up; reconcile balances first — map-vs-territory alarm |
| Rate-limit | the budget itself exhausted | hard backoff; cancels-only mode until headroom returns |

Unifying rule: **a reject is the venue telling you which of your beliefs is wrong.** Classify, correct the belief, then act.

##### Step 5 — Reconciliation: the outer truth-loop

Periodically and at every boundary (session start/end, any disconnect): fetch the venue's full truth — open orders, position, balances — and diff against local state. Three disciplines: the venue wins every disagreement (adjust the map, never argue with the territory); every diff is an incident to explain, not a number to patch (the same bug drifts you again tomorrow); stream truth is fast truth, snapshot truth is court truth (streams drop frames — the slow full snapshot periodically re-grounds everything; Level 2's book-resync pattern generalized to all state).

Containment check: slow venue, one order at a time, infinite budget, reliable network → every ack returns before the next decision, no ambiguity, no drift — the naive boolean survives as the special case *nothing is ever in flight*. True of a human clicking in a UI; false of an engine by its second millisecond.

#### 5. Why Should You Believe This? — The Compound Kill-Chain

Each discipline looks pedantic alone; the believer's scenario is how they fail *together*. A desk with no cancel reserve churns happily in calm (high messages-per-fill, budget draining). The storm arrives: FV jumps, the Level 9 race starts on every resting quote at once. The desk fires cancels — rate-limited: the budget went to churn. Stale quotes stay exposed; fills land on them (back-of-queue sweep fills, Level 8's worst class); the desk, flying blind mid-storm (acks delayed — Level 9's jitter clusters exactly now), re-sends under fresh IDs "to be safe" and doubles two positions. Mark-to-market now says large and wrong; the local map says modest and fine; without reconciliation the desk *keeps quoting off the wrong map with full confidence*. Every link in that chain is one of this level's rules, and every link has an incident number in this program's history — the duplicate-place guard, the MODIFY gate, the filter-composition scar, the reconcile race — each now a mechanism because it was once a loss.

#### 6. Professional Standard (Jane Street / Citadel Level)

- **Evidence-only state transitions** — a formal order state machine; "unknown" a first-class state; every transition auditable to its venue message.
- **Idempotent everything** — client IDs on every message; timeout recovery by query-or-same-ID-resend; duplicate-rejections classified as confirmations.
- **Inverted-priority rate budgeting** — a reserved cancel band maker placements may never consume; risk-reducing messages always flow; weight/headroom tracked as a live gauge with throttle tiers engaging BEFORE the venue refuses.
- **Reprice instructions gated by trigger intent** — amend for optimization, hard-cancel for defense; amend inherits the order's true age.
- **Reject taxonomy with per-class playbooks** — soft vs hard venue codes enumerated; deterministic rejects never retried unchanged; storm detection wired to backoff, not just counted.
- **Reconciliation as a subsystem** — per-symbol truth loops against venue statements; the checker gets checked; truth-resolution overrides local belief before any close fires.

#### 7. Summary

| | |
|---|---|
| **What it is** | The machinery that makes decisions true at the exchange and keeps local beliefs honest: state machine, in-flight discipline, idempotent IDs, the MODIFY gate, cancel-reserve budgeting, reject taxonomy, reconciliation. |
| **Why it matters** | Strategy bugs lose basis points; execution bugs lose positions — and they compound: churn spends the budget, the storm demands it, blindness doubles the exposure, a wrong map hides it. |
| **Professional standard** | Evidence-only states, idempotent recovery, inverted-priority budgets, intent-gated repricing, per-class reject playbooks, venue-truth reconciliation. |

#### Sees vs Misses

| Approach | What it sees | What it misses |
|---|---|---|
| Boolean order tracking | The happy path | "I don't know yet" — the most common true state; every state lie that follows |
| + state machine + idempotent IDs | Honest ignorance; safe timeout recovery | The budget: churn silently spending the cancel reserve the storm will demand |
| + cancel-reserve + reject taxonomy | Survival capacity under storm; beliefs corrected per reject class | The outer drift: missed acks and dropped frames accumulating into a wrong map |
| + reconciliation | The full honest loop — map audited against territory continuously | Nothing structural — what fills do to the position after the fact → L11; venue-class differences → L12 |

---

### Level 11 — Post-Fill Management

*(Pending.)*

---

### Level 12 — Asset Selection

*(Pending.)*

---

### Level 13 — Simulation

*(Pending.)*

---

### Level 14 — Statistical Validation

*(Pending.)*

---

### Level 15 — Adaptive Control

*(Pending.)*

---

### Level 16 — Cross-Venue / Cross-Asset

#### Multi-Asset & Cross-Venue Inventory Control

*(Interim — moved from Foundation 2026-07-10; will be rewritten to full end-to-end depth when this level is taught.)*

In real crypto market making, inventory is not isolated to a single asset or exchange. Risk must be evaluated globally across venues, instruments, and correlated exposures. True inventory management is multidimensional.

**Global Inventory Concept -**
1. Inventory must be evaluated as net exposure across all venues.
2. Example:
   - +5 BTC on Exchange A.
   - −3 BTC on Exchange B.
   - Net exposure = +2 BTC.
3. Risk is based on net exposure, not isolated venue positions.
4. Cross-venue netting reduces apparent exposure.
5. Inventory management operates at portfolio level.

**Cross-Venue Adverse Selection -**
1. Price discovery may occur on one exchange first.
2. Other venues temporarily become stale.
3. Arbitrageurs exploit stale quotes.
4. Fair value must incorporate cross-venue data.
5. Latency differences increase venue-specific adverse selection risk.

**Hedging Across Venues -**
1. Inventory from one venue can be neutralized on another.
2. Hedging reduces directional exposure.
3. Hedging introduces:
   - Taker fees.
   - Slippage risk.
   - Latency mismatch risk.
4. Hedging decisions should be threshold-based.
5. Continuous per-fill hedging is inefficient.

**Basis Risk -**
1. Basis = price difference between venues or instruments.
2. Even if net quantity is zero, price divergence creates risk.
3. Basis widening introduces hedge imperfection.
4. Volatile basis increases inventory risk.
5. Fair value models must account for cross-venue spread.

**Funding & Derivative Risk -**
1. Spot and perpetual futures differ due to funding.
2. Long spot and short perp may appear price-neutral.
3. Funding payments create additional exposure.
4. Inventory becomes multidimensional:
   - Price risk.
   - Funding risk.
   - Basis risk.
5. Ignoring funding creates structural PnL drift.

**Liquidity & Operational Risk -**
1. Liquidity may differ across exchanges.
2. If one venue halts trading, hedge may fail.
3. Exchange-specific risk impacts inventory stability.
4. Capital allocation affects quoting aggressiveness.
5. Inventory risk includes operational and counterparty components.

**Fair Value Adjustment Across Venues -**
1. Fair value should reflect leading price discovery venue.
2. Weighted multi-exchange pricing reduces arbitrage risk.
3. Stable basis may not require spread widening.
4. Volatile basis may require:
   - Spread widening.
   - Stronger skewing.
5. Cross-venue models function as distributed price engines.

**Core Insight -**
1. Price-neutral does not mean risk-neutral.
2. Inventory risk extends beyond raw position size.
3. Professional crypto market making is portfolio-based.
4. Risk must be evaluated across:
   - Venues.
   - Instruments.
   - Correlation structures.
5. Multi-venue inventory control is essential for scalability.

---

### Level 17 — Risk Management

*(Pending.)*

---

### Level 18 — Operations

*(Pending.)*

---

### Level 19 — Business Economics

*(Pending.)*

---

### Level 20 — Institutional Reality

*(Pending.)*

---

### Standalone Terminology Entries — pending fold into home levels

> Fold routing: EWMA / Distribution → Level 14 · Market Regime → Level 15 ·
> CVaR99 → Level 17 · Defensive Alpha → Level 15.
> (VPIN / OFI / p_tox / TailScore / Adverse Markout — folded into Level 6, 2026-08-09.)

#### EWMA — Exponentially Weighted Moving Average

A regular average treats all data points equally — a trade from 10 minutes ago counts as much as a trade that just happened. EWMA says: recent data matters more than old data. Each new data point gets high weight. Older points decay.

```
Trade 1: buy  (+1) → EWMA = +1.0
Trade 2: buy  (+1) → EWMA = +0.9   (old value decayed slightly)
Trade 3: sell (-1) → EWMA = +0.5   (sharp drop but prior buys still matter)
Trade 4: buy  (+1) → EWMA = +0.7   (recovering)
Trade 5: sell (-1) → EWMA = +0.3
```

The decay speed is controlled by lambda (λ):
- λ = 0.99 → slow decay — old trades still matter for a long time, smoother signal
- λ = 0.50 → fast decay — recent trades dominate almost immediately, noisier signal

**Why EWMA instead of a simple average?**
Markets change. A burst of buying 20 minutes ago is less relevant than a burst 5 seconds ago. A simple average treats them identically. EWMA keeps the model responsive to current conditions without overreacting to individual noisy ticks.

Used throughout market making:
- Flow adjustment (Layer 0): EWMA of trade sign detects stealth accumulation
- Toxicity model: EWMA of adverse drift tracks whether recent fills are getting more or less toxic
- Volatility estimation: EWMA of |returns| tracks short-term vs long-term volatility regime

---

#### Market Regime

Regime means: what mode is the market in right now? A market maker faces completely different conditions depending on the regime. Three regimes matter:

**Quiet** — low volume, random noise trading, no directional pressure. Fills are mostly clean. Adverse markouts are small. Best environment for a market maker — earn spread, low adverse selection risk.

**Normal** — some directional activity but mixed. Moderate informed flow mixed with noise. Fills are sometimes toxic, sometimes clean. Engine needs to be careful but can still participate profitably.

**Informed** — someone knows something. Strong directional flow, high VPIN, aggressive accumulation or liquidation. Fills in this regime are almost always toxic. Quoting normally here means every fill moves against you.

**Regime is not directly observed — it is classified from signals.** VPIN is the primary classifier in most systems. High VPIN → informed regime. Low VPIN → quiet. The classification is only as good as the signal.

**Why regime matters for markout analysis**: the regime at the moment of the fill is the context for that fill's outcome. A -15 tick adverse move in an informed regime is expected — the signal should have warned you. A -15 tick adverse move in a quiet regime is a surprise — something your model missed. Bucketing fills by regime separates what the model should have handled from what it could not have predicted.

---

#### Distribution

A distribution is the full picture of a set of values — not just the average, but where most values cluster, how spread out they are, and how extreme the worst cases get.

In market making, "markout distribution" means: if you plot all your 100ms adverse moves across every fill in a session, what does that picture look like?

```
Most fills:   -2 to -5 ticks   ← clustered here, this is normal
Some fills:   -10 to -15 ticks ← less frequent
Rare fills:   -30 to -50 ticks ← the tail — infrequent but severe
```

**Why the average alone is not enough**: two assets can have the same average adverse move but completely different distributions. One has consistent small losses (-5 ticks every fill). The other has mostly clean fills but occasional -50 tick disasters (same average, completely different risk). The tail is what kills a market maker — not the average.

**Distribution shift**: when the distribution of recent fills starts moving — the average worsens, the tail gets heavier — that is a signal that market conditions have changed. A professional engine detects this shift within a session and widens spread before more fills arrive in the new, worse distribution.

---

#### CVaR99 — Conditional Value at Risk at 99th Percentile

Regular average tells you the typical adverse move. CVaR99 tells you: in the worst 1% of fills on this asset, what is the average loss?

```
100 fills on SUI:
- 99 fills: average adverse markout = -5 ticks
- 1 worst fill: -80 ticks

CVaR99 = -80 ticks  ←  the tail loss, not the average
```

Why the tail matters more than the average in market making: a system with good average but fat tail is sitting on a time bomb. You can have 1000 profitable fills and one fill that wipes them all out. CVaR99 specifically measures the severity of the worst cases.

CVaR99 differs per asset because book depth differs:
- Deep books (AAVE, LINK): large moves are rare, CVaR99 relatively small
- Thin books (SUI, TRUMP, NEO): when someone sweeps the book, the move is violent, CVaR99 much larger

A system that ignores CVaR99 and only tracks average adverse move will systematically underprice risk on thin-book assets.

---

#### Defensive Alpha (Expected Value Protection Layer)

A professional market making system must continuously evaluate whether providing liquidity is profitable under current market conditions. Defensive alpha is the layer that estimates adverse selection risk and prevents participation in negative expected value states.

This layer converts microstructure signals into an expected value (EV) estimate and uses it to control participation and pricing decisions in real time.

**Core Objective -**  
Ensure the system only trades when:

EV (Expected Value per fill) > 0

**Key Equation -**

EV = Half Spread − Expected Adverse Move (EAM)

Where:

- Half Spread = reward for providing liquidity  
- EAM = expected loss due to informed order flow  

**Toxicity Modeling (Adverse Selection Estimation) -**

Defensive alpha estimates EAM using three complementary signals:

1. **Flow Toxicity (Leading Signal)**  
   Measures persistence of aggressive order flow.

   - flow = EWMA(trade_sign)  
   - tox_flow = |flow|

   Interpretation:  
   High → informed directional flow  
   Low → random / neutral flow  

   Purpose:  
   Detects adverse selection before price movement.

2. **Drift Toxicity (Realized Signal)**  
   Measures actual price movement after a fill.

   - drift = (mid_after − fill_price) × fill_side  
   - tox_drift = max(0, −drift)

   Interpretation:  
   Negative → adverse selection  
   Positive → favorable fill  

   Purpose:  
   Confirms whether fills were toxic.

3. **Volatility Risk (Uncertainty Signal)**  
   Measures instability of fair value.

   - sigma_short = EWMA(|returns|, fast)  
   - sigma_long  = EWMA(|returns|, slow)  
   - tox_vol = sigma_short / sigma_long  

   Interpretation:  
   ≈1 → stable  
   >1.5 → elevated risk  
   >2 → unstable  

   Purpose:  
   Scales magnitude of potential adverse move.

**Combined Toxicity Model -**

toxicity =  
w1 × tox_flow +  
w2 × tox_drift +  
w3 × tox_vol  

**Expected Adverse Move -**

EAM = k_tox × toxicity  

**Expected Value -**

EV = half_spread − EAM  

**System Integration -**

1. **Participation Control**  
   order_qty *= f(EV)

   - EV > 0 → full participation  
   - EV ≈ 0 → reduced participation  
   - EV < 0 → minimal / no trading  

2. **Spread Adjustment**  
   spread *= (1 + k × max(0, −EV))

**System Role in Architecture -**

This layer operates inside the continuous feedback loop and directly influences:

- Participation  
- Spread width  
- Fill quality  

It connects:

- Market Data Layer → inputs (flow, trades, price)  
- Quote Engine → outputs (order size, spread)  

**Behavioral Interpretation -**

- Flow → “something is happening”  
- Drift → “it already hurt”  
- Volatility → “it can hurt more”  

**Key Properties -**

- O(1) computation (latency safe)  
- Event-driven (per fill + rolling updates)  
- Self-adaptive across assets  

**Common Pitfalls -**

- Using flow alone (too noisy)  
- Using drift alone (too lagging)  
- Using absolute volatility instead of relative  
- Hard thresholds instead of EV-based control  

**Final Insight -**

Defensive alpha does not create profit.  
It ensures the system only trades when the spread compensates for adverse selection.

---

## Market making Profitability

> KCMME-specific deep-dive (Layers 0–13, complete 2026-07-09) — the applied
> record of why the engine was GPNL-negative. Canonical concept depth lives
> in the Lifetime Depth section above.

---

### Layer 0 — Fair Value / Microprice Quality

**Status: ✅ Done**

---

**What It Is**

A market maker needs one thing before placing any quote: an internal estimate of what the asset is actually worth right now. This is called **fair value**.

Every quote is placed around this number:
- Bid = fair_value − half_spread
- Ask = fair_value + half_spread

If fair value is wrong, the quote is wrong. A wrong quote causes adverse selection even if every other signal is perfect — because you are quoting at the wrong price, not because the counterparty is informed.

Key distinction: adverse selection from informed flow and adverse selection from stale fair value look identical in markout data but have completely different fixes. Confusing the two leads to widening spreads when the real fix is improving fair value accuracy.

---

**Why Raw Mid Is Incomplete**

Imagine a physical market — a fruit stall. Seller has 200 mangoes at ₹100. One buyer wants 1 mango at ₹99. Mid = ₹99.50.

Now 50 more buyers arrive, all wanting mangoes at ₹99. Suddenly 50 buyers, 1 seller. True value just went up — demand swamped supply. But mid is still ₹99.50. It didn't move. Mid is blind to imbalance because it only looks at the best price on each side, not how much is sitting there.

---

**Microprice — Why the Formula Makes Sense**

```
Ask: 100.10  (qty = 50)   ← only 50 sellers
Bid:  99.90  (qty = 200)  ← 200 buyers waiting
```

Ask: what is more likely to happen next?
- A market sell hits the bid at 99.90 → price stays or goes down
- A market buy hits the ask at 100.10 → price goes up

There are 200 units of buy intent and only 50 units of sell intent. The next aggressive order is statistically more likely to be a buy. Price is more likely to move toward 100.10 than 99.90 — before any trade happens.

Microprice captures this:
```
microprice = (bid_qty × ask_price + ask_qty × bid_price) / (bid_qty + ask_qty)
           = (200 × 100.10 + 50 × 99.90) / 250
           = 100.06
```

Why multiply bid_qty by ask_price? Because large bid_qty means high probability of upward movement — so it pulls the estimate toward the ask. Think of each unit of volume as a vote: every bid-side unit votes that price goes to the ask, every ask-side unit votes that price goes to the bid. The vote count determines fair value.

Sanity check — when does microprice equal mid?
```
bid_qty = ask_qty = 100:
microprice = (100 × 100.10 + 100 × 99.90) / 200 = 100.00 = mid
```
Perfectly balanced book → microprice = mid. Makes complete sense.

What microprice still misses: it only sees your own venue's book right now. It has no idea what's happening on Binance.

---

**Cross-Venue — Why It Matters**

You are a market maker on Bybit, quoting SOL at 100.00 / 100.10.

At 10:00:00.000, a large hedge fund decides to buy 50,000 SOL. They go to Binance first — most liquidity, tightest spread. They buy aggressively. Within 200ms, Binance SOL moves from 100.00 to 101.00.

On Bybit, nothing has happened yet. Your book still shows 99.90 / 100.10. Your fair value based on Bybit's book: 100.00.

At 10:00:00.200, an arbitrageur sees:
- Binance SOL: 101.00
- Bybit SOL (your ask): 100.10

He buys from you at 100.10 and sells on Binance at 101.00. Free 90 cents per SOL.

From your side: you got filled on your ask. Price then jumps to 101.00 on Bybit too. Your 1-second markout shows a 90-tick adverse move. Looks like toxic informed flow. It was not — the counterparty just read Binance 200ms before your Bybit fair value updated.

The fix: anchor Bybit fair value to Binance. The moment Binance moves to 101.00, your Bybit fair value becomes 101.00 regardless of what Bybit's own book shows. Your ask immediately reprices to 101.10. The arbitrageur finds nothing cheap. You are protected.

Why Binance specifically? Because Binance is where price is discovered first — highest volume, most participants, tightest spreads. Informed traders go there to execute. Other exchanges follow. Binance moves, everyone else catches up.

What cross-venue still misses: stealth accumulation — a large buyer breaking their order into small chunks so the book looks balanced while they accumulate. The book on every venue looks normal but the flow pattern tells a different story.

---

**Flow Adjustment — What Both Above Miss**

Scenario: you have perfect microprice and perfect cross-venue anchor. Order book looks balanced on all venues. Binance matches Bybit. Microprice = mid = 100.00.

But in the last 30 seconds, there have been 15 aggressive buy trades in a row on Binance. Small sizes, but consistently buying. No visible book imbalance because sellers keep replenishing the ask.

What is actually happening? A large trader is buying in small chunks — deliberately spreading the order so it does not move the book too fast. Book looks balanced, but the flow pattern says otherwise.

At the 16th trade, price jumps. The large buyer finishes accumulating and selling pressure runs out. Fair value moves up by 5 ticks.

Microprice missed it — the book looked balanced the whole time.
Cross-venue missed it — Binance book also looked balanced.
Flow adjustment catches it — 15 consecutive aggressive buys is a signal.

How it works: assign +1 to every aggressive buy, -1 to every aggressive sell. Take a running EWMA (recent trades count more than old ones). After 15 consecutive buys, EWMA ≈ +0.8 (strongly positive). This shifts fair value up slightly, repricing your ask. The stealth accumulator finds your quote less cheap.

Why decay? Because markets do not move in one direction forever. After buying pressure stops, EWMA fades back toward zero. Fair value drifts back to neutral. Without decay, one burst of buying would keep fair value elevated for hours — which would be wrong.

---

**How All Three Work Together — Complete Scenario**

SOL/USDT:

**t = 0** — Everything calm, balanced books everywhere.
```
Binance: 100.00 / 100.10  (balanced)
Bybit:   100.00 / 100.10  (balanced)

Raw mid:     100.05
Microprice:  100.05   (balanced = same as mid)
Cross-venue: 100.05   (Binance matches Bybit)
Flow signal: 0.0      (no directional trades)

Fair value:  100.05
```

**t = 100ms** — Large buyer starts accumulating on Binance in small chunks.
```
Binance: 15 aggressive buys, book still looks balanced (sellers replenishing)
Bybit:   unchanged

Microprice:  100.05  (Bybit book still balanced)
Cross-venue: 100.05  (Binance price not moved yet)
Flow signal: +0.6    (15 consecutive buys detected)

Fair value shifts to: 100.07
Your ask reprices:    100.17  (instead of 100.10)
```

**t = 200ms** — Buying accelerates. Binance ask side starts thinning.
```
Binance: 100.00 / 100.20  (asks being consumed)
Bybit:   100.00 / 100.10  (lagging)

Microprice:  100.05  (Bybit book still balanced)
Cross-venue: 100.10  (Binance mid now higher)
Flow signal: +0.85

Fair value:  100.12
Your ask:    100.22
```

**t = 350ms** — Binance jumps to 100.80 as the buyer clears the book.
```
Binance: 100.70 / 100.90
Bybit:   still showing 100.00 / 100.10

Microprice:  100.05  (Bybit book has not caught up)
Cross-venue: 100.80  (Binance is the truth)
Flow signal: +0.95

Fair value:  100.80
Your ask:    100.90
```

Without cross-venue: your ask is at 100.10 when it should be 100.90 → arbitrageur takes 70 ticks from you → markout shows massive adverse move → looks like toxic flow → real cause was stale fair value.

With all three layers active: your ask reprices continuously as each signal fires. By the time the arbitrageur looks, it is already at 100.90. Nothing cheap to take.

---

**What Each Layer Sees vs Misses**

| Method | What it sees | What it misses |
|---|---|---|
| Raw mid | Best bid and ask price | Book imbalance, cross-venue moves, flow |
| Microprice | Book imbalance on your venue | Cross-venue moves, stealth accumulation |
| Cross-venue | Price discovery on other exchanges | Stealth accumulation within one venue |
| Flow adjustment | Pattern of recent aggressive trades | Anything visible in the book |

They are not alternatives — they are layers. Each catches something the others are blind to. A professional engine runs all four simultaneously.

---

**Professional Standard — Jane Street / Citadel Level**

| Component | What they do |
|---|---|
| Base estimate | Microprice — always, non-negotiable minimum |
| Cross-venue anchor | All major venues merged; anchor to price leader |
| Flow adjustment | Trade sign EWMA + OFI, decaying over time |
| Volatility scaling | Fair value uncertainty widens in high-vol regimes |
| Update speed | Sub-millisecond, every book update |

Key property: their fair value is predictive, not reactive. It shifts before price jumps because it reads pressure signals building in the book and flow — not after price has already moved.

---

**Summary**

| | |
|---|---|
| **What it is** | Engine's internal estimate of where the asset should trade right now |
| **Why it matters** | Every quote anchors here — wrong anchor = adverse selection regardless of other signals |
| **Professional standard** | Microprice + cross-venue + flow adjustment + vol scaling, sub-ms updates |

---

### Layer 0.5 — Potemkin Check / Engine vs Infra Metric

**Status: ✅ Done**

---

**What It Is**

Before analysing any session data — fills, markouts, adverse selection — you need to answer one question: did the engine's orders actually reach the exchange?

This sounds obvious. It is not. An engine can log hundreds of order dispatches while the exchange received zero of them. Everything inside the engine looks healthy. The logs look normal. But nothing actually happened on the venue side.

This is called a **Potemkin** — named after Prince Potemkin who built fake village facades to impress Catherine the Great during her Crimea tour. Thriving villages from the outside. Nothing behind them.

In trading: engine logs show 100 dispatches. Exchange records show 0 placements. From inside the system, everything looks fine. Behind the facade: the engine was quoting into the void.

---

**Why This Must Come Before Markout Analysis**

If you run markout analysis on a Potemkin session, you are analysing ghost data. The fills may be real but the context — all the orders that "were placed" but never reached the exchange — is fabricated. Your adverse selection statistics are wrong. Your EV calculations are wrong. Everything downstream is built on fiction.

Tuning adverse selection parameters based on Potemkin data is like a doctor adjusting medication doses based on a broken thermometer. The actions feel logical but the inputs are invalid.

---

**The Two Metrics**

Every action the engine takes has two observable points:

- **Engine metric** — what did the engine decide to do? Measured inside the engine: dispatch counters, order logs. "I sent 100 order placement requests."
- **Infra metric** — what did the venue actually do? Measured at the exchange: REST API order history. "I received and processed 60 order placements from your account."

Healthy system: engine metric ≈ infra metric. Small gap is normal.
Potemkin system: engine metric = 100, infra metric = 0. Complete divergence.

---

**The Gate Check**

Cross-reference engine claims against exchange REST API before trusting any session:

```
Gap = |engine_claimed - exchange_received| / engine_claimed

Gap < 25%  → session trustworthy, proceed with analysis
Gap ≥ 25%  → Potemkin, stop, categorise, fix before analysing
```

Why 25%? Some gap is always normal — order rejections, timing, partial fills. Under 10% is typical noise. Over 25% means something structural broke, not just noise.

Also check position state:
```
Engine believes: long 5 SUI on Bybit
Bybit REST API:  0 open positions

→ Engine's position belief is wrong → all inventory calculations invalid
```

---

**Five Potemkin Types — Categorisation**

When a session fails the gate, you do not need deep research to know what type it is. The axis of divergence tells you immediately:

**Type A — Total Silence**
```
Engine sent: 500    Exchange received: 0
```
Nothing left the system. Causes: dead WebSocket, wrong endpoint, auth failure, test mode left on. Fix is in connectivity or configuration.

**Type B — Rate Limit Potemkin**
```
Engine sent: 500    Exchange received: 300
(first 300 fine, then exchange started rejecting)
```
Engine hit the venue's per-minute rate limit. Exchange returned error codes. Engine logged "sent" without properly checking the response. Fix is in rate limit handling.

**Type C — Symbol / Instrument Potemkin**
```
Engine sent: 500 orders for "SUIUSDT"
Exchange received: 0  (venue expects "SUI-USDT-PERP")
```
Orders routed to a symbol that does not exist. Exchange returned rejection, engine misread it as success. Fix is in symbol mapping.

**Type D — Fill Reconciliation Potemkin**
```
Placed count: matches ✓
Engine fill log: 23 fills    Exchange fill history: 15 fills
```
Orders reached the exchange and were placed correctly. But fills did not reconcile back into the engine properly — missed fill events, wrong fill tracking. Fix is in the fill reconciliation layer, not dispatch.

**Type E — Position State Drift**
```
Placed count: matches ✓    Fill count: matches ✓
Engine believes: long 5 SUI    Bybit REST: 0 open positions
```
Subtler. Individual fills tracked but position ledger drifted over time — wrong direction, missed close, ghost carry from previous session. Fix is in position state management.

---

**Quick Category Identification**

```
placed_count diverges heavily        → Type A, B, or C  (dispatch problem)
placed_count matches, fills diverge  → Type D           (fill reconciliation problem)
fills match, position diverges       → Type E           (position state drift)
```

Category identification is a 2-minute check — just look at which number diverges. The root cause investigation is deeper work done in research and log analysis cycles.

---

**When Each Step Happens**

| When | What you do |
|---|---|
| Before any session analysis | Run the 25% gate — pass or fail |
| Session fails the gate | Quick category identification — which axis diverges? |
| Category identified | Root cause investigation → research and log analysis work |

---

**Summary**

| | |
|---|---|
| **What it is** | Verification that engine orders actually reached the exchange before trusting any session data |
| **Why it matters** | Markout analysis on Potemkin data produces wrong conclusions — wrong inputs, wrong fixes |
| **The gate** | Gap < 25% → trust session. Gap ≥ 25% → stop, categorise, fix |
| **Quick category** | Which axis diverges: placed / fills / position → points to dispatch / reconciliation / state |
| **Deep fix** | Research and log analysis time — not session analysis time |
| **Professional standard** | Every session validated against exchange REST truth before any analysis runs |

---

### Layer 1 — Fill Markout Analysis

**Status: ✅ Done**

---

**What It Is**

A markout is the price movement against you after a fill, measured at fixed time horizons. After the engine is filled on its bid — say, buying SOL at 100.00 — you measure where SOL trades at 100ms later, 500ms later, 1s later, 5s later. If SOL is at 99.85 at 100ms, the 100ms markout is -15 ticks: the fill immediately moved against you.

Markout analysis tells you whether your fill was profitable, on average, at each horizon. If average adverse move at 100ms is larger than your half-spread, you are losing money on every fill before the second leg even has a chance to execute.

Without markouts, everything else is guessing. You can have a spread, a toxicity signal, an inventory controller — but if you do not measure what actually happens after each fill, you cannot know whether the spread is wide enough, whether the toxicity signal is working, or where the loss is really coming from.

---

**Why the Naive Approach Fails**

The naive approach is to look at session gpnl and ask "did we make or lose money?" This tells you nothing.

Suppose a session shows: 200 fills, net gpnl −$3.00. That is the total. But you do not know:
- Were fills toxic at the 100ms horizon and we recovered at 5s? (Short-term adverse, long-term ok)
- Were fills fair at 100ms but inventory carried against us over 30 minutes? (Not a fill problem — an inventory problem)
- Were half the fills clean and half catastrophically toxic? (Average masks the tail)
- Was it two assets doing well and one destroying everything? (Asset-level mask)

Without markouts, the answer to "what's causing the loss?" is a guess. With markouts, it becomes a calculation.

---

**Building Layers — From Simple to Professional**

**Layer 1a: Average markout per horizon**

The first step: compute the average post-fill price move at each horizon for every fill in a session.

```
SOL bid fill at 100.00
  t+100ms: price = 99.85  →  markout = -15 ticks (adverse)
  t+500ms: price = 99.80  →  markout = -20 ticks
  t+1s:    price = 99.82  →  markout = -18 ticks
  t+5s:    price = 99.95  →  markout = -5 ticks
```

Average over 200 fills:
```
  avg_100ms: -8 ticks   ← was the fill sniped? 
  avg_500ms: -6 ticks   ← short-term informed flow
  avg_1s:    -4 ticks   ← flow persistence
  avg_5s:    -1 tick    ← inventory carry pressure
```

If half-spread = 5 ticks:
```
fill_ev = half_spread - adverse_markout
at 100ms: 5 - 8 = -3 ticks  ← negative EV per fill at this horizon
at 5s:    5 - 1 = +4 ticks  ← positive EV if held to 5s
```

This tells you: the fills are being sniped at 100ms but market mean-reverts by 5s. The problem is not fills being toxic — it is that the engine cannot hold inventory to 5s without being stopped out by skew pressure or inventory limits.

**What this still misses**: the average may be distorted. 190 clean fills and 10 catastrophic fills would show an "average" that looks fine while hiding a tail loss pattern. And you have no idea whether the 10 catastrophic fills had a detectable signal beforehand.

---

**Layer 1b: Bucketing fills by signal state (VPIN buckets)**

The average markout is a start. The professional question is: does your toxicity signal actually predict which fills will be toxic?

Divide all fills into three buckets based on what the VPIN signal was at the moment of fill:
- **Quiet regime** (VPIN < 0.3): low informed flow, mostly noise
- **Normal regime** (VPIN 0.3–0.7): mixed, some directional pressure
- **Informed regime** (VPIN > 0.7): strong directional flow, high toxic risk

Now compute average markout per bucket:

```
                  avg_100ms_markout    avg_1s_markout
Quiet regime:        -2 ticks             -1 tick     ← nearly clean
Normal regime:       -6 ticks             -4 ticks
Informed regime:    -18 ticks            -12 ticks    ← deeply toxic
```

What this tells you:
1. The informed-regime fills are terrible — -18 ticks at 100ms with 5 tick half-spread = -13 tick net loss per fill in that bucket
2. The quiet-regime fills are nearly profitable — -2 ticks adverse vs 5 tick half-spread = +3 tick net
3. The VPIN signal actually predicts toxicity: markouts clearly separate across buckets

This means: if you widen spread or reduce size only in the informed regime, you stop the bleeding without touching the clean fills. The signal is usable.

But what if the buckets do NOT separate?

```
                  avg_100ms_markout
Quiet regime:        -7 ticks
Normal regime:       -8 ticks
Informed regime:     -9 ticks   ← almost no separation
```

The VPIN signal is not predicting toxic fills on this asset. Widening spread based on VPIN here helps nothing — you would widen on clean fills and miss the actual toxic ones. For this asset, VPIN is noise. You need a different signal, a different horizon, or a different strategy.

Bucketing is how you know whether your toxicity signals are actually working — not whether they are theoretically correct, but whether they separate observed outcomes in practice.

**What this still misses**: you are looking at your own historical session data. You are learning which fills were toxic after the fact. You are not yet using this learning to adjust the spread in real time while the session is running.

---

**Layer 1c: Per-asset markout distributions as a live model**

This is the professional standard. Instead of running markout analysis once after a session ends, the engine maintains a live distribution of past markouts per asset and uses it to set spreads continuously.

Concretely: the engine tracks the last N fills for SOL and maintains a rolling estimate of average adverse move at 100ms and 1s horizons. Each new fill updates the estimate. The spread is then set as:

```
half_spread ≥ expected_adverse_move_at_1s × safety_margin
```

If the last 50 SOL fills show an average 1s adverse move of 8 ticks, the engine widens SOL spread to at least 8–10 ticks. If the distribution starts improving (fills become less toxic), the spread can tighten. If the distribution worsens (regime shift, more informed flow), the spread automatically widens.

**The shift response**: this is the critical behaviour. If the distribution of adverse moves suddenly shifts — say, the last 20 fills start showing -20 ticks at 100ms when the historical norm is -5 ticks — the engine detects this shift and widens spread within the same session. It does not wait for the session to end and a researcher to run analysis.

A concrete scenario:
```
SOL: 10:00–10:30 — calm regime, avg 100ms markout = -3 ticks
SOL: 10:30–10:35 — someone starts accumulating aggressively
  fill 1: -8 ticks
  fill 2: -12 ticks
  fill 3: -15 ticks
  fill 4: -18 ticks
```

Distribution shifts. By fill 4, the live model detects a regime change. Spread widens automatically — before fill 5 happens. The engine is not reacting to fill 5 being bad. It is pricing in the fact that the distribution has shifted.

Without live markout distributions, the spread stays the same through fills 1–100. You only find out 30 minutes later that the regime had shifted at fill 4, and by then the damage is done.

---

**What Each Layer Sees vs Misses**

| Method | What it sees | What it misses |
|---|---|---|
| Session gpnl total | Whether we made or lost money | Why, which fills, which assets, which horizon |
| Average markout per horizon | Whether fills are toxic on average | Tail risk, signal quality, regime sensitivity |
| VPIN-bucketed markouts | Whether signal predicts toxic fills | Real-time feedback — this is post-session analysis |
| Live markout distribution | Regime shifts within a session | Nothing at the individual fill level — it is aggregate |
| Live distribution + signal buckets | Both regime and signal quality, continuously | Gaps in coverage when fills are sparse (thin assets) |

---

**Professional Standard — Jane Street / Citadel Level**

| Component | What they do |
|---|---|
| Markout horizons | Multiple horizons: 10ms, 100ms, 500ms, 1s, 5s, 30s — each measured separately |
| Signal-state bucketing | Fills are tagged at fill time with full signal state (VPIN, OFI, imbalance, regime) |
| Live distribution model | Rolling distribution per asset × signal-state bucket, updated each fill |
| Spread setting | Half-spread ≥ live-modelled expected adverse move at 1s horizon, with safety margin |
| Automatic regime response | When distribution shifts beyond threshold → spread widens before next fill, not after |
| Attribution | Every fill attributed: spread_captured / adverse_markout / inventory_carry — distinguishable in real-time |

Key property: markout analysis is not a post-session diagnostic. It is a continuous live model that drives spread decisions in the same session. The engine learns what this asset's fills look like today and prices accordingly — not based on last month's calibration.

---

**Summary**

| | |
|---|---|
| **What it is** | Price movement against the fill direction at fixed time horizons — the direct measurement of adverse selection cost |
| **Why it matters** | Without markouts, you cannot know whether spread covers adverse risk, whether signals work, or why gpnl is negative |
| **Core equation** | fill_ev = half_spread − adverse_markout; negative = losing money on every fill |
| **Signal validation** | Bucket fills by VPIN/signal state; if buckets do not separate — signal is not predicting toxicity on that asset |
| **Professional standard** | Live rolling distribution per asset, auto-widens spread when distribution shifts — not post-session analysis |

---

### Layer 2 — Adverse Selection / TailScore

**Status: ✅ Done**

---

**What It Is**

Layer 1 measured what happened after a fill — backward-looking damage assessment. Layer 2 is the forward-looking version: can you predict which fills will be toxic before they happen, and price them accordingly?

If you can — even partially — you stop losing money on the worst fills instead of just measuring the loss afterward. This is the biggest single profitability lever in market making.

---

**Why the Naive Approach Fails**

The naive approach: set one spread for the whole session. Every fill gets the same half-spread. Clean fills earn spread. Toxic fills lose more than spread. Hope the average works out.

Real-world analogy: a taxi driver who charges every passenger the same flat rate regardless of destination. Short rides to safe neighbourhoods subsidise dangerous 3am rides. Eventually the dangerous rides bankrupt the business.

In market making: quoting the same spread regardless of whether conditions look calm or informed is charging the same price for completely different risk levels. The fix is not a wider spread everywhere — that kills fill rate on the clean fills. The fix is a wider spread specifically when a toxic fill is likely, and a tighter spread when conditions are calm.

That requires predicting toxicity before the fill.

---

**Layer 2a — p_tox: Pricing the Probability**

Three signals, each detecting toxicity from a different angle:

**Signal 1 — Flow toxicity (leading signal)**
```
flow     = EWMA(trade_sign)      +1 per aggressive buy, -1 per aggressive sell
tox_flow = |flow|                how one-sided is recent aggressive flow?
```
Fires before price moves — detects the pattern of who is trading.

**Signal 2 — Drift toxicity (realized signal)**
```
drift     = (mid_after_fill - fill_price) × fill_side
tox_drift = max(0, -drift)       counts only adverse moves, not favourable ones
```
Backward-looking confirmation — recent fills actually hurt, not just theory.

**Signal 3 — Volatility risk (uncertainty signal)**
```
tox_vol = sigma_short / sigma_long
```
When short-term volatility exceeds long-term volatility, fair value is jumping around. Even without directional flow, an unstable fair value increases expected adverse move on any fill.

Combined:
```
toxicity = w1 × tox_flow + w2 × tox_drift + w3 × tox_vol
EAM      = k_tox × toxicity
EV       = half_spread − EAM
```

**What this still misses**: p_tox gives probability of a toxic fill. It says nothing about how bad the fill will be when it happens. A 70% chance of -2 ticks and a 70% chance of -50 ticks are treated identically. They are not.

---

**Layer 2b — TailScore: Adding Severity**

```
TailScore = p_tox × CVaR99_magnitude
delta_adv = k_tox × p_tox × q̂99    ← drives spread widening directly
```

Concrete example. Two assets, same p_tox:
```
LINK: p_tox = 0.6,  CVaR99 = -8 ticks   →  TailScore = 4.8
SUI:  p_tox = 0.6,  CVaR99 = -40 ticks  →  TailScore = 24.0
```

Same toxicity probability. Completely different tail risk. SUI's thin book means when someone sweeps through, the move is violent. A system using only p_tox treats them identically. TailScore sets a much wider SUI spread and reduces size significantly.

TailScore drives spread continuously — not a binary gate. High TailScore → spread widens proportionally, size reduces. The engine always quotes; it just prices the risk correctly.

---

**Layer 2c — Toxic Fill Clustering**

Toxic fills do not arrive randomly — they cluster. An informed trader does not send one order. They have a position to build before price moves. They send 10, 50, 100 orders in the same direction over minutes.

This means: after one toxic fill, the probability of the next fill being toxic is higher than baseline. The trader is still out there.

```
Fill 1: bid fill, -12 tick adverse at 100ms
Fill 2: bid fill, -15 tick adverse at 100ms  ←  still the same trader?
Fill 3: bid fill, -18 tick adverse at 100ms  ←  almost certainly yes
```

A naive system treats each fill independently — p_tox resets to baseline after each fill. A professional system detects the cluster: three adverse fills in a row is a signal. p_tox should rise after each adverse fill, not reset.

This is why tox_drift exists as a signal — it captures the fact that recent fills were adversely selected and keeps that information alive in the model, decaying slowly via EWMA. One bad fill raises tox_drift → raises p_tox → raises spread for the next fill.

---

**Why Global Thresholds Fail**

One global TailScore threshold applied to all assets is structurally wrong:
```
SUI:  thin book, violent moves, CVaR99 = -40 ticks
AAVE: deep book, slow moves,   CVaR99 = -6 ticks
```

Calibrate to AAVE → SUI will blow through the threshold on every regime shift. Calibrate to SUI → AAVE almost never quotes. Each asset needs its own CVaR99 baseline, its own TailScore threshold, its own signal sensitivity.

---

**What Each Layer Sees vs Misses**

| Method | What it sees | What it misses |
|---|---|---|
| Fixed spread, no toxicity model | Simple to implement | Same price for different risk levels — toxic fills bleed the clean ones |
| p_tox only | Probability of toxic fill | Severity — 70% toxic at -2 ticks vs -50 ticks treated identically |
| TailScore (p_tox × CVaR99) | Probability AND severity per asset | Clustering — treats each fill as independent |
| TailScore + clustering detection | Probability, severity, temporal pattern | Per-asset calibration — global thresholds wrong for thin vs deep books |
| Full system: all four layers | All of the above | Nothing structural — this is the professional standard |

---

**Professional Standard — Jane Street / Citadel Level**

| Component | What they do |
|---|---|
| Toxicity signals | Flow + drift + vol combined; weights calibrated per asset, not global |
| Severity measurement | CVaR99 per asset computed from live session data, updated continuously |
| TailScore | Drives spread and size continuously — not a binary gate |
| Clustering | tox_drift EWMA decays slowly — one adverse fill raises p_tox for the next fill |
| Per-asset calibration | Each asset has its own CVaR99 baseline and TailScore threshold |
| Response | Continuous: spread widens proportionally, size reduces — never a hard stop |

Key property: the system never stops quoting. When TailScore is extreme it quotes with a very wide spread and minimal size — not zero. Removing liquidity entirely is an institutional anti-pattern.

---

**Summary**

| | |
|---|---|
| **What it is** | Forward-looking prediction of fill toxicity — probability × severity — used to price risk before the fill arrives |
| **Why it matters** | Stops the worst fills from bleeding out the clean ones; biggest single profitability lever |
| **Core equation** | TailScore = p_tox × CVaR99; delta_adv = k_tox × p_tox × q̂99 drives spread |
| **Clustering** | Adverse fills raise p_tox for subsequent fills via tox_drift EWMA — not independent events |
| **Professional standard** | Per-asset CVaR99 live model + per-asset TailScore threshold + continuous proportional spread response |

---

### Layer 3 — Latency / Stale Quote Exposure

#### What It Is

A stale quote is a resting order on the exchange whose price no longer reflects fair
value — because fair value moved on another venue, but the cancel has not yet reached
the exchange.

The stale window is the gap between when price moves and when the cancel is confirmed:
```
t=0ms:   fair value shifts on Binance
t=Xms:   engine detects the shift, sends cancel to Bybit
t=Yms:   exchange confirms cancel (cancel ack)

Stale window = t=0ms to t=Yms
```

During this window the quote is live and fillable at the wrong price. An arbitrageur
watching both venues fires an aggressive order the moment they see the divergence —
often within 1ms. If their order arrives at the exchange before the cancel, they fill
at the stale price and immediately hedge on Binance at the new fair value.

This loss looks identical to informed flow in markout data. Both produce large adverse
moves after a fill. The cause is completely different — and so is the fix.

---

#### Why the Naive Approach Fails

Naive: set a spread and assume any adverse fill was from informed flow. Blame the
counterparty for having an edge.

Analogy: a shop owner puts yesterday's price tag on inventory and goes to the back
room. Customers buy everything at below-current value. The owner returns and blames
"smart customers who knew prices would rise." They knew nothing. He left a stale price
visible and did not update it fast enough.

The arbitrageur needs no information advantage. They just read two venues simultaneously
and act faster than the cancel travels to the exchange.

---

#### The Three Components of the Stale Window

```
Total stale window = detection lag + network RTT + exchange processing time
```

**Detection lag**: how long before the engine notices fair value shifted from the
incoming L2 update. Depends on engine processing speed.

**Network RTT**: how long the cancel request takes to travel to the exchange and
for the ack to return. At AWS Tokyo: ~22ms round trip to Bybit/BitMEX. At old
Delta India setup: 750–1000ms — stale window was 75× larger.

**Exchange processing time**: how long the exchange queues and processes the cancel
before matching is updated. This is the same for the market maker's cancel and the
arb's aggressive order — whoever arrives first at the exchange queue wins.

---

#### Quantifying Stale Fill Loss

```
stale_loss = P(fill before cancel ack) × E[adverse move in the stale window]
```

Concrete example at AWS Tokyo (22ms cancel ack):
```
Fair value moves +20 ticks on Binance
Stale ask on Bybit = 15 ticks below new fair value

P(fill in 22ms window) ≈ 0.85   (quote is cheap enough that arb fires immediately)
E[adverse move] = 18 ticks

stale_loss per event = 0.85 × 18 = 15.3 ticks
```

At 5 such events per session: 76.5 ticks of pure stale loss — before any informed
flow is counted.

---

#### Why 1ms Latency Difference Is Enough

Even a 1ms advantage lets the arb hunt stale quotes:

```
t=0ms:  Binance moves. Both arb and engine detect it simultaneously.
t=0.5ms: Arb (co-located at Bybit) fires aggressive order → arrives at Bybit
t=10ms:  Engine (AWS Tokyo) sends cancel → arrives at Bybit

Gap = 9.5ms. Arb wins the race by 9.5ms.
```

The arb does not predict direction. They see a price difference already existing
across two venues and lock it in by filling both legs simultaneously:
- Leg 1: buy on Bybit at stale price
- Leg 2: sell on Binance at new fair value

Profit is locked in by the cross-venue price difference. No directional bet.
Fees only kill the trade if the move is smaller than ~2–3 ticks — larger moves
are always profitable for the arb regardless of fees.

---

#### Quote Age as the Diagnostic Signal

Without tracking quote age at fill time, stale losses and informed losses look
identical in markout analysis. Both show large adverse moves after a fill.

The separator is `fill_order_age_ms` — how long the quote had been resting at the
exchange before it was filled:

```
Low age fills  (< 50ms):  avg adverse markout = -6 ticks  → informed flow candidate
High age fills (> 500ms): avg adverse markout = -22 ticks → stale pickoff candidate
```

If the large losses cluster at high quote age → the problem is cancel latency and
repricing speed, not informed flow. Improving the toxicity model here helps nothing.
Reducing cancel latency or tightening `max_quote_age_ms` is the fix.

---

#### How Faster Cancel Speed Changes Spread Economics

Faster cancel speed → smaller stale window → smaller expected stale loss → lower
spread floor required to remain EV-positive.

```
AWS Tokyo (22ms cancel ack):    spread floor contribution from stale loss ≈ 3–5 ticks
Delta India (800ms cancel ack): spread floor contribution from stale loss ≈ 30–50 ticks
```

Every millisecond reduction in cancel ack latency is worth a specific number of ticks
in spread tightening. This is why infrastructure investment (co-location, kernel-bypass
networking) translates directly into competitive quoting — not speed for its own sake.

---

#### Sees vs Misses

| Method | What it sees | What it misses |
|---|---|---|
| No latency tracking | Nothing — all adverse moves look like informed flow | Stale losses completely invisible |
| Cancel ack latency only | How long the stale window is | Whether fills actually happen in that window |
| Quote age at fill | Which fills happened on stale quotes | Why the quote was stale (detection lag vs RTT vs exchange) |
| Full decomposition | Detection lag + RTT + exchange processing separately | Nothing structural |

---

#### Professional Standard — Jane Street / Citadel Level

| Component | What they do |
|---|---|
| Detection speed | Sub-millisecond — every L2 update triggers immediate fair value recalculation |
| Cancel speed | Co-located or kernel-bypass — cancel ack in < 1ms |
| Quote age tracking | Every fill tagged with exact quote age at fill time |
| Stale loss attribution | Fills split: stale quote loss vs informed flow — different fixes for each |
| Spread floor | Explicitly derived from measured stale window: `spread ≥ P(fill_before_cancel_ack) × E[adverse_move]` |
| Infrastructure investment | Cancel speed improvement = direct spread tightening = direct EV improvement |

Key property: professionals do not treat latency as a background constraint. They
measure it, attribute losses to it specifically, and invest in reducing it because
the economics are direct.

---

#### Summary

| | |
|---|---|
| **What it is** | Fill risk from a quote whose price is stale because fair value moved faster than the cancel reached the exchange |
| **Why it matters** | Stale fills look identical to informed flow — wrong diagnosis leads to wrong fix |
| **Stale window** | Detection lag + network RTT + exchange processing — all three must be minimised |
| **Key diagnostic** | Quote age at fill time separates stale losses from informed flow losses |
| **Core equation** | stale_loss = P(fill before cancel ack) × E[adverse move in stale window] |
| **Spread implication** | Faster cancel speed directly lowers the spread floor — infra investment = EV improvement |
| **Professional standard** | Sub-ms detection, measured cancel ack latency, explicit stale loss attribution, spread floor set from measured latency |

---

### Layer 4 — Spread vs Adverse Move

#### What It Is

The spread is the only revenue a market maker earns. The adverse move — the price
movement against you after a fill — is the primary cost. If the adverse move exceeds
the half-spread captured at fill time, every fill is a loss.

```
fill_ev = half_spread_captured − adverse_markout
```

Getting the spread right means setting it wide enough to cover the adverse move in
expectation, while keeping it tight enough that fills actually happen. Too tight →
every fill bleeds. Too wide → no fills, no revenue.

---

#### Why the Naive Approach Fails

Naive: pick a spread that "looks competitive" by watching what others quote.

Analogy: a taxi driver sets his fare by looking at what other taxis charge, without
knowing what his fuel costs that day. When fuel is cheap, he profits. When fuel spikes,
every ride loses money — but the meter still reads the same number.

In market making: adverse move is the fuel cost. It changes every session, every
asset, every regime. A fixed spread that works in quiet markets bleeds in volatile
or informed-flow markets. You need a spread that responds to the actual cost of
being filled right now.

---

#### Layer 1 — Half-Spread and the Round-Trip Problem

At fill time you capture half the spread — not the full spread. If you quote
bid=99, ask=101, and the ask fills, you earned 1 tick (half of the 2-tick spread).
The other half only arrives if the bid also fills later. That second leg is never
guaranteed.

```
fill_ev = half_spread − adverse_markout

Example:
  half_spread = 1 tick
  adverse_markout at 1s = 3 ticks
  fill_ev = 1 − 3 = −2 ticks per fill
```

You captured your spread and still lost 2 ticks. This is not bad luck — it is
structural negative EV that repeats on every informed fill.

**What this still misses**: adverse move is not constant. It is much higher during
informed flow and volatile regimes. A single average spread cannot cover a
distribution that has fat tails.

---

#### Layer 2 — Spread Floor

The spread floor is the minimum spread below which EV is structurally negative
regardless of any signal:

```
spread_floor = 2 × E[adverse_markout]
```

The factor of 2 comes from the relationship: half-spread must cover the full adverse
move, and half-spread is half the total spread.

Per asset — because adverse markout differs by book depth:
```
SUI:  avg adverse markout at 1s = 4 ticks → floor = 8 ticks
AAVE: avg adverse markout at 1s = 2 ticks → floor = 4 ticks
LINK: avg adverse markout at 1s = 3 ticks → floor = 6 ticks
```

Quoting SUI at a 5-tick spread when the floor is 8 ticks means every fill is
negative EV in expectation. No signal improvement fixes this — the floor must be
raised first.

**What this still misses**: the floor is computed from an average adverse move.
Adverse move is much higher during volatile regimes — the floor must scale with
current conditions, not historical averages.

---

#### Layer 3 — Volatility-Adjusted Spread

When price is jumping, adverse moves are larger. The spread floor must scale:

```
spread_required = spread_floor_base × vol_multiplier
vol_multiplier  = current_sigma / baseline_sigma
```

Concrete example — SUI across regimes:
```
Quiet  (vol = 0.8× baseline): spread = 8 × 0.8 = 6.4 ticks
Normal (vol = 1.0× baseline): spread = 8 × 1.0 = 8.0 ticks
Active (vol = 2.0× baseline): spread = 8 × 2.0 = 16 ticks
Extreme(vol = 4.0× baseline): spread = 8 × 4.0 = 32 ticks
```

The 32-tick spread in an extreme event looks very wide. It is correct — the cost of
being filled at that moment is genuinely that high. Quoting tight during an extreme
vol event is offering cheap options to anyone watching.

**What this still misses**: volatility and informed flow are correlated but not the
same. Adverse move is worst specifically when informed traders are active — not just
when vol is high. The spread needs to respond to toxicity specifically, not just vol.

---

#### Layer 4 — Full Spread: Floor + Vol + Toxicity

The complete spread formula:

```
spread_total = spread_floor(asset) × vol_multiplier + 2 × delta_adv

delta_adv = k_tox × p_tox × q̂99
```

Where:
- `spread_floor(asset)` — minimum from average adverse markout. Per asset. Static-ish.
- `vol_multiplier` — scales floor for current volatility. Live, updates every cycle.
- `delta_adv` — additional width from toxicity state. p_tox is the probability of
  informed flow (from Layer 2); q̂99 is the severity in ticks; k_tox scales the response.

Three components, each independent, each necessary:

```
State A (quiet, low p_tox):
  p_tox = 0.2, q̂99 = 5 ticks, vol = 1.0×
  delta_adv = 0.5 × 0.2 × 5 = 0.5 ticks
  spread = 8 + 2(0.5) = 9 ticks

State B (informed, high p_tox):
  p_tox = 0.8, q̂99 = 12 ticks, vol = 1.5×
  delta_adv = 0.5 × 0.8 × 12 = 4.8 ticks
  spread = 8×1.5 + 2(4.8) = 12 + 9.6 = 21.6 ticks
```

State B spread is more than double State A — not because vol changed much, but
because p_tox (probability of informed flow, Layer 2) and q̂99 (severity of the
worst fills, also Layer 2) both rose. The spread is pricing the specific risk
of each fill, not average risk.

---

#### The Fill Rate Trade-Off

Spread too wide → fills stop. `fill_ev` per fill can be positive but revenue per
unit time collapses:

```
EV_per_unit_time = fill_rate × fill_ev
                 = fill_rate × (half_spread − adverse_markout)
```

Doubling the spread from 8 to 16 ticks might improve `fill_ev` per fill from
0.5 ticks to 6 ticks — but if fill rate drops from 10/hour to 0.5/hour, total
revenue falls from 5 ticks/hour to 3 ticks/hour. Wider is not always better.

The optimal spread maximises EV per unit time, not EV per fill. This requires
modelling how fill rate declines as spread increases — which depends on queue
depth, volatility, and how competitive other market makers are at each level.

---

#### Sees vs Misses

| Method | What it sees | What it misses |
|---|---|---|
| Fixed spread | Simple rule | Adverse move varies — same spread bleeds in volatile sessions |
| Spread floor from avg adverse move | Structural minimum per asset | Floor must scale with vol — static floor bleeds in volatile regimes |
| Vol-adjusted floor | Covers regime shifts | Vol ≠ informed flow — toxic fill spikes need toxicity signal |
| Full: floor + vol + toxicity (p_tox × q̂99) | Per-fill risk priced continuously | Fill rate trade-off — too wide = zero fills = zero revenue |
| Joint EV/time optimisation | Both EV per fill and fill rate | Nothing structural — professional standard |

---

#### Professional Standard — Jane Street / Citadel Level

| Component | What they do |
|---|---|
| Spread floor | Per asset, derived from rolling fill markout distribution — updated after every fill |
| Volatility adjustment | Live sigma estimate; spread scales automatically each cycle |
| Toxicity adjustment | p_tox × CVaR99 (TailScore) drives continuous delta_adv — separate from vol |
| Fill rate modelling | Spread set to maximise EV per unit time, not EV per fill |
| Joint optimisation | Avellaneda-Stoikov reservation spread — balances adverse selection cost against fill rate |
| Update cadence | Every L2 update — spread is never static within a session |

Key property: every component is measured from live session data. The floor is not
guessed — it is computed from recent fill markouts. The vol multiplier is a live
ratio. p_tox and q̂99 are live model outputs. Nothing is static config.

---

#### Summary

| | |
|---|---|
| **Core equation** | fill_ev = half_spread − adverse_markout; must be positive in expectation |
| **Spread floor** | 2 × E[adverse_markout] per asset — minimum below which EV is structurally negative |
| **Volatility** | Spread scales with live sigma — static floor bleeds in volatile regimes |
| **Toxicity** | delta_adv = k_tox × p_tox × q̂99 adds toxicity-driven width — continuous, not binary |
| **Fill rate** | Spread too wide = no fills = no revenue; optimal spread maximises EV per unit time |
| **Professional standard** | Per-asset floor from live markouts + vol multiplier + TailScore delta_adv + fill rate joint optimisation |

---

### Layer 4.5 — Queue / Fill Quality

#### What It Is

Queue position determines which fills you get, not just whether you fill. At any
price level, orders sit in a FIFO queue — the exchange fills them front to back as
aggressive orders arrive. Your position in that queue controls whether your fill
comes from a small uninformed order or from the tail end of a large informed sweep.

The cleanest fills go to whoever is at the front of a lightly-loaded queue.
The worst fills go to whoever is at the back of a queue that just got swept entirely.

---

#### Why the Naive Approach Fails

Naive: always quote at BBO — tightest price = most fills = most revenue.

Analogy: a shopkeeper sets up at the busiest market corner. Maximum footfall —
but this corner attracts every pickpocket too. A stall two streets back has fewer
customers but none of them steal. The busiest corner is not automatically the most
profitable corner.

BBO fills are the busiest corner. You fill the most — but the fills that actually
happen at BBO are disproportionately from informed traders and sweepers. Going one
tick deeper selects for committed, larger aggressors who had to consume the entire
BBO level first. Fewer fills, but structurally cleaner.

---

#### Layer 1 — What Queue Position Controls

At price level 101 (ask side), orders queue in FIFO order:
```
Position 1: 200 lots  ← fills first
Position 2: 150 lots  ← fills second
Position 3: YOUR 1 lot
Position 4: 300 lots  ← fills last
```

A 360-lot aggressive buy order consumes positions 1, 2, and your 1 lot. You filled
— but so did 350 lots before you in a single aggressive order. That aggressor was
committed enough to send 360 lots. P(toxic fill) ≈ 1.

If only 5 lots arrive and fill position 1 partially, you do not fill. But that
aggressor was small — probably uninformed. You missed a clean fill but avoided
nothing bad, because the small aggressor would not have reached position 3.

**The key insight**: easy fills (low queue ahead, BBO) disproportionately come from
sweeps. Hard fills (deep queue, away from BBO) are cleaner on average.

---

#### Layer 2 — BBO vs Deep Fill Trade-Off

```
BBO quote (101):    P(fill) high  |  Fills on ANY aggressor including small uninformed
1-tick deep (102):  P(fill) lower |  Fills only when aggressor sweeps through 101 first
2-ticks deep (103): P(fill) low   |  Fills only on large committed sweeps
```

Going deeper selects for larger, more informed aggressors. But a 2-tick-deeper
quote also earns 2 extra ticks of spread. The adverse markout is roughly similar
(the same informed trader caused the sweep) — but spread capture is higher.

This is why institutional market makers often quote slightly inside BBO rather
than at BBO — the fill quality improvement outweighs the fill rate reduction when
the spread premium is captured.

---

#### Layer 3 — Cancel/Replace Destroys Queue Position

Every cancel+replace at the same price resets you to the back of the FIFO queue:

```
t=0:   Place ask at 101. Queue: [500 lots ahead, YOU]
t=10s: Cancel + replace at 101 (same price).
       Queue: [500 lots + 10s of new arrivals ahead, YOU at the back]
```

The replacement was meant to keep your price fresh. Instead it destroyed position.
An engine that cancels and replaces every 200ms to track mid price is perpetually
at the back of the queue — every fill is a sweep fill because only sweeps reach
the back of the queue.

`min_quote_lifetime_ms` in KCMME enforces a floor on how fast quotes can be
replaced — specifically to prevent this compounding queue-destruction pattern.

---

#### Layer 4 — Sweep Fill Detection

The clearest toxic fill signal available without any model: being filled at the
same time as the entire level.

```
Sweep fill:
  Level 101 had 600 lots. You were at position 400.
  Aggressive buyer consumed all 600 lots in one order.
  After fill: BBO is now 102/103. The 101 level is gone.
  Signal: you were the tail of an informed sweep. Adverse markout will be severe.

Non-sweep fill:
  Level 101 had 600 lots. You were at position 2.
  Aggressive buyer consumed 5 lots and left.
  After fill: BBO is still 101/102. 595 lots remain at 101.
  Signal: small, probably uninformed aggressor. Fill is likely clean.
```

Tracking whether the level was swept at fill time separates toxic from clean fills
structurally — independent of post-fill drift measurement.

---

#### Layer 5 — Queue-Aware P(fill) Model

The full model combines queue position with fill probability:

```
P(fill) = f(queue_volume_ahead, own_qty, aggressor_arrival_rate, vol)
EV      = P(fill) × (half_spread − E[adverse_markout | fill at this queue position])
```

Key insight (Cont-Kukanov-Stoikov 2011): P(fill) and fill quality move in opposite
directions. The easiest fills to get (front of queue at BBO) have the highest
adverse markout. The hardest fills (deep, large queue ahead) are the cleanest.

The optimal quote placement maximises EV — not P(fill) alone, not spread alone,
but their product adjusted for expected fill quality at each queue depth.

---

#### Sees vs Misses

| Method | What it sees | What it misses |
|---|---|---|
| Always BBO | Maximum fill rate | Fills are disproportionately sweeps — most toxic |
| Quote 1–2 ticks deep | Fewer but cleaner fills | Still no queue position — don't know how far back |
| Track queue volume ahead | Know position | Can't compute P(fill) without aggressor size distribution |
| Cancel/replace on every tick | Fresh price tracking | Destroys queue position — perpetually at the back |
| Queue-aware model (CKS 2011) | P(fill) by depth + fill quality by position | Nothing structural |

---

#### Professional Standard — Jane Street / Citadel Level

| Component | What they do |
|---|---|
| Queue position tracking | Estimated from L2 snapshots — volume ahead tracked per symbol |
| P(fill) model | CKS 2011 — fill probability as function of queue depth and aggressor rate |
| Fill quality by position | Adverse markout modelled separately for BBO vs deep fills |
| Cancel/replace discipline | Minimum lifetime enforced — queue position preserved |
| Sweep detection | Fill + level-swept tagged — separated from non-sweep fills in markout analysis |
| Spread by queue depth | Deeper quotes get wider spreads — same EV target at each depth |

---

#### Summary

| | |
|---|---|
| **What it is** | Queue position determines which fills you get — earlier = cleaner, later = sweep tail |
| **BBO vs deep** | BBO = high fill rate + toxic; deeper = lower fill rate + cleaner + wider spread capture |
| **Cancel/replace cost** | Every cancel+replace sends you to back of queue — destroys position, guarantees worst fills |
| **Sweep fill** | Level consumed = tail of informed sweep; near-certain severe adverse move follows |
| **P(fill) model** | P(fill) and fill quality move in opposite directions — must be modelled jointly |
| **Professional standard** | Queue-aware P(fill) + sweep detection + min lifetime + spread calibrated by queue depth |

---

### Layer 5 — Inventory Carry, Single Venue

#### What It Is

Every position you hold has a carry cost: the expected mark-to-market loss from
price moving against the position while you hold it. A market maker with inventory
is no longer a neutral price-setter — they have directional exposure. The spread
must compensate for that exposure, and the quotes must continuously work to reduce it.

---

#### Why the Naive Approach Fails

Naive: quote symmetrically around fair value regardless of inventory. Half-spread
applied equally on both sides every cycle.

Analogy: a market vendor quotes the same buy and sell price for umbrellas from 9am
to 5pm regardless of how many he has. By 4pm he holds 200 units, the market closes
in an hour, and he is forced to sell all 200 to a wholesaler at a 30% discount.
Every individual price was right. The session P&L is negative because he never
adjusted his buying interest as his stock grew.

A market maker does the same when ignoring inventory: every fill captures the spread,
p_tox — the probability the fill was from informed flow — is acceptable, the 100ms
adverse markout is within the half-spread. But 80 fills are all on the same side.
Position is now 80 contracts long. Asset drifts 3 ticks against it over the session.
Net carry loss: 240 tick-equivalents. All from holding, not from being picked off.

---

#### Layer 1 — What Carry Actually Costs

Every tick a position is held, it is exposed to price movement.

```
carry_exposure ∝ inventory × volatility × time_held
```

Example: long 10 LINK contracts, σ = 0.02 ticks/sec, held 30 minutes (1800 seconds):
```
expected_price_move = 0.02 × √1800 ≈ 0.85 ticks
carry_exposure      = 10 × 0.85    = 8.5 tick-equivalents
```

If the half-spread is 1 tick, carry eats 8.5 ticks of expected P&L per session at
normal fill rates. The adverse markout from Layer 1 captures carry within 100ms of
the fill. Inventory carry is the same mechanism at the session scale — a slow bleed
that cumulates.

---

#### Layer 2 — Reservation Price Is the Fix

Stop quoting around fair value. Quote around your reservation price — the price at
which your inventory risk is already priced in.

```
reservation_price = fair_value − γ × inventory
```

- `fair_value` = microprice or mid — what the asset is worth to a neutral party
- `γ` = risk aversion — how much you dislike holding inventory (calibrated per asset)
- `inventory` = signed net position (+10 = long 10, −10 = short 10)

With half-spread δ:
```
bid = reservation_price − δ
ask = reservation_price + δ
```

**When flat** (inventory = 0): reservation = fair value. Symmetric. No preference.

**When long 10** (γ = 0.01):
```
reservation = 14.00 − 0.01 × 10 = 13.90
bid = 13.85   ← harder for sellers to sell to you
ask = 13.95   ← easier for buyers to buy from you
```

**When short 10**:
```
reservation = 14.00 − 0.01 × (−10) = 14.10
bid = 14.05   ← easier for sellers to sell to you (reducing your short)
ask = 14.15   ← harder for buyers to buy from you
```

Both quotes shift in the direction that makes inventory-reducing fills more likely.
No quotes pulled. No sides disabled. Continuous.

---

#### Layer 3 — Spread Also Widens With Inventory

Skew alone is not enough. Each additional fill on the wrong side deepens exposure.
The spread must widen to compensate for the carry risk each new fill adds.

**Avellaneda-Stoikov 2008** — optimal half-spread:
```
δ* = (1/γ) × ln(1 + γ/κ)  +  (γ × σ² × (T−t) × |2q+1|) / 2
       ↑ adverse selection       ↑ inventory carry term
```

- `κ` = aggressor arrival rate — controls how much you can charge without losing fills
- `γ × σ² × (T−t)` = carry risk that grows with volatility AND time remaining
- `|2q+1|` = inventory magnitude term

At flat inventory (q=0): spread reflects only adverse selection + fee coverage.
At high inventory: spread widens — each fill on the wrong side costs more to compensate
the carry it adds. Widening makes wrong-direction fills more expensive while skew makes
the right-direction fills easier. Both active simultaneously.

---

#### Layer 4 — Inventory Urgency in 24/7 Crypto

Avellaneda-Stoikov uses `(T−t)` — time to session end. Equity markets close at 4pm.
Crypto never closes. Professional crypto market makers do not shut down to create a
session boundary — shutting down is zero revenue.

They replace time-urgency with three continuous signals:

**1. Inventory magnitude** — large position is always urgent, regardless of time.
Urgency is driven by `|inventory|`, not by a clock.

**2. Inventory age** — how long a position has been held without flattening. If long
10 contracts for 45 minutes with no mean-reversion, urgency is identical to "45 minutes
until session end" in equity terms. `t_held_inv_s` (inventory hold age) is the practical
substitute for `(T − t)`.

**3. Funding rate** — perpetual contracts pay funding every 8 hours. Holding a large
position into a funding event that goes against it is a real periodic carry cost. The
8-hour funding window functions as a soft session boundary in crypto. This is Layer 6.

---

#### Sees vs Misses

| Method | What it sees | What it misses |
|---|---|---|
| Symmetric quoting | Every fill captures the spread | Carry accumulates — forced flatten at bad price |
| Hard limit + flatten | Prevents catastrophic exposure | Flattens at market price at the limit |
| Reservation price (skew only) | Continuously nudges fills toward flat | Does not widen spread — still takes on carry risk per wrong-side fill |
| Skew + spread widening | Compensation per wrong-side fill too | Not inventory-age-aware — same urgency at minute 1 and minute 60 |
| Full Avellaneda-Stoikov | Skew + widening + urgency ramp | Static γ — does not interact with TailScore when both are high |

---

#### Professional Standard

| Component | What they do |
|---|---|
| Reservation price | A-S with per-asset γ calibrated from historical carry cost data |
| Spread widening | `δ ∝ γ × σ² × T_remaining + adverse_selection_floor` |
| Skew | Continuous — updates every cycle, never steps |
| Urgency | Inventory age + funding proximity replace session-clock urgency |
| TailScore interaction | High p_tox + high inventory: wide spread + maximum skew simultaneously |
| Cross-venue hedge | At hard inventory limit: immediately hedge on another venue — do not wait for passive fills |

---

#### Summary

| | |
|---|---|
| **What it is** | Cost of holding inventory — position × price move × time = carry drag |
| **Naive failure** | Symmetric quoting → inventory accumulates → forced flatten at bad price |
| **Reservation price** | `fair_value − γ × inventory` — shifts quotes toward reducing position |
| **Skew** | Both bid and ask move to make inventory-reducing fills easier |
| **Spread widening** | Wider spread at high inventory — compensates carry cost per wrong-side fill |
| **24/7 urgency** | Inventory age + funding timing replace session-clock urgency |
| **Professional standard** | A-S with per-asset γ, inventory-age T, TailScore interaction, cross-venue hedge at limit |

---

### Layer 5.5 — Cross-Venue Delta Neutrality

---

#### What It Is

When a market maker quotes on multiple venues simultaneously, watching individual venue inventory is not enough. You can be flat on Bybit (+0 SUI), flat on Binance (+0 SUI), and long 70 contracts on BitMEX — from Bybit's view, nothing looks wrong. From the system's view, you are carrying $4,200 of directional SUI risk with no mechanism to exit it.

**Delta neutrality** means the net signed position summed across ALL active venues is approximately zero per symbol:

```
net_delta = Binance_qty + Bybit_qty + BitMEX_qty ≈ 0
```

Getting this wrong means the engine is unknowingly running a directional book — not market making, but speculating with exchange fees on top.

---

#### Why the Naive Approach Fails

A beginner watches each venue separately and panics when any single venue exceeds an inventory limit.

**The problem**: fills happen asynchronously. You make-fill on Bybit (long +50), partially hedge on BitMEX (short −20), and make-fill again on Binance (long +30). Each venue alone says "normal." The net says "long +60."

**Concrete incident**: cyc131 mainnet. SUI reached net −70 (BitMEX +10, Bybit −80) while every per-venue residual check passed — `abs_diff_base = 0.0` on each venue individually. The verification script was computing per-venue accuracy but never summing across venues. The engine bled on a directional position it didn't know it had.

---

#### How It Works

**Layer 1 — Net delta check**: sum signed position across all venues every cycle per symbol. Hedge when |net| > threshold.

```
net_SUI = Binance_SUI + Bybit_SUI + BitMEX_SUI
```

**What about basis risk?** When you hedge by taking IOC on another venue, you now have a long on one venue and a short on another — the prices are not identical. The divergence between venue prices while you're hedged is **basis risk**. The primary driver is the perpetual funding rate — different venues can have different funding rates, so your "hedged" position still carries funding exposure. This is the cost you accept when you eliminate carry risk via hedging.

---

**Layer 2 — When to hedge?** Hedging costs money: taker fee + half-spread on the hedge venue. You don't hedge every tick.

Decision: hedge when expected carry cost exceeds hedge cost.

```
carry_cost = |inventory| × σ × mark × √(t_held)    // grows with time and vol
hedge_cost = taker_fee_bps × mark × qty + 0.5 × spread_hedge_venue × qty

hedge if carry_cost > hedge_cost
```

**Mean-reverting regime**: price is bouncing around. In T minutes the position will likely be filled flat naturally. Wait — don't pay taker fees for something passive fills will solve.

**Trending regime**: price is moving away from your fill price. The longer you wait, the more carry accumulates. Hedge now, pay the taker fee, reset the position.

The carry vs hedge cost break-even time:

```
T_break_even = (hedge_cost / (|inventory| × σ))²
```

If T_break_even < 10 minutes in current σ regime → hedge now. If T_break_even > 20 minutes → wait for passive fills.

---

**Layer 3 — The no-transaction band** (Barzykin-Bergault-Guéant 2022 §3-4): don't hedge every time net > 0. Hedge when net exceeds a band derived from three components:

```
band = max(
    band_floor,                          // minimum lot size below which hedging is uneconomic
    band_sigma × σ × √dt × mark,        // 2-sigma natural drift over dt seconds — tolerable variance
    band_fee × mark                      // fee break-even — must exceed taker round-trip cost
)

hedge fires when: |net_delta| × mark > band
```

**Why the sigma term?** In high volatility, natural position swings are larger — a $200 net delta today might reverse in 30 seconds. Setting the band to 2σ × √dt means you only hedge when the position is large relative to what natural mean-reversion can handle. In low volatility, the same $200 net delta is suspicious — it's unlikely to self-correct — so the band is tighter.

---

**Layer 4 — Signal-conditional threshold** (professional): the band should tighten when directional pressure is building. Four signals that indicate the position will NOT self-correct:

| Signal | Why it matters |
|---|---|
| **OFI** (order flow imbalance) | Book pressure building before trades fire — p_tox — probability the fill is from informed flow — is rising. Position will worsen, not revert. |
| **Mid drift velocity** | Price is moving away from your fill price at sustained speed — not a transient noise bounce. |
| **Adverse fill streak** | N consecutive fills all on the same side — you're being picked off directionally, not making two-sided markets. |
| **Inventory age** (`t_held`) | Position has been held 20 minutes without reversion — market has moved against you permanently. |

In trending regime (OFI strong + drift velocity high + streak active): band narrows → hedge at smaller net delta.
In mean-reverting regime (OFI low + drift flat): band stays wide → wait for passive fills.

---

#### Sees vs Misses

| Method | What it sees | What it misses |
|---|---|---|
| Per-venue inventory limit | Single-venue exposure | Cross-venue net accumulation |
| Net delta sum across venues | Total directional risk per symbol | When to hedge (would trigger on every tiny imbalance) |
| No-transaction band (BBG 2022) | Avoids over-hedging in normal variance | Same threshold in trending vs mean-reverting |
| Signal-conditional band | Adapts urgency to market state | Requires OFI and streak signals to be active |

---

#### Professional Standard

| Component | What they do |
|---|---|
| Net delta | Computed across ALL venues every cycle, per symbol, including all leg types |
| Hedge trigger | BBG 2022 band: `max(band_floor, band_2σ × √dt, band_fee)` |
| Regime conditioning | Band narrows on high OFI + high drift velocity + adverse fill streak |
| Inventory age urgency | `t_held` continuously narrows the band — position held 20min = much tighter threshold |
| Venue selection | Hedge routes to cheapest venue: `taker_fee_bps + 0.5 × spread` compared live |
| Basis risk monitoring | Funding rate divergence tracked as latent basis risk — factored into carry cost |
| Continuous in-engine auditor | Every 60s: assert `|net_delta| ≤ tol` internally — not just at post-deploy checkpoints |

---

#### Summary

| | |
|---|---|
| **What it is** | Net signed position summed across all venues — must stay near zero per symbol |
| **Why it matters** | Per-venue limits catch single-venue exposure, not cross-venue accumulation |
| **Naive failure** | Each venue reports flat; net is directional; engine unknowingly speculates |
| **No-transaction band** | Hedge when net > band — avoids over-hedging on natural variance |
| **Carry vs hedge** | Hedge when σ × √t_held × |inventory| > taker_fee + spread; otherwise wait |
| **Regime conditioning** | Trending regime: narrow band (hedge sooner); mean-reverting: wide band (wait) |
| **Professional standard** | BBG 2022 band + signal-conditional tightening + inventory-age urgency + continuous auditor |

---

### Layer 6 — Funding Rate / Basis in Perpetuals

---

#### Why the Naive Approach Fails

A beginner market maker quotes two-sided on a SUI perpetual, earns the spread, and tracks daily gpnl. After a week they notice something strange: spread capture is consistently positive, but total gpnl is flat or negative. The spread model looks right. The fills look right. The number doesn't add up.

What they missed: every 8 hours, an invisible cash payment clears against their inventory.

**Concrete example:**

You hold 100 SUI long at $3.50 throughout a session. Funding rate is +0.05% (positive means longs pay shorts). At the 8h mark:

```
funding_payment = inventory × mark_price × funding_rate
               = 100 × $3.50 × 0.0005
               = $0.175 per period

Three periods per day = $0.525/day out of your account.
Equivalent to ~14 full bid-spread captures erased.
```

You can be a perfectly functioning market maker and still lose money to funding if you hold consistent long inventory in a high-positive-funding environment.

---

#### How the Funding Rate Is Computed

The exchange derives the rate from the basis — the gap between the perpetual price and the spot index:

```
premium_index = (perp_mid − index_price) / index_price    // basis as fraction of spot
interest_rate = 0.01% per 8h                              // fixed cost of capital

funding_rate ≈ premium_index + interest_rate              // simplified, clamped ±0.75%
```

**Why this formula?** If the perp is above spot (premium_index > 0), longs pay shorts. This makes going short the perp attractive — new shorts enter, new longs are discouraged — which pulls the perp back toward spot. The funding mechanism IS the anchoring mechanism. Without it, a perpetual would drift away from spot permanently since there's no delivery date forcing convergence.

**Sanity check**: if perp == spot, premium_index = 0, funding rate ≈ 0.01% (just the interest rate). Nobody is especially advantaged. Holding a perp long is like borrowing capital — a tiny per-period cost is correct.

**Numbers**: SUI perp at $3.52, SUI index at $3.50:
```
premium_index = (3.52 − 3.50) / 3.50 = +0.57%
funding_rate  ≈ 0.57% + 0.01% = 0.58% per 8h

= 21% annualized carry cost for longs.
```
At 0.58%, a 100-lot long position pays $2.03 every 8 hours. Holding for a full day = $6.09 — the engine would need to capture 120+ spreads on that position just to break even on carry.

---

#### Funding as a Regime Signal

The funding rate is not just a cost — it tells you the market's structure.

**High positive funding (>0.05%)** means:
- Perp is trading significantly above spot
- The market is net-long and leveraged — retail traders are paying to stay long
- Adverse selection risk rises on bid fills: fills happen into a crowded bullish trade; correlated adverse moves are more likely

**High negative funding (<−0.05%)** means:
- Perp is below spot; shorts are crowded and leveraged
- Ask fills carry elevated squeeze risk

**For a market maker, high positive funding changes two things:**

1. **Every bid fill is more expensive than it looks.** Not just adverse selection risk — also 0.05%+ per 8h in explicit cash carry. Your effective bid price should be lower to demand more compensation per fill.

2. **The spread must include a funding-adjusted floor:**

```
spread_bid += 2 × |funding_rate_per_tick × expected_hold_time|
```

At 0.05%/8h = 0.000174%/min, with expected 5min hold per fill:
```
funding_carry = 0.000174% × 5 = 0.00087% ≈ 0.030 ticks on SUI at $3.50
```
Small per fill, but stacks directly with the adverse selection floor from Layer 4 and the inventory carry term from Layer 5.

---

#### Funding Timing — the 5-Minute Window

Funding payments happen at specific UTC moments: 00:00, 08:00, 16:00. The inventory you hold at that exact second determines your payment.

**Pre-funding urgency**: if funding rate is +0.1% and you're holding 200 SUI long, holding through the window costs $0.70. Flattening 5 minutes before avoids the payment entirely.

A professional MM tracks `time_to_next_funding`. As it approaches zero with large positive-rate long inventory:
- Widen bid further (demand even more edge per wrong-side fill)
- Accelerate skew toward flattening
- Consider hedging earlier than the normal band would trigger

This is directionally the same as the session-urgency in Avellaneda-Stoikov (Layer 5) — but driven by the funding clock, not a closing bell. In crypto, this IS the urgency signal that replaces (T−t).

---

#### Basis Risk Across Venues

From Layer 5.5: when you hedge by going short on a different venue, you hold long on venue A and short on venue B. This looks delta-neutral. But funding rates are NOT identical across venues.

**Example**: BitMEX SUI funding = +0.08%, Bybit SUI funding = +0.03%.

You are long BitMEX, short Bybit:
```
Pay on BitMEX long:    0.08% per period on notional
Receive on Bybit short: 0.03% per period on notional

Net funding drag = 0.08% − 0.03% = 0.05% per period
```

Your "delta-neutral" hedge still has a 0.05%/8h carry cost purely from the funding rate divergence. This is **funding basis risk** — distinct from the price basis risk (venue prices diverging temporarily) covered in Layer 5.5.

```
funding_basis_drag = |rate_long_venue − rate_short_venue| × inventory × mark
```

The hedge venue selection should incorporate `funding_rate_diff` in its cost comparison, not just `taker_fee + spread`.

---

#### Sees vs Misses

| Method | What it sees | What it misses |
|---|---|---|
| Ignore funding | Spread revenue | Periodic cash drain — can erase all spread capture |
| Track funding rate as a cost | Explicit carry per period | Funding as regime signal (crowded longs = elevated adverse selection) |
| Funding-adjusted spread | Correct per-fill compensation in current rate environment | Timing urgency near 8h window |
| Pre-funding urgency ramp | Avoids worst-case inventory carry through settlement | Cross-venue funding basis in hedged positions |
| Full professional model | All of the above simultaneously | — |

---

#### Professional Standard

| Component | What they do |
|---|---|
| Funding rate | Consumed live from venue WebSocket every tick — not polled |
| Spread adjustment | `spread_bid += funding_carry_term` when rate > 0; opposite when rate < 0 |
| Pre-funding urgency | Track `time_to_next_funding`; in last 300s with long inventory → widen bid + narrow hedge band |
| Funding as regime signal | Sustained >0.05% → increase adverse selection weight; reduce bid size |
| Cross-venue hedge cost | HedgeRouter adds `funding_rate_diff × notional` to each venue's hedge cost comparison |
| Sim modelling | Funding payments modelled in sim P&L — prevents sim-live divergence on high-funding sessions |

---

#### Summary

| | |
|---|---|
| **What it is** | Periodic payment between longs and shorts to anchor perp price to spot |
| **Direction** | Positive rate → longs pay shorts; negative → shorts pay longs |
| **Formula** | `funding_rate ≈ (perp_mid − index) / index + 0.01%` — basis dominates |
| **MM impact** | Long inventory in positive-funding regime = explicit cash carry on top of adverse selection |
| **As a signal** | High positive funding = crowded leveraged longs = elevated adverse selection risk on bid fills |
| **Timing** | Track `time_to_next_funding` — widen bid + accelerate flatten in the 5-min approach window |
| **Cross-venue** | "Hedged" positions still carry funding basis risk if venues have different rates |
| **Professional standard** | Live funding rate → spread floor + pre-funding urgency + regime signal + cross-venue cost comparison + sim modelling |

---

### Layer 7 — Cancel/Replace Churn Ratio

---

#### Why the Naive Approach Fails

**Analogy**: you work a market stall and you reprice your sign every 30 seconds whenever the stall next door changes theirs. Each time you change the sign, the queue resets — customers walk away and rejoin the back. By end of day you changed the sign 200 times and served 4 customers. You were always correctly priced. You never made any money.

A beginner MM reprices on every mid-price tick. Quotes are always near fair value. But:
- Every reprice destroys queue position — new place goes to the back
- Every reprice = 2 order operations (cancel + place) → OTR spikes → exchange may throttle
- During the cancel's ~22ms round-trip, the old quote is live and can be adversely filled
- Result: 500 operations/minute, 3 fills. All the cost of market making, none of the queue benefit.

---

#### The Core Tension

**Cost of repricing** (cancel + replace):
- Queue rank resets to 0
- +2 to OTR counter
- ~22ms cancel RTT window where old stale quote remains fillable
- If reprice delta < 1 tick: queue destruction with zero economic gain

**Cost of NOT repricing** (holding a stale quote):
- Quote drifts from fair value
- Informed traders pick off a quote that's 3 ticks cheap

The question: at what fair-value move distance does stale cost exceed reprice cost? That threshold is the decision boundary — and it must adapt to the current volatility regime.

---

#### How It Works

**Layer 1 — Reprice threshold**: only reprice when fair value has moved far enough:

```
reprice if |new_fair_value − current_quote_price| > δ_reprice
```

Too small → constant repricing, queue destruction, OTR spike.
Too large → stale quotes → adverse fills.

**Never reprice by less than 1 tick.** A sub-tick reprice sends a new quote to the same price level, resets queue rank, and gains nothing.

---

**Layer 2 — The adaptive threshold**: the threshold should track the current volatility regime:

```
δ_reprice = max(1_tick, k_vol × σ_current × √(cancel_RTT_ms / 1000))
```

**Why σ × √RTT?** This is the expected mid-price move during the cancel window — the same quantity as the stale quote cost. You reprice only when the quote is already as stale as a full cancel-window of volatility would produce.

- High vol (fast market): σ large → δ_reprice falls → reprice more aggressively. Quotes go bad fast.
- Low vol (quiet market): σ small → δ_reprice rises → hold queue position longer.
- High RTT: cancel is slow → stale window is large → tolerate more staleness before repricing pays off.

**Also**: `min_quote_lifetime_ms` — the temporal floor. Even if the spatial threshold fires, the quote cannot be canceled until it has lived long enough. Prevents burst repricing (a fast price spike triggers 20 cancels in 50ms). In KCMME: 300ms default, per-asset configurable, but static within a session (identified gap: should be σ-adaptive too).

---

**Layer 3 — Schmitt-trigger hysteresis**: a threshold without hysteresis bounces. If |Δd*| = 2.1 ticks and threshold = 2.0, the reprice fires. After the reprice, |Δd*| = 0. Price moves 0.1 tick. Now |Δd*| = 0.1 — no reprice. Moves another 0.1 tick — |Δd*| = 0.2. If this oscillates, the engine enters a cancel/replace loop that never settles.

**Schmitt-trigger** breaks this:
```
enter REPLACE-eligible: |Δd*| ≥ 1.0 × θ
exit  REPLACE-eligible: |Δd*| ≤ 0.6 × θ
```
Once you trigger, you stay in reprice mode until the quote is back within 60% of the threshold. Prevents oscillation at the boundary.

---

**Layer 4 — Churn budget and feedback loop**: OTR is a budget. If the exchange allows 200 operations/minute before throttling, and you fill 5 times/minute, your budget is 40 operations/fill. Professional MMs monitor rolling OTR and use it as a feedback signal:

```
if rolling_5min_churn_ratio > budget_threshold:
    increase δ_reprice    // widen the dead-band — repress less aggressively
else if churn_ratio < 0.7 × budget_threshold:
    decrease δ_reprice    // budget headroom — can afford to track price more closely
```

This makes the system self-correcting. The engine modulates its own reprice aggressiveness based on observed outcome, not just on a calibrated parameter.

---

#### Sees vs Misses

| Method | What it sees | What it misses |
|---|---|---|
| Reprice on every tick | Always near fair value | Queue destruction, OTR spike, exchange throttle |
| Fixed threshold (e.g. 2 ticks) | Controlled churn in normal conditions | Too aggressive in high-vol, too conservative in low-vol |
| σ-adaptive threshold | Right balance for current regime | No feedback — doesn't respond to actual observed churn rate |
| Schmitt-trigger + adaptive | Prevents oscillation at boundary | No cross-asset OTR budget coordination |
| Churn budget feedback + all above | Self-correcting, exchange-aware | — professional standard |

---

#### Professional Standard

| Component | What they do |
|---|---|
| Reprice threshold | `max(1_tick, k_vol × σ × √RTT)` — σ-adaptive per asset |
| Schmitt-trigger | Hysteresis at 1.0×θ enter / 0.6×θ exit — prevents oscillation |
| Minimum quote lifetime | Hard temporal floor, ideally also σ-adaptive |
| Sub-tick guard | Reprice vetoed if new price == current price after tick rounding |
| OTR monitoring | Rolling 5min churn ratio tracked per asset per venue in real time |
| Churn budget feedback | High OTR → widen dead-band autonomously; recover when OTR falls |
| Queue-protect gate | Skip cancel if current queue value > back-of-queue replace value |

---

#### Summary

| | |
|---|---|
| **What it is** | Ratio of cancel/place operations to fills — measures quoting activity vs liquidity produced |
| **The tension** | Reprice too often: queue destruction + OTR throttle. Too rarely: stale fills |
| **Sub-tick guard** | Never reprice to the same price level — queue destruction with zero gain |
| **Adaptive threshold** | `max(1_tick, k_vol × σ × √RTT)` — widens in fast markets, tightens in slow |
| **Schmitt-trigger** | Hysteresis prevents oscillation at the threshold boundary |
| **Churn budget** | OTR is a budget; feedback loop keeps churn near the limit, not blindly below |
| **`min_quote_lifetime_ms`** | Temporal hard floor — no cancel before minimum age, regardless of price move |
| **Professional standard** | σ-adaptive threshold + Schmitt-trigger + OTR feedback + queue-value gate |

---

### Layer 8 — Asset-Wise Profitability

---

#### Why the Naive Approach Fails

You run 10 assets. Total session gpnl = +$5. You note it's a profitable day.

What you didn't see:
```
SUI:   +$22     TRUMP: −$8
BTC:   +$8      AAVE:  −$7
BNB:   +$3      LINK:  −$5
ETH:   +$3      NEO:   −$4
SOL:   +$2      DOGE:  −$9
```

Three assets made $35. Seven lost $30. You ran a seven-way losing book subsidized by three winners — and you never noticed because you only looked at the sum.

Total session gpnl is the worst possible diagnostic. It tells you whether the day was positive. It tells you nothing about what caused it, which assets to run more of, or which to stop.

---

#### The Four Dimensions of Per-Asset Health

Every asset needs to be measured on four axes simultaneously.

---

**1. GPNL per fill** — how much do you earn per maker fill on average?

```
gpnl_per_fill = session_gpnl / fill_count
```

Positive = spread captures more than adverse selection loses. Negative = the asset's fills are structurally losing regardless of spread width.

**Numbers**: SUI — 200 fills, +$18 gpnl → +$0.09/fill. DOGE — 180 fills, −$9 gpnl → −$0.05/fill. SUI earns 9 cents per fill; DOGE loses 5 cents on every fill it receives.

---

**2. Fill rate** — fills per hour per asset

High fill rate × positive gpnl/fill = ideal. But fill rate alone says nothing:
- High fill rate + negative gpnl/fill = constantly swept by toxic flow
- Low fill rate + positive gpnl/fill = spread is wide, fills are selective — may be fine
- Low fill rate + negative gpnl/fill = almost never fills and loses when it does — exit the asset

Fill rate is only useful alongside gpnl/fill.

---

**3. Adverse fill rate** — fraction of fills that moved against you afterward

```
adverse_fill_rate = fills where post_fill_100ms_markout < 0 / total_fills
```

Re-anchoring p_tox from Layer 2: p_tox is the probability the fill is from informed flow. The adverse fill rate is the realized outcome of that probability — measured from actual post-fill markout in fills_*.jsonl, not predicted.

**Threshold**: if adverse fill rate > 35–40%, the asset's flow is structurally informed. No spread adjustment fixes this — you are quoting into a book dominated by traders who know more than you. The right response is not to widen; it is to question whether to run the asset at all.

**Example**: TRUMP adverse fill rate = 48%. For nearly half of all TRUMP fills, the market immediately moved against you. That is not a calibration problem — it is a flow composition problem.

---

**4. Capital efficiency** — gpnl per unit of inventory risk committed

```
capital_efficiency = session_gpnl / (avg_inventory_notional_usd × session_hours)
```

This is the dimension that most engines miss entirely. Two assets can both show +$10 gpnl:
- LINK: avg $150 inventory → efficiency = $10 / ($150 × 4h) = $0.017/USD·hour
- SUI:  avg $800 inventory → efficiency = $10 / ($800 × 4h) = $0.003/USD·hour

LINK earned the same return at one-fifth the capital. In a world with a fixed total inventory cap ($3,000 across all assets), every dollar you give to the SUI-equivalent is a dollar you cannot give to the LINK-equivalent.

---

#### The Capital Allocation Decision

```
maximize: Σ_asset (capital_allocation_i × capital_efficiency_i)
subject to: Σ_asset capital_allocation_i ≤ total_risk_budget
```

Run more of what works. Run less of what doesn't. This is not complex in principle — it is just invisible without the per-asset scorecard.

**Screening criteria** — when to reduce or drop an asset:

| Criterion | Threshold | Action |
|---|---|---|
| GPNL (rolling 5 sessions) | < 0 | Reduce cap; investigate |
| Adverse fill rate | > 35% | Investigate flow composition |
| Adverse fill rate | > 45% | Flag for removal |
| Capital efficiency | Below basket average | Reallocate cap to better assets |
| Fill rate | Below minimum | Spread too wide or asset illiquid |

---

#### How Prior Layers Compound Per-Asset Differently

Each gap from Layers 0–7 damages different assets disproportionately:

| Layer | Which assets suffer most |
|---|---|
| L0 — fair value lag | Thin-book assets (SUI, TRUMP, NEO) — mid vs microprice diverges 3–5 ticks |
| L2 — adverse selection | Structurally informed assets — news-driven tokens with high informed-flow fraction |
| L3 — cancel RTT | Fast-moving assets (SUI, LINK) — stale window matters more when price moves quickly |
| L5 — inventory carry | High-volatility assets — carry cost grows with σ; SUI carry >> AAVE carry |
| L6 — funding | Assets where you hold consistent long inventory in positive-funding environments |
| L7 — churn | Thin-book assets with 1-tick spreads — queue destruction per reprice is more damaging |

The scorecard tells you WHERE the losses are. The gap register tells you WHY. Used together, they produce a prioritized list: fix the gap that hurts the most assets or the most capital-weighted asset first.

---

#### Sees vs Misses

| Method | What it sees | What it misses |
|---|---|---|
| Total session gpnl | Was the day profitable? | Which assets made money vs which are subsidized |
| Per-asset gpnl | Which assets contributed | Doesn't separate adverse selection from spread capture |
| Gpnl/fill + adverse fill rate | Fill quality per asset | Doesn't account for inventory risk committed |
| Capital efficiency ranking | True return per unit of risk budget | Rankings shift with regime — requires rolling window |
| Full 4-axis rolling scorecard | Complete picture for allocation decisions | — professional standard |

---

#### Professional Standard

| Component | What they do |
|---|---|
| Daily scorecard | Per-asset: gpnl, fill_count, gpnl/fill, adverse_fill_rate, fills/hour, avg_inventory_notional, capital_efficiency |
| Rolling window | 5-session rolling average — smooth single-session noise |
| Automatic reallocation | Capital shifts toward high-efficiency assets; advisory script proposes TOML changes |
| Adverse rate gate | > 35%: cap reduction. > 45%: flagged for removal |
| New asset screening | 3-criterion pass (adverse rate, fill rate, capital efficiency) over 10-day sim + live trial |
| Regime adjustment | Efficiency rankings recalibrated quarterly — calm-market rankings do not hold in high-vol |

---

#### Summary

| | |
|---|---|
| **What it is** | Per-asset decomposition of gpnl, fill quality, and capital committed |
| **Naive failure** | Total gpnl masks seven losing assets subsidized by three winners |
| **Four axes** | Gpnl/fill + adverse fill rate + fill rate + capital efficiency |
| **Capital allocation** | Fixed risk budget → concentrate on high-efficiency assets, withdraw from low |
| **Adverse rate gate** | > 35%: reduce; > 45%: remove. No spread adjustment fixes structural informed flow |
| **Prior layer interaction** | Each gap hurts different assets — scorecard shows WHERE, gap register shows WHY |
| **Professional standard** | 4-axis rolling scorecard → automatic reallocation proposals → regime-aware recalibration |

---

### Layer 9 — Per-Asset Calibration

---

#### Why the Naive Approach Fails

You spend two weeks carefully tuning SUI parameters. Adverse fill rate drops from 38% to 27%. GPNL/fill turns positive. You copy the same parameter set to AAVE, BNB, and LINK and deploy all four.

AAVE starts bleeding immediately. BNB churns on every tick. LINK barely fills.

The parameters that fit SUI captured SUI-specific properties — its tick size, its book depth, its informed-flow fraction, its volatility in tick units. None of those are the same on AAVE. You didn't tune an engine; you tuned a SUI engine and called it general.

Each asset is a different environment. The engine must adapt to the environment — the environment will not adapt to the engine.

---

#### What Must Be Calibrated Per Asset

Not all parameters matter equally. There is a tier structure.

**Tier 1 — Must be per-asset (wrong here = structural bleed every session):**

| Parameter | Why it must differ |
|---|---|
| `base_spread` / `k_vol_spread` | SUI σ in tick units is 5× higher than LINK. Same multiplier on both means SUI is underpriced and LINK is overpriced. |
| Toxicity sensitivity (`k_tox_gate`) | Adverse fill fraction differs by asset. SUI attracts more informed flow than AAVE. Same sensitivity = over-defensive on AAVE, under-defensive on SUI. |
| `max_inventory_notional` | Must match the asset's fill rate and σ. At SUI's fill rate and volatility, $500 notional cap fills up in 2 minutes. On BTC it takes 45 minutes. |
| `integrated_gamma` | Risk aversion in the A-S spread formula. γ must reflect this asset's carry cost per lot — proportional to σ per tick. |
| `replace_deadband_k_sigma` | The vol-adaptive reprice multiplier. Needs different calibration per asset because σ in tick units and book update frequency differ. |

**Tier 2 — Should be per-asset (wrong here = suboptimal but survivable):**
`k_inv_depth_t` (inventory widening), `mid_drift_cancel_frac` (stale cancel aggressiveness), `min_quote_lifetime_ms`.

**Tier 3 — Can be shared:**
`cancel_replace_cooldown_ms`, `ws_ping_interval_ms`, `funding_interval_hr` — exchange/operational properties, not asset-specific.

---

#### The Calibration Sequence

Calibrate in order. Each layer depends on the previous one being stable. Never touch layer N+1 while layer N is still moving.

```
Step 1: Spread floor (base_spread, k_vol_spread)
        ↓ freeze
Step 2: Toxicity sensitivity (k_tox_gate, tox weights)
        ↓ freeze
Step 3: Inventory cap (max_inventory_notional)
        ↓ freeze
Step 4: Reprice threshold (replace_deadband_k_sigma)
        ↓ freeze
Step 5: Advanced (integrated_gamma, T_horizon)
        ↓ only when 1–4 are stable
```

If the spread floor is wrong, the toxicity data you collect is polluted — you're measuring adverse selection at the wrong spread width. Tuning toxicity first means calibrating to a moving target.

---

#### The Cold-Start Problem

You need 200–300 fills with post-fill markout to compute a statistically meaningful adverse fill rate and A3 deflated Sharpe. But to get 200 fills you need to be live. But to be live you need parameters.

**The cold-start solution**: use Stage 2 sim-derived parameters as the starting point. Apply a 20% safety margin (widen spread, reduce inventory cap). Collect live data. Once you have 200+ fills with markout, calibration starts.

```
Stage 2 sim suggests: base_spread = 4 ticks
Cold-start live:      base_spread = 5 ticks  (+20% safety margin)
```

---

#### Walk-Forward Validation Protocol

The antidote to overfitting. Parameters are never validated on the same data they were tuned on.

1. **Collect**: run cold-start parameters for 10+ sessions
2. **Split**: sessions 1–7 calibrate / sessions 8–10 validate (sealed during calibration)
3. **Calibrate**: tune Tier 1 params against sessions 1–7 only
4. **Lock**: freeze all parameters
5. **Validate**: run locked params against sessions 8–10 without touching them
6. **Gate**:
   - A3_deflated_sharpe on sessions 8–10 ≥ 70% of sessions 1–7 → **PASS**
   - A3_deflated_sharpe on sessions 8–10 < 70% → **FAIL (overfit)**

If FAIL: the calibration captured the noise of sessions 1–7, not the structure of the asset. Collect more data and re-examine what drove the apparent improvement.

---

#### Overfitting Detection Signals

| Signal | What it reveals |
|---|---|
| **High parameter sensitivity** | Change k by 10% → gpnl changes >30%. You're on a sharp peak — likely a historical artefact. |
| **Parameters at range boundaries** | Tuned k_tox is at its configured maximum. The optimizer found an edge case, not a general property. |
| **One session driving the result** | Remove one session from calibration window → A3 drops >50%. You calibrated to one outlier. |
| **Walk-forward degradation > 30%** | Definitive test — calibration didn't generalise. |

---

#### Regime-Conditional Calibration

Calibrating on mixed-regime data produces params that are suboptimal for both regimes — an average of two different distributions.

**Separate calibration sets:**
- Calm-regime params: sessions where `sigma_short < 30th percentile`
- Trending-regime params: sessions where `sigma_short > 70th percentile`

In calm SUI, `k_tox_gate` might correctly sit at 0.15 (informed flow rare). In trending SUI, `k_tox_gate` should be 0.35 (informed flow spikes). Mixed-regime data gives 0.22 — under-defensive in trending, over-defensive in calm.

The live regime classifier (Layer 10) switches between the two sets. When regime flips, params flip.

---

#### Can We Make This Fully Automated? (Honest Answer)

Some params ARE already auto-adaptive. The FeedbackController updates `k_tox_live` on every fill — online learning is already running. The remaining pain comes from params that update too slowly for fill-by-fill adaptation:

| Parameter | Why it can be online adaptive |
|---|---|
| `k_tox_live` | Already: FB controller updates per fill |
| `replace_deadband_k_sigma` | Can adapt from session OTR data each session |
| `min_quote_lifetime_ms` | Can adapt from current σ_tick_rate (Layer 7 gap) |
| `k_tox_gate` | Can adapt as posterior from rolling adverse fill rate |

| Parameter | Why it cannot be fully online adaptive |
|---|---|
| Asset's baseline flow composition | Property of who trades it — changes slowly; need 200+ fills to observe |
| Walk-forward gate | Cannot have a held-out window in a fully online system — fundamental tension |
| Cold-start prior for a genuinely new asset | Must come from somewhere — sim-derived conservative defaults |

The right target: small set of cold-start priors (conservative, sim-derived) + everything else driven by the feedback controller. After 200+ fills, the system has self-calibrated to the asset.

---

#### Sees vs Misses

| Approach | What it sees | What it misses |
|---|---|---|
| Global params (same for all) | Engine simplicity | Every asset is a different environment |
| Per-asset tuning (no validation) | Asset-specific fit | May be overfit to historical window |
| Walk-forward validated calibration | Generalizable params | Mixed-regime data averages two distributions |
| Regime-conditional walk-forward | Full picture | Requires enough data per regime to calibrate separately |

---

#### Professional Standard

| Component | What they do |
|---|---|
| Calibration pipeline | Automated: fills data → locked_metrics → param proposal → walk-forward gate → staged deployment |
| Sequence discipline | Validate-freeze per layer — never tune N+1 while N is unstable |
| Data minimum | 300+ fills with markout before calibrating; 500+ for trusting A3 |
| Walk-forward gate | 70% retention of calibration-window performance on validation window |
| Sensitivity check | Every proposed param change tested ±10% and ±20% — must stay within 15% gpnl variance |
| Regime-conditional | Separate calm/trending calibration sets per asset; regime classifier switches live |
| Recalibration cadence | Quarterly or on regime shift; never ad-hoc mid-session |

---

#### Summary

| | |
|---|---|
| **What it is** | Finding the right parameter values for each asset from data, not intuition |
| **Why per-asset** | Each asset has different σ, fill rate, informed-flow fraction, book depth |
| **Calibration sequence** | Spread floor → toxicity → inventory cap → reprice threshold → advanced |
| **Cold start** | Sim-derived params + 20% safety margin until 200+ fills collected |
| **Walk-forward** | Calibrate on 70% of sessions, validate on 30% without re-tuning |
| **Overfitting signals** | High sensitivity, boundary params, single-session dependence, walk-forward degradation |
| **Regime-conditional** | Separate calm/trending param sets; regime classifier switches live |
| **Professional standard** | Automated pipeline + validate-freeze sequence + sensitivity check + quarterly recalibration |

---

### Layer 10 — Market Regime Classification

---

#### Why the Naive Approach Fails

You build a market making engine and tune it carefully. It works well for two weeks. Then it starts bleeding. Parameters unchanged. Spread unchanged. What changed was the market.

The engine was tuned in a mean-reverting regime — prices oscillate around fair value, fills are balanced, inventory naturally unwinds. It is now in a trending regime — price has a direction, every bid fill is followed by a downward move, every ask fill by an upward move. The engine is posting two-sided quotes into a one-directional market. Every fill is adverse by design.

**A regime-unaware engine is a regime-dependent engine pretending to be general.**

---

#### The Three Regimes a Market Maker Cares About

**Regime 1 — Mean-Reverting / Choppy**

Price oscillates around fair value. Buyers and sellers are roughly balanced.
```
Price:   ↑↓↑↓↑↓↑↓   (oscillates)
EV per fill: positive — spread captured, adverse selection low
Inventory: fills naturally unwind as the book oscillates
```
This is the market maker's natural habitat. Tight spreads, high fill rates, natural inventory recycling.

**Regime 2 — Trending**

Price has direction. Every fill on the wrong side is followed by continued adverse movement.
```
Price:   ↓↓↓↓↓↓↓↓   (directional)
Every bid fill: adverse markout negative (price keeps falling)
EV per fill: structurally negative at current spread width
```
In a trending regime, two-sided market making is structural adverse selection. Informed traders know the direction — they sell your bids in a downtrend. Your fills are directionally concentrated, not balanced.

**Regime 3 — Volatility Spike**

Fair value gaps discontinuously. Any live quote is immediately stale by multiple ticks. Identical to Layer 3 stale quote exposure — but caused by a regime event rather than slow RTT.

---

#### The Four Regime Signals

**σ_ratio** = σ_short / σ_long (30s realized vol / 10min realized vol)
- ratio > 1.5 → vol spike or early trend
- ratio < 0.7 → unusually calm, mean-reverting

**VPIN** = |buy_volume − sell_volume| / total_volume over rolling volume bucket
- VPIN → 0: balanced flow (choppy/uninformed)
- VPIN → 1: one-sided flow (trending/informed)
- VPIN > 0.35–0.40 predicts increased adverse selection in next window (leading indicator)

**OFI** = (bid_size_change_at_BBO − ask_size_change_at_BBO) / total_BBO_size
- Sustained positive OFI → upward price pressure; negative → downward
- 50–200ms leading signal; VPIN is minutes-scale. Both needed.

**price_path** = (mid_now − mid_60s_ago) / σ_short
- |price_path| > 2.0 → strong confirmed trend
- |price_path| < 0.5 → choppy, no direction

---

#### What Must Change Per Regime

| Parameter | Choppy | Trending | Spike |
|---|---|---|---|
| Spread width | 2–3 ticks (base) | 4–6 ticks (widen structurally) | much wider; re-quote only after σ settles |
| Inventory cap | full | reduce (don't accumulate against trend) | reduce temporarily |
| Hedge band | normal | narrow (hedge more aggressively) | n/a — cancel all live |
| Skew aggressiveness | moderate | high (push hard to exit wrong-side inventory) | n/a |

---

#### The Probabilistic Classifier (Professional Standard)

**Naive way** — hard threshold switch:
```
if VPIN > 0.40 → TRENDING
if VPIN < 0.40 → CHOPPY
```
Problem: VPIN bounces around 0.40. Params flip back and forth. Engine destabilises.

**Professional way** — probability output, blend params proportionally:
```
P(TRENDING | signals) = 0.73
P(CHOPPY   | signals) = 0.22
P(SPIKE    | signals) = 0.05

spread = 0.73 × trending_spread + 0.22 × choppy_spread + 0.05 × spike_spread
```
No hard switch, no oscillation. Logistic regression or HMM trained on labelled historical sessions, walk-forward validated.

---

#### Sees vs Misses

| Approach | What it sees | What it misses |
|---|---|---|
| No regime awareness | Simple engine | Systematic adverse selection in trending; over-wide in choppy |
| Hard threshold classifier | Regime detection | Oscillation at boundary; no uncertainty quantification |
| Probabilistic classifier | Uncertainty handling | Requires labelled training data; walk-forward discipline |
| Per-asset regime classifier | Asset-specific patterns | Some assets rarely trend — classifier must be per-asset |

---

#### Professional Standard

| Component | What they do |
|---|---|
| Four signals | σ_ratio + VPIN + OFI + price_path — no single signal sufficient |
| Probabilistic output | Regime probability vector, not hard label — blend params proportionally |
| Regime-conditional params | Separate calibration sets per regime per asset |
| Walk-forward validated | Classifier trained on sessions 1–N, validated on N+1 |
| Spike response | Cancel-all within 1 RTT; re-quote only after σ stabilises |
| Per-asset classification | SUI and BTC have different regime signatures |

---

#### Summary

| | |
|---|---|
| **What it is** | Real-time labelling of market behavior — choppy, trending, or spiking |
| **Why it matters** | Spread, hedge aggressiveness, inventory cap, and skew must all shift with regime |
| **Four signals** | σ_ratio (magnitude), VPIN (informed flow fraction), OFI (book pressure), price_path (confirmed direction) |
| **Regime-conditional params** | Two calibration sets (calm/trending) per asset; classifier blends between them |
| **Spike response** | Cancel-all immediately; re-quote only after σ stabilises |
| **Professional standard** | Probabilistic classifier + walk-forward validation + per-asset training |

---

### Layer 11 — Post-Fill Monetization

#### Naive Failure

You post a bid at 99.90. It fills. Now what?

Naive response: "great, I have a position, I'll just wait for the other side to fill and collect the spread."

What actually happens:
- The fill arrived because someone wanted to sell to you. They usually know why.
- Price drifts against you. Your bid-fill at 99.90 sees mid move to 99.80 within 3 seconds.
- You never get the ask fill. You eventually exit at 99.85 with a loss.

The naive mistake: treating a fill as a completed trade. A fill is actually two events:
1. **Entry edge locked**: you captured half the spread. This is permanent and already won.
2. **Inventory created**: you now own a position that costs you carry every second you hold it.

These two events require completely different management. Getting event 1 right (spread, adverse selection) is what Layers 1–10 cover. Managing event 2 is what Layer 11 covers.

---

#### The Four Exit Paths

After every fill, you have exactly four ways to exit the inventory:

**Path 1: Passive recycle (preferred)**
- Skew your ask side tighter — post on the other side of the spread
- Wait for an opposing fill from natural flow
- Cost: zero taker fees. You collect the spread on both legs.
- Downside: takes time. During that time, inventory drift can erase the entry edge.

**Path 2: Trailing stop (opportunistic)**
- If price moves favorably after a bid fill (price goes up), ride it
- Arm a trailing stop when unrealised PnL exceeds a threshold (e.g. 0.5× natural spread)
- Stop fires when price gives back 20% of the peak gain
- Example: bid fills at 99.90, price rises to 100.10. Trail stop arms. Price falls to 100.06. Stop fires at 100.06. Net: +$0.16 on the inventory (above the entry edge).
- Research: Leung-Zhang 2019, Cartea-Sanchez-Betancourt 2025.

**Path 3: Predictive exit (signal-triggered)**
- A signal says: price is about to move adversely. Exit before the drift materialises.
- Triggers: leading indicators — OFI shows one-sided pressure, Hawkes process acceleration, informed-flow score spike.
- Exit order: limit (GTX preferred) or IOC if signal strength is high.
- This is a pre-emptive exit, not a reaction to actual adverse price movement.

**Path 4: Aggressive IOC exit (loss-cutting)**
- Cancel all maker orders, fire an IOC taker on the opposing side.
- This locks in a certain small loss (taker fee + half-spread crossing).
- Used when: (a) carry cost will exceed IOC cost, or (b) adverse drift is already occurring.
- Critical understanding: **IOC exit is NOT profit-taking. It is damage control.**

---

#### The IOC Exit — Why It Always Loses Money

People assume you can "exit profitably" with an aggressive IOC. You cannot. Here is why:

**Binance USDT-M standard tier example (SUI, 1 lot = $3.50 notional):**

```
Entry: Bid fills at 99.90. You captured +0.5 ticks of spread (entry edge).
Exit via IOC: You sell at 99.88 (market impact: −0.1 tick) + taker fee 0.05% = −0.35 tick.

Spread captured: +0.5 ticks
IOC taker fee:   −0.35 ticks  (0.05% × 2 legs, or just exit leg depending on venue)
Exit crossing:   −0.1 tick    (half of the current spread you cross)
Entry maker fee: +0.02% rebate = +0.14 ticks  (Binance rebate if you hold VIP)

Net at standard tier: +0.5 − 0.05% on bid entry − 0.05% on IOC exit − 0.1 crossing
                     ≈ +0.5 − 0.35 − 0.35 − 0.1 = −0.20 ticks net loss
```

The round-trip costs roughly 4 ticks total at standard tier. You captured 0.5 ticks on entry. IOC exit leaves you −3.5 ticks net — deeply negative.

**The decision is: certain small loss (IOC now) vs uncertain large loss (hold through adverse drift).**

IOC is the RIGHT choice only when:
```
carry_cost(t) > IOC_exit_cost
carry_rate × t > fee_bps × notional
```

Where `carry_rate = inventory_notional × σ_daily / 86400` per second.

**At VIP 5+** (Binance: maker 0.00%, taker 0.017%): IOC exit cost collapses to ~0.35 ticks net. Then the tradeoff genuinely changes and IOC becomes viable for much shorter hold durations.

---

#### The Maker-First Timer

Before firing an IOC, institutions first try a maker limit order on the exit side. The timer for how long to wait is NOT arbitrary — it is derived from the observed fill rate on that side.

**Poisson model**: opposing fills arrive at rate λ_exit_side (fills per second).

```
P(no fill in time t) = e^(-λ × t)
```

Set the no-fill threshold at 5%: solve for t:

```
t* = −ln(0.05) / λ_exit_side = 3.0 / λ_exit_side
```

**Per-asset examples:**

| Asset | Opposing side fill rate | Maker-first timer t* |
|---|---|---|
| SUI (liquid, skewed) | 500 fills/hour ≈ 0.14/s | ~21 seconds |
| BCHUSDC (medium) | 40 fills/hour ≈ 0.011/s | ~4.5 minutes |
| Thin token | 10 fills/hour ≈ 0.003/s | ~18 minutes |

**Three adjustments to t*:**

1. **Regime**: trending market collapses λ_exit_side (opposing fills dry up). Shorten t* proportionally.
2. **Skew level**: the tighter you skew the exit side, the higher the effective λ. Tighter skew → shorter wait.
3. **Carry ceiling**: if carry_cost(t*) > IOC_exit_cost, cap t* at the carry breakeven time regardless.

Research anchor: Cartea-Jaimungal 2015 — optimal switching time from limit to market order under Poisson arrival.

---

#### The Full Per-Fill Exit Pipeline

Each fill triggers a structured pipeline:

```
Phase 0 — At fill (< 1ms)
  Record fill price, time, side, notional
  Compute IOC_exit_cost (fixed threshold for this fill's lifecycle)
  Start carry clock

Phase 1 — Immediate skew (< 1ms)
  Skew exit side tighter on ALL quoting venues
  Existing resting orders on exit side move toward BBO

Phase 2 — Natural exit hunt (ongoing)
  Maker race on exit side across all venues simultaneously
  P(fill on any of N venues) = 1 − (1−p)^N
  Multi-venue internalisation advantage: N venues multiply the fill probability

Phase 3 — Carry clock check (every cycle)
  expected_carry_to_fill = carry_rate × (1/λ_exit_side)
  If expected_carry_to_fill > IOC_exit_cost → escalate to Phase 4
  If trending regime → λ_exit_side drops → escalate faster

Phase 4 — IOC escalation (when carry clock triggers)
  Cancel ALL maker orders first (avoid double execution)
  Then fire IOC on the cheapest taker venue

Phase 5 — Post-exit markout feedback (calibrate threshold)
  Record: did price continue adversely after exit? Or did it revert?
  Use this to recalibrate the carry threshold over time.
```

**The double-taker trap**: never fire taker IOC while maker orders are still live. If the maker fills AND the taker fires simultaneously, you have a double-taker round trip on one inventory lot. Cancel first, always.

---

#### Cross-Venue Hedge Lifecycle

When you hedge on another venue:

1. Primary fill: Binance bid fills. Net: +1 lot on Binance.
2. Hedge: fire IOC or limit sell on BitMEX. Net: +1 Binance, −1 BitMEX → net 0.
3. You are now delta neutral. Done?

**No. The hedge position becomes independent inventory.**

After the Binance primary position exits (via natural fill or IOC), the BitMEX short remains. It is now a naked short on BitMEX. It enters the SAME passive-first exit pipeline — skew buy side on BitMEX, wait for opposing fill, fall back to IOC if carry exceeds cost.

**Double-duty rule**: if a second Binance bid fill arrives while the BitMEX short is still live, the BitMEX short can hedge BOTH Binance fills simultaneously. This is the key internalisation win — the same hedge leg serves multiple primary fills before it needs to be unwound.

**Break-even for same-venue vs cross-venue IOC exit:**

```
Cross-venue maker pays rebate if fill, saves taker if fill.
Break-even: P(maker fill on hedge venue) > IOC_exit_cost_on_primary / maker_rebate_on_hedge
```

On BitMEX (maker rebate = 0.01%, primary taker = 0.05%):
```
P_fill × 0.01% − (1−P_fill) × 0.075% > −0.05%
Solve: P_fill > 29%
```

If P(maker fill on BitMEX within t*) > 29% for this asset in this regime → cross-venue maker is better. Otherwise → same-venue taker IOC wins.

---

#### Sees vs Misses

| Approach | What it sees | What it misses |
|---|---|---|
| Hold-and-hope | Zero fees on exit | Carry cost, adverse drift, regime shifts |
| Always-IOC exit | Bounded drawdown per fill | Unnecessary fee cost when fill rate is high |
| Fixed-time carry ramp (30s/60s) | Simple time-based urgency | σ_daily variation across assets; liquid asset bleeds in 5s, thin asset safe for 10min |
| Poisson maker-first timer | Asset-calibrated urgency | Regime adjustment needed (λ collapses in trending) |
| Multi-venue maker race | Highest P(passive exit) | Requires coordinated cancel-then-IOC across venues |

---

#### Professional Standard

| Component | What they do |
|---|---|
| Immediate skew | < 1ms after fill — skew exit side on all venues, don't wait |
| Maker-first timer | t* = −ln(0.05)/λ_exit_side per asset, regime-adjusted |
| Carry threshold | carry_rate × t* vs IOC_exit_cost — explicit per-asset computation |
| Multi-venue maker race | Post limit on all hedge venues, cancel all when first fills |
| IOC as loss-cutting only | Never triggered for "profit-taking" — only when carry > IOC cost |
| Post-exit markout feedback | Exit decision quality measured: did price continue adversely? |
| Double-duty hedging | Single hedge leg serves multiple primary fills before unwinding |
| Internalisation priority | Natural opposing flow > skewed opposing fill > same-venue IOC > cross-venue IOC |

---

#### Summary

| | |
|---|---|
| **What it is** | Per-fill pipeline to exit the inventory created by each maker fill |
| **Two events** | Entry edge (locked, permanent) + inventory (must be managed, costs carry) |
| **Four paths** | Passive recycle (preferred) → trailing stop → predictive exit → IOC (loss-cutting) |
| **IOC truth** | Always a net loss at standard tier; the decision is certain small loss vs uncertain large loss |
| **Maker-first timer** | t* = −ln(0.05)/λ_exit_side — per-asset, regime-adjusted, carry-bounded |
| **Cross-venue hedge** | Hedge position becomes independent inventory after primary exits |
| **Professional standard** | Maker race across venues → Poisson-calibrated IOC fallback → post-exit feedback loop |

---

#### Extension: Same-Venue vs Cross-Venue Exit — Two Modes

Every taker IOC exit has two route choices. Which one you take determines your fee economics. These are not the same thing and neither is always better.

---

##### Mode A — Same-Venue Exit Chain

After a bid fill on Binance USDT-M:

```
T=0ms     Fill arrives → long +1 Binance
           Immediately: skew ask side tighter across ALL venues
           L1 ask order already resting on Binance (normal quote cycle)

T=0 → t*  [Natural exit window]
           Any natural seller on Binance hits resting ask → flat, zero fee
           Any opposing fill on another venue → internalised → flat, zero fee

T=t*      [Carry clock fires: carry_rate × t* ≥ IOC_exit_cost]
           Step 1: post LIMIT SELL at BBO on Binance (maker attempt)
           Step 2a: fills as maker → zero fee (spread collected both legs)
           Step 2b: timer expires → IOC SELL on Binance → 0.05% taker fee

Fee outcome:
  Natural exit:    0%    (both legs maker)
  Maker-first:     0%    (maker on ask side)
  IOC fallback:    0.05% (Binance standard taker)
```

Mode A is the short path: two positions, one venue, one symbol. The fallback fee is capped at 0.05%.

---

##### Mode B — Cross-Venue Hedge Chain

After a bid fill on Binance USDT-M:

```
T=0ms     Fill arrives → long +1 Binance
           Simultaneously: skew ask side on ALL venues (same as Mode A)
           AND: start cross-venue maker attempt on cheapest hedge venue (BitMEX)

T=0 → t*  [Parallel — natural exit AND cross-venue maker attempt running simultaneously]

           Route A: Binance natural ask fills → flat. Cancel cross-venue attempt. Done.

           Route B: Cross-venue maker fills on BitMEX
             State: +1 Binance long, −1 BitMEX short = delta neutral
             Continue waiting for Binance natural ask fill (carry ≈ 0, delta = 0)
             When Binance ask fills naturally:
               Binance flat. Orphaned: −1 BitMEX short still open.
               Post LIMIT BUY at BitMEX BBO (maker attempt for unwind)
               If fills: fully flat. BitMEX earned another +0.01% rebate.
               If timer expires: IOC BUY on BitMEX → 0.075% taker fee.

           Route C: Cross-venue maker did NOT fill in t*
             IOC SELL on BitMEX → 0.075% taker fee
             Delta neutral. Continue natural Binance exit pipeline.

Fee outcome:
  All-maker path:  −0.01% − 0.01% = −0.02% net income (rebates on both BitMEX legs)
  Mixed path:      0.075% (one IOC leg) + 0% or +0.01% (other leg)
  Worst path:      0.075% × 2 = 0.15% round-trip on BitMEX (two IOC legs)
```

Mode B is the long path: three or four position transitions. The all-maker path earns income. The IOC fallback is significantly more expensive than Mode A (0.075% vs 0.05%).

---

##### Break-Even: When Does Mode B Beat Mode A?

Let P = probability of maker fill on the hedge venue within t*.

```
Expected cost:
  Mode A: (1−P_A) × 0.05%
  Mode B: P_B × (−0.01%) + (1−P_B) × 0.075%

B beats A when:
  P_B × (−0.01%) + (1−P_B) × 0.075% < (1−P_A) × 0.05%

Assuming P_A ≈ P_B = P (same asset, same skew level):
  0.075 − 0.085P < 0.05 − 0.05P
  P > 71%
```

**Mode B via BitMEX only beats Mode A when P(maker fill cross-venue within t*) > 71%.**

Per-venue break-even table:

| Hedge Venue | Maker fee | Taker fee | Break-even P | Verdict |
|---|---|---|---|---|
| BitMEX | −0.01% (rebate) | 0.075% | P > 71% | Use only on high-liquidity assets on BitMEX |
| Bybit | 0% | ~0.055% | P > 100% | Never beats Mode A — same cost, no rebate |
| Gate.io | 0% | 0.05% | P > 100% | Same economics as Mode A — no advantage |

For most assets, Mode A wins. Mode B via BitMEX is worth attempting on liquid perpetuals (SUI, SOL, BTC) where BitMEX books are active enough to give P > 71%.

---

##### A/B Measurement Framework

Theory gives the break-even P; live data gives the actual P for each asset. The right approach: run both modes alternately, measure, select the winner per asset.

**Per-fill exit record to log:**

```json
{
  "fill_id": "...",
  "exit_mode": "A_same_venue | B_cross_venue",
  "exit_method": "natural | maker_first | ioc_fallback",
  "time_to_exit_ms": 4200,
  "exit_cost_bps": 0.05,
  "post_exit_drift_1s_ticks": -0.2
}
```

**Per-asset rolling comparison (200-fill window per mode):**

```
Asset: SOLUSDC
Mode A (180 fills): avg_exit_cost 0.021%, natural_exit_rate 73%, ioc_rate 27%
Mode B (180 fills): avg_exit_cost 0.018%, maker_hedge_rate 61%, ioc_rate 39%
Winner: Mode B (−0.003% per fill advantage → select Mode B for this asset)
```

**Mode selection rule:**

```python
def select_exit_mode(asset):
    if mode_B_fills < 100:         # insufficient data → use A (safe default)
        return "A"
    delta = mode_A_cost - mode_B_cost
    if delta > HYSTERESIS_BPS:     # 0.003% hysteresis prevents flapping
        return "B"
    return "A"
```

Re-evaluate every 1000 fills — regime changes invalidate prior measurements.

---

##### Unified State Machine (All 7 Mechanisms Integrated)

Complete per-fill flow incorporating internalisation, skew, maker-first, carry clock, and regime logic:

```
FILL_ARRIVES
│
├─ T=0ms (always, regardless of mode)
│   ├─ Skew exit side tighter on ALL venues
│   ├─ L1 exit order already resting — no action needed
│   └─ Check UnifiedPositionLedger: did opposing fill already arrive on any venue?
│       YES → internalised, flat, zero fee. DONE.
│
├─ T=0 → carry_threshold [Natural window — all mechanisms run in parallel]
│   Every opposing fill on any venue → check net delta → if flat: DONE.
│
├─ T=carry_threshold [Mode-selected exit]
│   MODE A path:
│   ├─ Post LIMIT SELL at BBO on same venue
│   │   t* = −ln(0.05) / λ_exit_side_same_venue, regime-adjusted
│   └─ t* expires → IOC SELL on same venue [0.05% taker]
│
│   MODE B path:
│   ├─ Post LIMIT SELL at BBO on BitMEX
│   │   t* = −ln(0.05) / λ_exit_side_bitmex, regime-adjusted
│   ├─ Fills as maker → delta neutral → continue waiting for natural Binance exit
│   │   When Binance exits naturally → unwind BitMEX via maker
│   └─ t* expires → IOC SELL on BitMEX [0.075% taker — expensive]
│
├─ REGIME OVERRIDE (continuous — overrides all timers)
│   Trending detected → collapse t*, escalate immediately
│   Near funding window → max hold = 3 min pre-window
│   σ spike → force_exit Layer A (30→60s ramp) fires, overrides mode logic
│
└─ POST-EXIT FEEDBACK (every exit)
    Record: exit_method, time_to_exit_ms, exit_cost_bps, post_exit_drift_1s
    Update: λ_exit_side EWMA for this (asset, venue) pair
    Update: mode A/B rolling cost table → re-evaluate mode selection
```

---

##### What Needs to Be Built (Implementation Stack)

In priority order — each line is a prerequisite for the line below it:

| # | Component | Purpose | Mode |
|---|---|---|---|
| 1 | **λ_exit_side tracker** | Rolling EWMA of opposing fill rate per (asset, venue) — foundational for t* | Both |
| 2 | **Per-asset t* computation** | −ln(0.05)/λ, regime-conditional, carry-bounded | Both |
| 3 | **HedgeRouter maker-first phase** | Post limit on hedge venue at t*; cancel → IOC fallback | Mode B |
| 4 | **Per-fill exit mode tag** | Log `exit_mode` + `exit_method` to fills.jsonl | Both |
| 5 | **Per-asset A/B rolling stats** | avg_exit_cost_bps per mode over 200-fill window | Both |
| 6 | **Mode selector** | Hysteresis comparison → runtime mode flag per asset | Both |

The λ_exit_side tracker (item 1) is the foundation everything else builds on. Without it, t* is a guess and mode selection is blind. Start there.

---

### Layer 12 — GPNL Attribution Decomposition

#### Naive Failure

The engine is gpnl-negative. What do you do?

Naive response: widen the spread. Or tighten the spread. Or change k_tox. Or run more assets.

None of these are the right first move because "gpnl is negative" contains no information about WHY. You cannot fix what you cannot locate. A day where you bled $5 from adverse selection and earned $2 from spread looks identical in the total to a day where you bled $4 from carry and earned $1 from spread. They require completely different fixes.

Attribution decomposition breaks the total into independently measurable components so each component can be diagnosed and fixed in isolation.

---

#### The Decomposition Formula

Every maker fill contributes:

```
fill_contribution = spread_captured
                  − adverse_selection
                  − inventory_carry
                  − exit_cost
                  − fee_cost
```

Summed across all fills in a session:

```
GPNL = spread_captured_total
       − adverse_5s_total       (post-fill price drift against position)
       − inv_holding_total      (cost of carrying net inventory over time)
       − hedge_slippage_total   (crossing cost on hedge IOC legs)
       − exit_cost_total        (crossing cost on same-venue IOC exits)
       − fee_total              (taker fees net of maker rebates)
       + unexplained_residual   (measurement gap — should be near-zero)
```

The residual is not rounding error — it is a falsification signal. A large non-zero residual means you have a measurement bug: double-counting, sign flip, missing leg, or parser anomaly. It is the system checking itself.

---

#### Component by Component

**1. Spread Captured** (entry edge — always positive if quoting correctly)

```
spread_captured = Σ_ask_fills (ask_price − mid_at_fill) × size
                + Σ_bid_fills (mid_at_fill − bid_price) × size
```

What it measures: how much of the spread you earned on each maker fill. If this is low, your quotes are too close to mid (getting adversely selected before fill) or you are not getting enough fills (too wide).

Diagnostic: `cost_spread_captured_window_usd` in diag.jsonl. Compare to the theoretical half-spread × fill_count — if they diverge, mid is stale at fill time.

---

**2. Adverse Selection** (the primary leak)

```
adverse_5s = Σ_fills post_fill_price_drift_5s × fill_size × side
```

What it measures: how much price moved against you in the 5 seconds after each fill. A bid fill followed by price falling = adverse selection on that fill. Averaged across many fills this is the per-fill toxicity cost.

Diagnostic: `cost_adverse_5s_window_usd` in diag.jsonl. If `|adverse_5s| > spread_captured`, the engine is paying more in adverse selection than it earns in spread. This is the primary profitability failure mode.

Actionable fixes: Layer 2 (TailScore), Layer 3 (latency — cancel before sniped), Layer 10 (regime — widen in trending).

---

**3. Inventory Carry** (the holding cost)

```
inv_holding = Σ_periods net_qty × mark_price × σ_1s × hold_seconds
```

Measured as a time-integral: every second you hold net inventory, you accumulate carry proportional to inventory size and instantaneous volatility. In calm markets this is small. In trending markets after a bad fill it compounds rapidly.

Diagnostic: `cost_inv_holding_window_usd` in diag.jsonl. High inv_holding relative to spread_captured means inventory is not recycling fast enough (Layer 5, Layer 11).

---

**4. Hedge Slippage** (cost of crossing on hedge venue)

```
hedge_slippage = Σ_hedge_fills (mid_at_hedge_dispatch − hedge_fill_price) × side × size
```

What it measures: how much worse than mid you executed on the hedge leg. A large hedge_slippage means your hedge IOC is crossing a wide spread or hitting during adverse conditions on the hedge venue.

Diagnostic: `cost_hedge_slippage_window_usd`. High hedge_slippage while adverse_5s is also high = you are both getting adversely filled AND paying to hedge. Double bleed.

---

**5. Exit Cost** (same-venue IOC crossing)

```
exit_cost = Σ_exits (mid_at_exit_decision − exit_fill_price) × side × size
```

Separate from hedge_slippage — this is the cost of exiting on the SAME venue via taker IOC. Isolates same-venue exit decisions from cross-venue hedge decisions.

Diagnostic: `cost_exit_cost_window_usd`. High exit_cost means your IOC exits are crossing wide (adverse timing) or the carry threshold is too conservative (exiting too late, into worse prices).

---

**6. Fee Cost** (net of rebates)

```
fee_cost = Σ_taker_exits taker_fee × notional
         − Σ_maker_fills maker_rebate × notional
```

At standard tier: Binance maker −0.02% (cost), taker +0.05% (cost). Net per round trip ≈ 0.07%.
At VIP 5: maker rebate, taker ≈ 0.017%. Net ≈ near-zero.

Diagnostic: `cost_fee_rebate_window_usd`. This component should be the smallest — if it is large, VIP tier is too low or too many taker exits are firing.

---

#### Fill-Type Classification

After computing per-fill contribution, classify every fill into three types:

```
fill_contribution_i = spread_captured_i − adverse_5s_i − carry_i − exit_i − fees_i

Type A: fill_contribution_i > 0                    profitable fill
Type B: −spread_captured_i < fill_contribution_i ≤ 0    break-even (lost some spread)
Type C: fill_contribution_i < −spread_captured_i   catastrophic (adverse selection > spread)
```

A healthy session: 70%+ Type A, <10% Type C.
A bleeding session: <40% Type A, >25% Type C.

Type C fills are the primary target. Track WHAT CONDITION was present at each Type C fill:

| Condition at fill time | Root cause | Fix |
|---|---|---|
| VPIN > 0.6 at fill | Informed flow — fill was toxic | Layer 2: raise k_tox, widen |
| σ_spike in prior 500ms | Stale quote — mid moved before fill | Layer 3: reduce max_quote_age |
| Queue position = back (q_pos_norm < 0.2) | Sweeper fill | Layer 4.5: restrict deep fills |
| regime_idx = TRENDING | Structural adverse selection | Layer 10: trending regime param switch |
| t_held_inv > 60s | Carry accumulation without exit | Layer 11: carry threshold too loose |

---

#### The Attribution Waterfall

The professional way to present attribution is as a descending bar chart from left to right:

```
+spread_captured     = +$8.40    ← earned
−adverse_selection   = −$5.20    ← biggest leak
−inv_holding         = −$1.80    ← second leak
−hedge_slippage      = −$0.60
−exit_cost           = −$0.30
−fees                = −$0.40
──────────────────────────────
GPNL                 = +$0.10    ← what survived

residual             = −$0.03    ← near-zero: attribution clean
```

This waterfall tells you exactly where to look. In this example: adverse_selection is eating 62% of spread_captured. Fix Layer 2 and Layer 10 first. Inventory carry is second: fix Layer 11 exit timing. Everything else is noise by comparison.

---

#### The Residual as a Bug Detector

```
residual = realized_GPNL − Σ(all 7 components independently measured)
```

This should be close to zero. If it is not:
- Large positive residual → a component is underestimating costs (missing leg, sign error)
- Large negative residual → a component is overestimating costs (double-count)

The residual cannot be tuned away by adjusting the engine. It can only be zeroed by fixing the measurement. This makes it uniquely honest — unlike any engine metric that could be gamed by parameter changes.

---

#### Sees vs Misses

| Approach | What it sees | What it misses |
|---|---|---|
| "GPNL is negative" | Total outcome | Nothing actionable |
| Markout analysis alone (Layer 1) | Adverse selection | Carry, exit cost, fees |
| Full attribution waterfall | All 7 components | Root cause per fill (need classification) |
| Fill-type classification | Which fills are toxic | Why they are toxic (need condition tags) |
| Root-cause tagging | Exact condition at each Type C fill | Requires per-fill condition snapshot at fill time |

---

#### Professional Standard

| Component | What they do |
|---|---|
| 7-component waterfall | Run after every session automatically; visible in the operator dashboard |
| Reconciliation residual | Non-zero residual triggers measurement audit before any strategy change |
| Fill-type classification | Every fill labelled A/B/C at session end; Type C % is a health metric |
| Root-cause tagging | VPIN, σ, queue_pos, regime_idx all snapshotted at fill time and joined to fill record |
| Component trend | Week-over-week: is adverse_5s improving? Is carry improving? Track each independently |
| Attribution before tuning | Any parameter change requires attribution delta — did that component improve? |

---

#### Summary

| | |
|---|---|
| **What it is** | Decomposing GPNL into independently measurable sources of gain and loss |
| **Formula** | GPNL = spread_captured − adverse_5s − inv_holding − hedge_slippage − exit_cost − fees + residual |
| **Why it matters** | "GPNL negative" is not actionable; "adverse_5s exceeds spread_captured by 62%" is |
| **Fill types** | A (profitable) / B (break-even) / C (catastrophic — adverse > spread) |
| **Root cause** | VPIN / σ spike / queue position / regime at Type C fill time → maps to a specific layer fix |
| **Residual** | Not noise — a falsification signal for measurement bugs |
| **Professional standard** | Waterfall report every session + fill-type % + root-cause tag per Type C fill |

---

### Layer 13 — Validation Discipline

#### Naive Failure

You make a change. You run the sim. The result is better. You ship it.

Three things just went wrong:

1. The sim may not represent live conditions — if it diverged >25% from live before the change, the "improvement" is fabricated.
2. Running the sim once on one scenario is not a test — it is a single sample from a random process. One lucky seed looks the same as a real improvement.
3. If you tried 10 parameter combinations and picked the best, the best will look good by chance even if none of them are genuinely better. You have not validated; you have overfit.

Validation discipline is the framework that separates genuine improvements from noise and luck.

---

#### The Validation Ladder

Three rungs. Each one is a necessary condition for the next. You cannot skip a rung.

```
Rung 1 — Sim
  Floor test, not proof. Catches structural bugs and direction of effect.
  Required: ±25% fidelity gate, multi-seed, multi-scenario, baseline comparison.
  What sim cannot tell you: queue position effects, real latency, partial fills,
  venue-specific quirks, regime persistence.

Rung 2 — Testnet
  Real order flow, real latency, real venue behavior. No real money.
  Required: ≥40 fills, same session conditions as a live session.
  What testnet cannot tell you: real adverse selection (counterparty risk profile
  on testnet differs from mainnet), VIP tier fee effects.

Rung 3 — Mainnet (ground truth)
  The exchange is the final verdict. Every claim about the engine
  is a hypothesis until confirmed here.
  Required: capital-safety gate, canary period, attribution delta from the
  waterfall showing the TARGET component improved.
```

---

#### What Makes a Sim Result Trustworthy

**Condition 1 — ±25% Fidelity Gate (prerequisite)**

Before any sim result is meaningful, the sim must track live GPNL within ±25% per asset on the most recent live session. If sim says +$5 and live said −$8 before the change, the sim is not modeling the engine's actual behavior. Anything it says about the change is noise.

If fidelity is broken, fixing fidelity is priority zero before any strategy work.

**Condition 2 — Multi-Seed WITH Scenario Regen**

A critical distinction that most people get wrong:

```
Wrong:  run sim with --seed=1, --seed=2, --seed=3 on the SAME scenario
        → tests engine's internal RNG only, not scenario variance
        → looks like robustness, is not robustness

Right:  run generate_scenario.py --seed=1, generate_scenario.py --seed=2, ...
        → generates 3 different market scenarios with different adverse flow,
          different timing, different regime sequences
        → true robustness across scenario space
```

A result that holds on 4 genuine multi-seed scenarios is approximately 2.5× more meaningful than a same-scenario multi-seed result.

**Condition 3 — Multi-Regime Coverage**

At minimum: one calm scenario, one trending scenario, one volatile scenario. A change that improves calm regime and destroys trending regime is not an improvement — it is a regime-conditional bug that will hurt on the next trending session.

**Condition 4 — Baseline Comparison**

The sim result of the change is meaningless without the sim result of the UNCHANGED engine on the same scenarios. The change must be compared to the baseline on identical inputs, not to a prior session's result or a remembered number.

---

#### Statistical Validity — Sample Size and Multiple Testing

**The MinTRL problem**

Every Sharpe ratio is estimated from a finite sample. With fewer fills, the estimate is noisier. The Minimum Track Record Length (MinTRL) tells you how many fills you need before the Sharpe is statistically meaningful:

```
MinTRL ≈ 1 + (z_α / SR_hat)² × (1 + skew correction)
```

If SR_hat = 1.0 and you want 95% confidence: MinTRL ≈ 60–80 fills minimum, depending on skew.

Below MinTRL, a positive Sharpe could easily be luck. This is why the 40-fill checkpoint exists as a minimum gate before a long run — 40 fills is approximately the minimum to rule out pure chance at typical SR levels for a single-asset session.

**The multiple testing problem**

If you run 10 parameter combinations and pick the best, expect roughly 1 false positive by chance at 5% significance. The more combinations you test, the more likely the winner is noise. This is called p-hacking in research; in trading it is called overfitting.

The Deflated Sharpe Ratio (Bailey & Lopez de Prado 2014) adjusts for this:

```
DSR = Sharpe × correction_factor(skew, kurtosis, n_trials)
```

Where n_trials is the number of parameter sets you tested before picking this one. If you tested 10 sets and picked the best, the DSR is meaningfully lower than the raw Sharpe. A high DSR means the result is robust to the search process.

Practical rule: if you changed one thing and validated it on a fresh scenario, DSR ≈ Sharpe. If you swept 20 values and picked the best, DSR tells you whether the winner was genuine.

---

#### The Validate-Freeze Approach

Change one thing. Validate it. Freeze it. Then change the next thing.

**Why this is not just good practice — it is the only way to know what worked:**

If you change spread AND k_tox AND deadband simultaneously and the result improves by $3:
- Which change contributed?
- Was the improvement from one change and the others were neutral?
- Did two changes fight each other and the result was net-positive despite internal conflicts?
- If it regresses next session, which parameter do you roll back?

You cannot answer any of these questions. Simultaneous changes make attribution impossible.

**The four layers in order (from validate-freeze memory):**

```
Layer 1: Toxicity (k_tox, k_tox_gate, TailScore threshold)
   → Validate: adverse_5s component improves
   → Freeze before touching:

Layer 2: EV hold (spread_floor, EV threshold, d* minimum)
   → Validate: edge per fill improves, fill rate acceptable
   → Freeze before touching:

Layer 3: P(fill) (deadband, hold_ms, quote depth)
   → Validate: fill rate improves without adverse selection worsening
   → Freeze before touching:

Layer 4: Spread width (base_spread, k_vol_spread)
   → Validate: spread_captured component improves
```

Only move down the list when the current layer is validated and frozen.

---

#### What Invalidates a Validation Result

These are the failure classes that have cost real money in prior cycles:

**Bug-induced prior wins (GH#109 pattern)**
A bugfix improves the result. But the prior "positive" results depended on the bug. After the fix, prior wins flip to losses because they were artifacts of the broken behavior. Always re-run baselines after a bug fix — a prior win that disappears after a bug fix was a Potemkin result.

**Same-scenario multi-seed**
Running the same scenario with different seeds tests only engine RNG, not scenario robustness. A result that "held across 4 seeds" on one scenario is approximately as meaningful as 1 seed. The 4-seed improvement will not hold in live when the scenario changes.

**Single-session dependence**
A parameter tuned to one live session is overfit to that session's regime. Standard test: the improvement must hold on session N+1 (walk-forward) at ≥70% of the magnitude. If the walk-forward result is less than 70% of the training result, the parameter is overfit.

**Sim diverged before validation**
If the sim was not within ±25% of live before the change, the sim result is meaningless. Validating on a broken sim produces guaranteed-invalid results, even if the numbers look good.

**Optimizing and fixing simultaneously**
Changing a bug fix AND a parameter improvement in the same iteration makes it impossible to separate their contributions. If it regresses, you cannot know which to roll back. Fix bugs alone, then optimize in the next iteration.

---

#### Sees vs Misses

| Approach | What it sees | What it misses |
|---|---|---|
| Run sim once, take result | Quick feedback | Scenario variance, fidelity gap, multiple testing inflation |
| Multi-seed same scenario | Engine RNG robustness | Real scenario diversity — this is not multi-seed |
| Multi-seed + scenario regen | True scenario robustness | Regime coverage (must add trending/volatile scenarios) |
| Walk-forward validated | Out-of-sample hold | Whether the target attribution component actually improved |
| Deflated Sharpe | Adjusts for number of trials | Requires accurate n_trials count — if you forgot some iterations, DSR is understated |

---

#### Professional Standard

| Component | What they do |
|---|---|
| ±25% fidelity gate | Mandatory before any validation run; broken fidelity = stop all strategy work |
| Multi-seed scenario regen | Each seed regenerates the full scenario via generate_scenario — not just engine RNG |
| Multi-regime coverage | Calm + trending + volatile at minimum; never validate on one regime only |
| Baseline comparison | Every result compared to the unmodified engine on identical inputs |
| Walk-forward | 70% train / 30% validate; result must hold ≥70% in walk-forward |
| Deflated Sharpe | Adjusts raw Sharpe for skew, kurtosis, and number of prior trials |
| MinTRL | Do not interpret Sharpe below the minimum track record length |
| Validate-freeze | One layer at a time; never change toxicity and spread in the same iteration |
| Attribution delta | At mainnet: confirm the TARGET component (e.g. adverse_5s) improved, not just total GPNL |
| Canary period | 10-second startup canary; STOP armed; bleed threshold set before any mainnet run |

---

#### Summary

| | |
|---|---|
| **What it is** | The discipline of separating genuine improvements from noise, luck, and overfitting |
| **The ladder** | Sim (floor) → Testnet (real flow) → Mainnet (ground truth). Cannot skip rungs. |
| **Sim trustworthiness** | ±25% fidelity gate + scenario-regen multi-seed + multi-regime + baseline comparison |
| **Statistical validity** | MinTRL (minimum fills for Sharpe to be meaningful) + DSR (adjusts for number of trials) |
| **Validate-freeze** | One change → validate → freeze → next change. Simultaneous changes make attribution impossible. |
| **Key invalidations** | Bug-induced prior wins / same-scenario seed / single-session overfit / sim diverged / simultaneous changes |
| **Professional standard** | Walk-forward + DSR + attribution delta (did the target component actually improve?) |

---
