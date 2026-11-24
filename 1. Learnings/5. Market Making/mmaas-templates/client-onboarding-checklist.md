# Kosashi Capital: Client Onboarding Checklist (retainer market making)

Run this for every new retainer client, in order. Nothing goes live until every box is ticked.
Built in MMaaS Layer 4 (2026-11-25) on the Kestrel example. Copy this file per client: `client-onboarding-<token>.md`.

Client: ________  Token: ________  Venues: ________  Go-live date: ________  Owner: ________

## 0. Pre-conditions (business side)
- [ ] Term sheet agreed and contract signed (see `term-sheet-private-reference.md`)
- [ ] Client screening done: investors, treasury (public wallets), team and product alive, no red flags (fake volume / price targets)
- [ ] KPI schedule per venue written in the contract (spread, ±2% depth each side, uptime, measurement method, exclusions)
- [ ] **First month's fee received** (paid in advance, USDT)

## 1. Infrastructure gate (must already be true for any client)
- [ ] High-availability setup live: auto-restart, hot standby with automatic failover, single-quoter lock
- [ ] Exchange reconnect + order reconciliation tested
- [ ] Failover drill passed

## 2. Venue coverage
- [ ] Spot connection built for each venue the client is listed on
- [ ] Tested with a small amount first (place, cancel, fill, rate limits, minimum sizes, fees)
- [ ] Venue fee / rebate tier known; ask about the exchange's market-maker programme

## 3. Account and inventory
- [ ] Client created a dedicated sub-account per venue
- [ ] API key: **trade only**, withdrawals **disabled**, **IP-locked** to our servers
- [ ] Inventory **verified by us** on each venue (tokens + USDT, amounts match the contract)
- [ ] Starting inventory snapshot saved (for the trading-result baseline and settlement)

## 4. Engine: client-book mode
- [ ] **No flattening, ever** (kill / shutdown / exit = cancel orders only, inventory untouched)
- [ ] **Self-trade prevention ON** on every order
- [ ] Organic trading only (no volume targets, no price targets)
- [ ] Separate config + process (or isolated account) for this client

## 5. Quoting setup
- [ ] Inventory band agreed (e.g. tokens 45–65% of value) + top-up rule (client tops up within 24–48 h)
- [ ] Quote ladder configured per venue to meet spread + depth within ±2%
- [ ] Skew (lean) settings within the spread target, for pacing drift

## 6. Risk and monitoring
- [ ] Trading-loss guardrail set (e.g. 1% warning, 2% pause and agree) — trading loss vs hold-the-starting-mix, not price loss
- [ ] Alerts ON: quotes present (≤ 1 min), spread, depth, inventory band, guardrail, connection / exchange status
- [ ] On-duty rota and phone paging working (test alert sent and received)
- [ ] KPI snapshots every 10 s being recorded; exclusions logged (exchange maintenance, client inventory shortfall)
- [ ] Client deposits / withdrawals detected and logged

## 7. Client information
- [ ] **Event calendar** collected: unlocks, launches, listings, big announcements, treasury sales
- [ ] Event-notice duty confirmed (client tells us in advance); non-public info used only to prepare liquidity
- [ ] Client contacts for top-ups and emergencies

## 8. Reporting
- [ ] Weekly report template ready
- [ ] Monthly report template ready (KPIs per venue, volume, inventory vs start, trading result, downtime with reasons)

## 9. Go live
- [ ] Go live; watch closely for the first 48 hours
- [ ] First weekly report sent
- [ ] Next month's invoice scheduled (due before the month starts)
