# Market Making as a Service — Learning Roadmap

Goal: understand end to end how a market maker serves token projects on a retainer
(and the alternative models), so Kosashi Capital can find, qualify, pitch, price,
negotiate, onboard and run retainer clients.

Started 2026-11-23. Same contract as the Lifetime Roadmap:
`learning-template/topic-template.md` (5-step sequence, terminology check first,
non-quant accessibility, never self-advance). Taught content goes into the
`## Market Making as a Service (Token Projects)` section of `market-making.md`,
one `### MMaaS Layer N` per layer.

Step 4 (KCMME check) for this course = "can Kosashi / the engine deliver this
today, and what is missing?" Gaps go to the KCMME gap register as usual.

Mark `[x]` when a layer is done.

## Venue Naming Convention (use in EVERY layer — PO 2026-11-23)

Never say bare "DEX". Always one of these three:
- **CEX** — centralised exchange (Binance, HTX, MEXC). Exchange holds funds, order book, database settlement.
- **Order-book DEX** — on-chain order book (Hyperliquid, dYdX). Own wallet, bids/asks/mid, we quote exactly as on a CEX.
- **Pool DEX** — AMM, no order book (Uniswap, PancakeSwap, Raydium, Orca, Meteora; reached via routers like Jupiter / the swap screen in Phantom). Price = ratio of the two sides in the pool; MM role = provide liquidity + arbitrage vs other venues.

## Running Example (use in EVERY layer — PO 2026-11-23)

One fictional project, followed through its whole lifecycle, so every layer uses the
same numbers. Extend it as layers need (never change existing facts).

**Kestrel Network (KSTL)**, fictional.
- Product: blockchain file-storage service; users pay storage fees in KSTL; stakers earn a share of fees; holders vote.
- Treasury: 200M KSTL held by the project (separate from the inventory loan), sold slowly / OTC to fund operations.
- Total supply 1,000,000,000 KSTL. Day-one circulating 100M (10%).
- Seed round $0.02, private round $0.05, public sale $0.08 (raised $2M).
- TGE 1 March. Deposits open on the exchange 1 March; trading opens 3 March 10:00.
- DEX: project seeds a Uniswap pool with 1M KSTL + $100k USDC → implied price $0.10.
- CEX: mid-tier exchange lists KSTL/USDT; listing agreement requires a market maker.
- Kosashi hired on retainer; Kestrel lends 2M KSTL + $200k USDT into the account we run.
- Opening quotes: bids $0.098 / asks $0.102 around reference price $0.10.

**Heron (HRN)**, fictional comparison client (Layer 2+): same size as Kestrel but on the **loan + call option** model: lends 2M HRN at $0.12, call option on those 2M at strike $0.15, 12-month tenor, no fee. Kestrel = retainer at $10k/month (illustrative). Assume $1k/month trading profit for both when comparing.

---

## Layer 0 — New Token Listing Mechanics (technical foundation) ✅ Done 2026-11-23

**Why first**: everything we have done so far quotes around a mid price that
already exists. A new token has no market yet. Before any commercial talk we must
know who creates the first order book, where the first price comes from, and how
quoting starts.

- [x] How a project gets listed on a CEX (application, due diligence, listing fee, MM requirement, deposit window, trading-open time)
- [x] Who seeds the order book: exchange vs market maker vs the crowd
- [x] Opening mechanisms: empty book (first orders set price) vs call auction / pre-opening period
- [x] Where the reference (initial) price comes from: private/public sale price, FDV comparables, DEX pool price, pre-market / pre-launch perps, OTC
- [x] DEX launch: how seeding a liquidity pool fixes the starting price
- [x] Price discovery in the first minutes/hours: quoting wide around a reference, letting flow move fair value, no external price leader
- [x] Inventory needed to open: tokens (from the project) + stablecoins
- [x] Already-listed tokens (most retainer clients): how onboarding differs
- [x] Core question: **with no Binance-style price leader, what is our fair value on day one?**

## Layer 1 — Why Projects Pay for Market Making ✅ Done 2026-11-23
- [x] Exchange listing and continued-listing requirements (spread, depth, uptime)
- [x] What thin markets cost a project (slippage, price gaps, lost investor trust, delisting risk)
- [x] KPIs: spread, depth at ±2%, uptime, volume; how exchanges and projects measure them

## Layer 2 — Commercial Models ✅ Done 2026-11-24
- [x] Retainer (fixed monthly fee + KPI SLA, client lends inventory)
- [x] Loan + call option model, and its conflict of interest
- [x] Hybrids, performance fees, profit share
- [x] Which model fits a new firm, and why

## Layer 3 — Anatomy of a Deal (Term Sheet)
- [ ] Inventory loan size, tenor, return terms
- [ ] KPIs per venue, reporting cadence, SLA breach consequences
- [ ] Account ownership (client sub-accounts + API keys vs MM accounts), custody
- [ ] Fees, termination, clawbacks, exclusivity, PnL ownership

## Layer 4 — Operations of a Client Book
- [ ] Spot, single-asset, thin books vs our perps-on-majors setup
- [ ] Inventory management when the client owns the inventory
- [ ] KPI monitoring and client reporting
- [ ] Venue coverage (where tokens actually list)

## Layer 5 — Legal, Compliance and Ethics
- [ ] Legitimate market making vs wash trading / manipulation
- [ ] Enforcement cases against token market makers
- [ ] Client screening, contract jurisdiction, red flags

## Layer 6 — Pricing and Unit Economics
- [ ] Cost to serve one client; capital at risk
- [ ] Pricing tiers; who keeps trading PnL
- [ ] What a retainer book is worth to Kosashi

## Layer 7 — Market and Pipeline
- [ ] Buyer types (pre-TGE, newly listed, unhappy with current MM)
- [ ] Lead sources (exchange listing teams, launchpads, VCs, visibly thin books)
- [ ] Competitors; qualification questions; outreach

## Layer 8 — Sales Conversation and Negotiation
- [ ] Discovery call structure; proposal; objection handling
- [ ] Mock calls: price-sensitive founder, demanding founder, red-flag founder (asks for wash trading)
