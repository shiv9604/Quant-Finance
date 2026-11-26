# Kosashi Capital: Market-Making Term Sheet (PRIVATE REFERENCE)

Internal only. Never send this file to a client. It holds every term, our default position, our walk-away
line, and what we may concede in negotiation. The client-facing version is `offering-sheet.md`.
Built in MMaaS Layer 3 (2026-11-25) on the Kestrel running example. Numbers are illustrative until Layer 6 (pricing).

| # | Term | Our default (template) | We may concede | Red line / never |
|---|---|---|---|---|
| 1 | Parties | Kosashi Capital (market maker) and client | — | — |
| 2 | Service | Continuous two-sided quoting, spot | Add venues for a higher fee | — |
| 3 | Venues | Named exchanges and pairs | More venues for a higher fee | Venues we can't connect to reliably |
| 4 | KPI schedule | Main venue: spread ≤ 1%, ±2% depth agreed per venue, uptime ≥ 95%. Smaller venue: spread ≤ 1.5%, uptime ≥ 95%. Snapshot every 10 s, monthly %. | Tighter targets only for a higher fee and once proven | Targets we can't measure or prove |
| 5 | Exclusions | Exchange outages or maintenance, exchange freezes, client inventory shortfalls, force majeure | — | Removing exclusions |
| 6 | Account and inventory | Client-owned sub-account; client deposits tokens + USDT before the start; trade-only API key, withdrawals off, IP-locked | — | Withdraw permission on our key (custody risk) |
| 7 | Inventory changes | Client gives 48 h notice before adding or removing inventory; unannounced withdrawal = client's responsibility | Shorter notice (24 h) | No notice at all |
| 7b | Inventory band & top-ups | We notify the client when inventory leaves the agreed band (e.g. tokens outside 45–65% of value); client tops up within 24–48 h. If not, KPI misses on the empty side = client-inventory exclusion. | Longer top-up window | We sell the client's tokens without approval |
| 7c | Event notice | Client gives advance notice of planned events that move flow: token unlocks, listings, launches, major announcements, treasury sales. We use it only to prepare liquidity (top-ups, depth), never to trade for our own benefit. | — | Trading on the client's non-public info (insider risk) |
| 7d | Treasury sales | Client never sells its own tokens into our quotes on venues where we make markets for them (shows as self-trade / wash trading to the exchange). Treasury cash-outs go via OTC, or by withdrawing stablecoin from the sub-account with 48 h notice. | Small sales with advance notice, coordinated with us | Client routinely trading against its own MM book |
| 8 | Fee | Monthly retainer in USDT, paid before each month starts, no refunds | Paid pilot or split first month only if the deal needs it | Work before payment |
| 9 | Performance | NOT in the template. No penalty offered upfront. | If asked: a penalty only alongside a matching uptime bonus (symmetric) | One-sided penalties; anything tied to price |
| 10 | Trading PnL | Belongs to the client (its account); our income = pure retainer | — | — (open item: trading-loss guardrail, Layer 4) |
| 11 | Term | 6–12 months; minimum 6 months; then rolling monthly with 30 days' notice | 12-month term at a better monthly rate | Under 6 months (except a paid pilot) |
| 12 | Termination for cause | Template: Kosashi may exit for non-payment (5 days after due date), any illegal request, or delisting. Client's KPI-based exit NOT written upfront. | Non-payment grace 7–10 days (free concession). If the client insists on a KPI exit: a full quarter of misses, not 1–2 months. | Exit for price falls |
| 13 | Exit procedure | Cancel all orders, client revokes key, final report within 7 days, settle | — | — |
| 14 | Reporting | Weekly + monthly reports (continuous internal measurement) | Live dashboard / daily summary later, or as a paid extra | — |
| 15 | Clawback | Only for proven reporting errors or misconduct, within 60 days (matters only once bonuses exist) | — | Clawback linked to price |
| 16 | Exclusivity | Sole market maker on the venues we serve; NO competitor restrictions | Narrow, named rivals, contract term only, at a premium | Broad or permanent sector bans |
| 17 | Conduct | Organic trading only; no wash trading; self-trade prevention on; no volume boosting; no price targets | — | Any request to fake volume or move the price → walk away |
| 18 | Confidentiality | Mutual | — | — |
| 19 | Law and disputes | To decide with a lawyer (Layer 5) | — | — |

Pricing principle (Layer 2, to finalise in Layer 6): cash floor (e.g. $7k/month) covers cost-to-serve plus margin; above it, the client may swap
part of the fee for call options, valued at $0 in our planning.
