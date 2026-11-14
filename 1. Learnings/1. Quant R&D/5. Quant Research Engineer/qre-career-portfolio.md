# Career Portfolio — Proof of Skill

One entry per completed level: what was found or judged on KCMME that proves the skill to
an employer. Written at Step 6 of each level. Source material for Build Track B6
(interviews, resume, STAR stories).

Entry format:

### Level N — <skill>
- **What I did** (judged / found on KCMME):
- **Result** (number, finding, artifact link):
- **What it proves** (which judgment skill):
- **Interview story** (STAR, 4 lines: situation · task · action · result):

---

### Level 0 — Research → production loop: auditing a shipped feature
- **What I did** (hands-on, on KCMME): audited M8 (Decision Layer LIVE), a closed feature of
  my own market-making engine, against the professional desk loop — hypothesis with a
  number, kill criteria, independent review, true A/B — reading the contract and A/B report
  myself; then cross-checked the whole AI delivery workflow against the same loop.
- **Result**: M8's predictions were direction-only ("> 0", "drops"); no economic kill
  criteria; the independent model (Codex) reviewed proof mechanics, not the research idea;
  the "A/B" was two back-to-back 25-min windows (40 vs 52 lots), and the new behaviour's
  own ledger showed ~2.75× higher per-lot exit cost (0.33¢ vs 0.12¢) yet shipped default-ON.
  Filed 8 delivery-workflow gaps (WG0.1–WG0.8, KCMME `docs/architecture/gaps/delivery-workflow-gaps.md`,
  fugu-dev `6adfb9c2f`) incl. a mandatory research-note template and a target end-to-end
  delivery flow, routed to a workflow change.
- **What it proves**: Junior bar on the loop (Mid on spotting missing judgment stages); can
  read a shipped feature's record and say what was and wasn't proven.
- **Interview story** (STAR):
  S — I ran an AI-assisted delivery workflow for my own MM engine and couldn't tell if shipped features were economically right.
  T — Audit a shipped feature against how professional desks take ideas to production.
  A — Mapped M8 onto the research → review → reproduction → A/B → scale-or-kill loop; found direction-only predictions, no kill rule, sequential A/B.
  R — Showed a 2.75× cost result had been caveated instead of judged; filed 8 process gaps incl. a mandatory research note with predicted effect + kill criteria.

### Level 1 — P&L attribution: rebuilding and reconciling a live session
- **What I did** (hands-on, on KCMME): rebuilt the per-fill P&L waterfall (spread capture,
  5 s adverse selection, fees) for a real 16-minute SOLUSDC mainnet session (73 engine fills)
  in a spreadsheet; split maker vs taker; compared my numbers with the engine's own
  attribution; reconciled both against the Binance trade export.
- **Result**: engine-log view −$0.017 (makers +$0.288, takers −$0.304 — one taker fill wiped
  ~4 maker fills); found the engine measures adverse selection from the fill price, so its
  spread bar reads ≈ 0 and the spread is misreported as adverse selection (would have steered
  toward "widen quotes" instead of "cut taker exits"); found the fill log missed 39 of 112
  exchange trades (36 takers) — the real net was −$0.688, ~40× worse. Filed engine gaps
  QRE-L1-G1/G2 and delivery gaps WG1.1–WG1.3 (KCMME fugu-dev `47e0d181c`).
- **What it proves**: Junior bar on attribution mechanics; Mid-level instinct on
  reconciliation and catching a definition bug by independent recomputation.
- **Interview story** (STAR):
  S — My engine reported a near-break-even session.
  T — Verify where the money really went.
  A — Rebuilt the waterfall by hand from raw fills, compared bar-by-bar with the engine, reconciled to the exchange export.
  R — Found a labelling bug (spread counted as adverse selection) and a log missing 36 taker exits; true loss 40× the engine's figure; root cause = taker exits, not quote width.

### Level 2 — Signal vs noise: judging results and tests on a live MM business
- **What I did** (judged / found on KCMME): judged real HTX cost-down results with the
  CI-vs-bar verdict rule (first live HTX test: −0.183 [−0.279, −0.116] vs a −0.10 stop bar →
  FAIL; ETH basket inclusion −0.101 that becomes −0.124 without one day → CONTINUE); found all
  six flaws in an AI-proposed queue-position A/B (coin split, two changes, sequential hours,
  fill-count n, bar set after the result, no guardrail) and rewrote it as a pre-registered
  switchback test; showed the lean's +0.053 per $1k cost win must be judged as money per hour
  because it keeps ~1/3 of volume and our cost straddles the rebate break-even.
- **Result**: engine finding — the spine's 20-fill adverse meter wobbles ±1.5 ticks
  (autocorrelation 0.38 → ~9 effective fills), the 5 worst of 109 fills carry 26 % of it, it
  predicts the next fill at only 0.13, and under best-price entry its output never moves the
  quote. Filed engine gaps QRE-L2-G1/G2 and delivery gaps WG2.1–WG2.2 (verdict statistical
  standard, A/B design checklist; KCMME fugu-dev `165f7d89c`).
- **What it proves**: Junior bar on statistical judgment (SE, CIs, units, verdicts); Mid-level
  on experiment design (switchback, randomisation, guardrails) and catching an
  implementation-theater signal.
- **Interview story** (STAR):
  S — My startup's cost-down claims rested on short before/after runs and AI-written reports.
  T — Decide which results were real and which tests could decide anything.
  A — Re-read results by block-level CIs against pre-written bars; redesigned an A/B as a randomised switchback; measured the engine's own toxicity meter's noise and predictive power.
  R — Separated decided results from CONTINUEs, blocked a size step on a 2-day result, found a meter with no decision effect, filed two process gaps.

