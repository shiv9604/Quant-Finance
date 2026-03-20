# Market Making

Market making is way to provide liquidity on perticular asset or in market provide to keep that instrument tradeable and earning profit from the bid and ask spread.

---
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
### Core Architecture of a Market Maker

A market maker continuously posts a bid and an ask around an internal estimate of fair value. The goal is not to predict direction but to price risk, manage inventory, and optimize expected value per trade. The business model is to earn small spreads repeatedly while controlling losses from adverse selection.

**Pillar 1 — Fair Value Estimation -**
1. Fair value is the internal estimate of what the asset should trade at right now.
2. It is not the last traded price.
3. If fair value is wrong, the market maker gets picked off.
4. Fair value can be derived from:
   - Mid price.
   - Cross-exchange prices.
   - Order book imbalance.
   - Short-term momentum.
   - Funding rates (in perpetual markets).
5. Fair value is the anchor of the entire quoting system.

**Pillar 2 — Spread Setting -**
1. Once fair value (F) is estimated:
   - Bid = F − half_spread.
   - Ask = F + half_spread.
2. Spread is compensation for risk.
3. Spread accounts for:
   - Adverse selection risk.
   - Volatility.
   - Inventory risk.
   - Trading fees.
4. Higher volatility → higher adverse risk → wider spread.
5. Spread is dynamic and must adjust to market conditions.

**Pillar 3 — Inventory Management -**
1. A market maker will not remain flat at all times.
2. Imbalanced order flow causes inventory buildup.
3. Inventory introduces directional exposure.
4. If unmanaged, inventory risk can wipe out spread gains.
5. Inventory is controlled by:
   - Skewing quotes.
   - Adjusting spread asymmetrically.
   - Reducing quote size.
   - Hedging when necessary.
6. Inventory control is essential for long-term survival.

**Structural Relationship -**
1. Fair value determines where to quote.
2. Spread determines how much risk premium to charge.
3. Inventory determines how aggressively to lean quotes.
4. All three pillars interact continuously.
5. Market making is the optimization of these three variables under uncertainty.

**Terminologies used in this section -**

- **Half-Spread -**
  1. Half-spread = Spread ÷ 2.
  2. Quotes are typically placed symmetrically around fair value.
  3. If Fair Value (F) = 100 and Spread = 2:
     - Bid = 99.
     - Ask = 101.
  4. Half-spread simplifies quote construction around fair value.
  5. It represents risk premium charged on each side.

- **Fair Value (F) -**
  1. Fair value is the internal estimate of what the asset should trade at right now.
  2. It is not necessarily the last traded price.
  3. It can be derived from:
     - Mid price.
     - Cross-exchange prices.
     - Order book imbalance.
     - Short-term momentum.
     - Funding rates (in perpetual markets).
  4. Accurate fair value estimation is critical to avoid being picked off.

- **Adverse Selection -**
  1. Occurs when someone trades with your quote.
  2. Immediately after the trade, price moves against you.
  3. It implies the counterparty had superior short-term information.
  4. It is the primary structural risk in market making.
  5. Spread must compensate for expected adverse selection cost.

- **Quote Size -**
  1. Quote size is the quantity posted at bid and ask.
  2. Larger size increases exposure per fill.
  3. Smaller size reduces inventory risk.
  4. Size impacts fill rate and inventory accumulation speed.

- **Skewing Quotes -**
  1. Skewing means shifting bid and ask asymmetrically.
  2. It is typically done due to inventory imbalance.
  3. If long inventory:
     - Move quotes downward.
     - Make buying harder.
     - Encourage selling.
  4. If short inventory:
     - Move quotes upward.
     - Make selling harder.
     - Encourage buying.
  5. Skewing helps return inventory toward neutral.

- **Inventory Leaning -**
  1. Leaning is adjusting quotes in the direction that reduces inventory exposure.
  2. It introduces directional bias intentionally.
  3. It is a risk control mechanism.
  4. It prevents uncontrolled inventory accumulation.

- **Symmetric vs Asymmetric Quoting -**
  1. Symmetric quoting:
     - Equal distance from fair value on both sides.
  2. Asymmetric quoting:
     - Unequal distances due to inventory or risk adjustments.
  3. Asymmetry reflects active risk management.
  4. Professional market makers constantly shift between symmetric and asymmetric quoting.

---
### Adverse Selection Mechanics

Adverse selection is the structural risk faced by market makers when counterparties possess superior short-term information. It occurs when a trade happens at a quoted price and the market immediately moves against that quote. Understanding this mechanism is critical for survival.

**What is Adverse Selection -**
1. Adverse selection occurs when someone trades against your quote.
2. Immediately after the trade, price moves in the same direction as the aggressor.
3. This implies the counterparty had better short-term information.
4. The market maker traded at a price that became stale.
5. It is the primary structural risk in liquidity provision.

**Structural Cause -**
1. Information in markets is not evenly distributed.
2. Some participants react faster to:
   - News.
   - Cross-exchange price moves.
   - Order book imbalance.
   - Momentum shifts.
3. Informed traders consume liquidity when price is about to move.
4. Market makers provide liquidity and bear the risk.
5. The loss is structural, not emotional or intentional.

**Latency & Repricing Lag -**
1. Fair value may shift before the market maker updates quotes.
2. Faster traders detect this shift first.
3. They execute against stale quotes.
4. The market maker updates after being filled.
5. The difference between execution price and updated fair value is adverse selection cost.

**Expected Value Perspective -**
1. Expected Profit per fill = Spread − Expected adverse move.
2. If adverse movement exceeds spread, expected value becomes negative.
3. Spread alone does not guarantee profitability.
4. Risk-adjusted spread relative to expected movement determines survival.

**Toxic Flow Clustering -**
1. Adverse selection often clusters rather than occurring randomly.
2. Repeated fills on one side signal predictive flow.
3. Inventory builds in the wrong direction.
4. Price continues drifting after fills.
5. Loss compounds before adaptation.

**Continuous vs Jump Volatility -**
1. Continuous volatility:
   - Fair value moves gradually.
   - Quotes can adapt.
   - Inventory may mean-revert.
   - Spread can compensate over time.
2. Jump volatility:
   - Fair value shifts discontinuously.
   - Quotes instantly become stale.
   - Fills cluster on one side.
   - Price gaps before adjustment.
   - Loss occurs before repricing.
3. Jump volatility is more dangerous because it creates concentrated adverse selection.

**News Event Impact -**
1. News creates information shocks.
2. True fair value changes abruptly.
3. Faster participants react first.
4. Slower quotes remain exposed.
5. Liquidity providers experience elevated adverse selection.
6. During extreme uncertainty, market makers may widen spreads significantly or pull liquidity.

**Core Insight -**
1. Market makers fear variance of fair value more than variance of last traded price.
2. If fair value is stable, volatility is manageable.
3. If fair value is uncertain, quoting becomes dangerous.
4. Survival depends on pricing and reacting to adverse selection risk efficiently.

---
### Inventory Risk & Inventory Dynamics

Inventory is the net position accumulated from filled quotes. While market making aims to remain directionally neutral, inventory introduces temporary directional exposure. Proper inventory control is essential for long-term survival.

**What is Inventory -**
1. Inventory is the net position held due to executed trades.
2. If more sellers hit the bid → long inventory accumulates.
3. If more buyers lift the ask → short inventory accumulates.
4. Inventory is unavoidable in market making.
5. Eliminating inventory completely would eliminate liquidity provision.

**Why Inventory Is Dangerous -**
1. Inventory introduces directional risk.
2. If long and price falls → unrealized loss increases.
3. If short and price rises → unrealized loss increases.
4. Spread gains can be wiped out by large inventory moves.
5. Inventory temporarily converts a market maker into a directional trader.

**Inventory Compounding Risk -**
1. Repeated fills on one side increase exposure.
2. Inventory growth is nonlinear under persistent one-sided flow.
3. Larger inventory increases sensitivity to price movement.
4. Loss accelerates as exposure grows.
5. Weak market makers fail due to uncontrolled compounding inventory.

**Inventory Drift -**
1. Occurs when order flow remains one-sided for a period.
2. Often coincides with informed volatility or trend formation.
3. Inventory builds in the same direction as market drift.
4. Early detection is critical.
5. Ignoring drift leads to escalating exposure.

**Inventory Control Mechanisms -**
1. Quote skewing:
   - Shift quotes in the direction that reduces exposure.
2. Asymmetric spread adjustment:
   - Widen the risky side more than the safer side.
3. Size reduction:
   - Reduce quantity on the side causing imbalance.
4. Hard inventory limits:
   - Define maximum allowable exposure.
5. External hedging:
   - Hedge when exposure exceeds tolerance.

**Spread–Inventory Tradeoff -**
1. Tighter spreads increase fill rate.
2. Higher fill rate accelerates inventory accumulation.
3. Wider spreads reduce fill frequency.
4. Spread decisions directly affect inventory volatility.
5. Spread and inventory management are structurally interconnected.

**Crisis Scenario Response -**
1. If long inventory and price accelerates downward:
   - Widen spreads.
   - Skew quotes downward.
   - Reduce bid size.
2. The objective shifts from profit maximization to risk control.
3. Survival takes priority over spread capture.

**Core Insight -**
1. Retail mindset focuses on realized profit.
2. Market maker mindset focuses on current exposure.
3. Inventory awareness must be continuous.
4. Controlled inventory determines long-term viability.

---
### Fair Value Estimation Mechanics

Fair value is the internal estimate of what the asset should trade at right now. It is the anchor of all quoting decisions. If fair value is inaccurate or slow to update, the market maker becomes exposed to adverse selection.

**Last Traded Price Is Not Fair Value -**
1. The last trade is only the most recent agreement between two parties.
2. It may represent small size or temporary imbalance.
3. It does not necessarily reflect current consensus value.
4. Fair value must be continuously estimated, not assumed from the last print.

**Mid Price -**
1. Mid price = (Best Bid + Best Ask) ÷ 2.
2. It assumes both sides of the book are equally informative.
3. It is the simplest baseline estimate of fair value.
4. Many beginner systems start with mid price.
5. It does not account for imbalance or short-term pressure.

**Microprice (Order Book Weighted Fair Value) -**
1. Microprice adjusts fair value based on order book imbalance.
2. If bid size is significantly larger than ask size:
   - Fair value shifts above the mid.
3. If ask size is significantly larger than bid size:
   - Fair value shifts below the mid.
4. It captures short-term pressure before price moves.
5. It reflects probabilistic drift rather than certainty.

**Cross-Exchange Fair Value -**
1. In crypto, price discovery may occur on different venues.
2. If one exchange moves first, others become temporarily stale.
3. Professional market makers monitor multiple venues simultaneously.
4. Fair value may be derived from:
   - Fastest exchange.
   - Weighted average of exchanges.
5. This reduces arbitrage-based adverse selection.

**Momentum & Trade Flow Adjustment -**
1. Repeated aggressive buys suggest upward short-term pressure.
2. Repeated aggressive sells suggest downward short-term pressure.
3. Fair value shifts in the direction of dominant trade flow.
4. Flow imbalance can signal predictive short-term drift.
5. Fair value models often incorporate recent trade intensity.

**Derivatives & Funding Adjustment -**
1. In perpetual futures, price deviates from spot due to funding.
2. Fair value must incorporate:
   - Basis between spot and futures.
   - Funding expectations.
3. Ignoring basis leads to systematic mispricing.
4. Cross-asset relationships influence true fair value.

**Dynamic Updating -**
1. Fair value must update continuously.
2. Static estimates create stale quotes.
3. Slow updates increase adverse selection risk.
4. High-frequency environments require millisecond-level recalculation.
5. Accurate and adaptive fair value estimation determines survivability.

**Core Insight -**
1. Spread is placed around fair value.
2. If fair value is wrong, spread cannot protect you.
3. Persistent one-sided fills often signal misestimated fair value.
4. Fair value accuracy is the foundation of professional market making.

---
### Expected Value Per Fill Framework

Market makers evaluate profitability on a per-fill basis, not per round trip. Round-trip spread capture is not guaranteed because fills are random and flow may be imbalanced.

**Spread Is Earned in Two Legs -**
1. Total spread = Ask − Bid.
2. Half-spread = Spread ÷ 2.
3. When selling at the ask, only half-spread is earned initially.
4. The second half of spread is earned only if the opposite side fills later.
5. Round-trip completion is not guaranteed.

**Per-Fill Expected Value -**
1. Expected Profit per fill = Half-spread − Expected adverse move.
2. Half-spread represents immediate compensation.
3. Expected adverse move represents average post-fill price movement against the position.
4. If expected adverse move exceeds half-spread, expected value becomes negative.
5. Spread alone does not determine profitability.

**Why Round-Trip Spread Cannot Be Assumed -**
1. After a fill, price may move away permanently.
2. The opposite quote may never execute.
3. Inventory may need to be closed at worse prices.
4. Flow imbalance often results in one-sided fills.
5. Therefore, full spread capture is conditional, not guaranteed.

**Adverse Selection Example -**
1. Sell at 100.10.
2. Half-spread earned = 0.10.
3. Fair value jumps to 100.25.
4. Adverse move = 0.15.
5. Net expected value = 0.10 − 0.15 = −0.05.
6. Even though total spread was 0.20, only half was earned at fill time.

**Core Insight -**
1. Market makers optimize expected value per fill, not per idealized round trip.
2. Positive EV requires:
   - Half-spread > Expected adverse move.
3. Persistent negative per-fill EV leads to slow capital erosion.
4. Professional spread setting is based on expected post-fill risk, not theoretical full spread.

---
### Estimating Expected Adverse Move

Expected adverse move is the average price movement against a market maker after a fill. It represents the structural cost of providing liquidity and must be estimated accurately for spread optimization.

**What Is Expected Adverse Move -**
1. It is the average post-fill price movement against the position.
2. It is conditional on being filled.
3. It differs for buy fills and sell fills.
4. It reflects information disadvantage and repricing lag.
5. Spread must exceed expected adverse move for positive expected value.

**Empirical Estimation Method -**
1. Record each fill event.
2. Record price at fixed intervals after fill (e.g., 10ms, 50ms, 100ms, 1s).
3. Compute average movement against the fill direction.
4. Estimate conditional expectation of adverse drift.
5. Update this estimate continuously over time.

**Volatility Proxy Approximation -**
1. Short-term volatility can serve as a rough proxy.
2. Higher volatility generally increases expected adverse movement.
3. Volatility alone does not measure informed toxicity.
4. Noise volatility and informational volatility must be distinguished.
5. Pure volatility-based models are incomplete but usable.

**Order Flow Imbalance Conditioning -**
1. Expected adverse move increases when aggressive flow is imbalanced.
2. Repeated aggressive buys increase adverse cost after selling.
3. Repeated aggressive sells increase adverse cost after buying.
4. Flow-conditioned models outperform static volatility models.
5. Expected adverse move is state-dependent, not constant.

**Latency Impact -**
1. Adverse selection has two components:
   - Information disadvantage.
   - Latency disadvantage.
2. Faster quote updates reduce repricing lag.
3. Reduced lag lowers average adverse movement per fill.
4. Latency does not eliminate informed flow, but reduces exposure to stale pricing.
5. Superior latency improves risk-adjusted profitability.

**Competition Dynamics -**
1. If latency becomes equal across participants:
   - Spreads compress.
   - Latency edge disappears.
2. Edge shifts toward:
   - Better fair value modeling.
   - Better flow prediction.
   - Superior inventory management.
3. Tighter spreads increase fill frequency.
4. Higher fill frequency increases inventory turnover.
5. Profit margins per trade shrink in highly competitive markets.

**Core Insight -**
1. Expected adverse move is the key driver of spread design.
2. It must be estimated empirically and dynamically.
3. Latency reduces repricing risk but does not remove informational disadvantage.
4. Spread optimization requires understanding conditional post-fill behavior.
5. Professional market making is fundamentally risk-adjusted pricing of adverse selection.

---
### Inventory-Optimal Quoting (Avellaneda–Stoikov Intuition)

Inventory-optimal quoting formalizes how market makers adjust quotes dynamically based on inventory, volatility, and risk tolerance. The objective is to maximize expected spread capture while penalizing inventory risk.

**Core Optimization Objective -**
1. Market makers aim to maximize:
   - Expected spread profit − Inventory risk penalty.
2. Spread generates income.
3. Inventory introduces directional variance.
4. Optimal quoting balances income generation with risk control.
5. Ignoring inventory leads to compounding exposure risk.

**Risk Aversion Parameter (γ) -**
1. γ represents sensitivity to inventory risk.
2. Higher γ:
   - Wider spreads.
   - Stronger quote skew.
   - Lower inventory tolerance.
3. Lower γ:
   - Tighter spreads.
   - Mild skew adjustments.
   - Higher tolerance for inventory swings.
4. γ reflects capital structure, drawdown constraints, and risk mandate.
5. Risk aversion determines how aggressively exposure is controlled.

**Reservation Price -**
1. Reservation price is the inventory-adjusted fair value.
2. It shifts away from raw fair value depending on inventory.
3. If long inventory:
   - Reservation price shifts downward.
4. If short inventory:
   - Reservation price shifts upward.
5. Quotes are placed around reservation price instead of raw fair value.
6. This automatically embeds inventory control into pricing.

**Optimal Spread Determinants -**
1. Spread increases with:
   - Volatility.
   - Risk aversion (γ).
   - Inventory magnitude.
   - Shorter remaining time horizon.
2. Higher volatility requires greater risk compensation.
3. Larger inventory increases risk exposure.
4. Short time horizons require faster inventory neutralization.
5. Spread is dynamic and state-dependent.

**Time Horizon Effect -**
1. As trading horizon shortens, inventory becomes more dangerous.
2. Stronger skew is required near session end.
3. Inventory liquidation pressure increases over time.
4. Risk penalty grows as time to neutralization decreases.
5. Time awareness is embedded in optimal control models.

**Core Insight -**
1. Inventory should influence quote center dynamically.
2. Spread and skew are not independent decisions.
3. Risk aversion directly shapes quoting behavior.
4. Professional market making embeds inventory into pricing mathematically.
5. Avellaneda–Stoikov provides a foundational framework for dynamic optimal quoting.


---
### Multi-Asset & Cross-Venue Inventory Control

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
### Market Making Engine Architecture

A professional market making system is a coordinated set of modules that operate continuously. It is not simply placing bid and ask orders. The engine integrates market data, fair value estimation, inventory control, execution management, and risk safeguards.

**High-Level System Layers -**
1. Market Data Layer.
2. Fair Value Engine.
3. Risk & Inventory Engine.
4. Quote Engine.
5. Execution & Order Manager.
6. Safety & Kill-Switch Layer.
7. Continuous feedback loop.

**Market Data Layer -**
1. Consumes order book updates, trades, funding data, and cross-venue prices.
2. Requires low latency and accurate timestamping.
3. Must process data without packet loss.
4. Stale data leads to stale quotes.
5. Input speed is more critical than model complexity.

**Fair Value Engine -**
1. Computes real-time fair value estimate.
2. May include:
   - Mid price.
   - Microprice.
   - Cross-venue weighting.
   - Momentum adjustment.
   - Basis and funding adjustment.
3. Updates continuously per tick.
4. Incorrect or slow fair value causes adverse selection.

**Risk & Inventory Engine -**
1. Monitors net exposure across venues.
2. Applies risk aversion parameter (γ).
3. Computes reservation price shift.
4. Adjusts spread dynamically.
5. Triggers hedge thresholds.
6. Controls inventory drift.

**Quote Engine -**
1. Calculates:
   - Bid = Reservation price − Half-spread.
   - Ask = Reservation price + Half-spread.
2. Applies skew based on inventory.
3. Adjusts size per risk limits.
4. Handles venue-specific adjustments.
5. Ensures quotes remain competitive yet risk-adjusted.

**Execution & Order Manager -**
1. Places and cancels orders.
2. Tracks fills and partial fills.
3. Measures placement and cancel latency.
4. Handles exchange errors and rejections.
5. Detects desynchronization.
6. Cancel speed is critical for minimizing stale quote risk.

**Cancel Latency Risk -**
1. If cancel speed is slow, stale quotes remain exposed.
2. Price may move before cancellation completes.
3. Stale fills create adverse selection.
4. Increased adverse selection raises expected loss per fill.
5. Higher cancel latency requires wider spreads.

**Infrastructure Principle -**
1. Quote aggressiveness must match infrastructure quality.
2. Faster data and cancel speed allow tighter spreads.
3. Slower systems must charge higher risk premium.
4. Infrastructure advantage directly improves expected value.
5. Competitive survival depends on execution efficiency.

**Safety & Kill-Switch Layer -**
1. Enforces maximum inventory limits.
2. Enforces maximum loss limits.
3. Detects volatility spikes.
4. Detects exchange disconnections.
5. Stops quoting when risk becomes unpriceable.

**Core Insight -**
1. Market making is a systems engineering problem.
2. Data speed, cancel speed, and pricing logic are interconnected.
3. Latency disadvantages increase adverse selection.
4. Spread must reflect infrastructure capability.
5. Engine design determines survivability in competitive markets.