# Session Handover — Market Making Learning Program

**Session name**: local-learning-session-gpnl-profitability
**Handover date**: 2026-07-10
**Context**: this file is the entry point for the next Claude session.
Read it fully before responding to the user.

---

## 1. What This Program Is

A structured institutional market making learning program running in parallel with
active KCMME engine development. Two goals run simultaneously every layer:

**Goal 1 — Learn**: teach MM concepts at Jane Street / Citadel depth.
**Goal 2 — Audit**: check KCMME engine against each concept and file confirmed gaps.

These two goals have a strict dependency: audit only happens AFTER understanding is
confirmed. This rule was violated once mid-program and caught by the user.

---

## 2. Two Roadmaps in Play

### Lifetime Roadmap (user-provided, Levels 0–20)
The full institutional MM curriculum. Levels in order:
0 Mental Model | 1 Market Structure | 2 Limit Order Book | 3 Maker Economics |
4 Fair Value | 5 Spread Design | 6 Adverse Selection | 7 Inventory |
8 Queue/Fill Probability | 9 Latency/Staleness | 10 Execution Engineering |
11 Post-Fill Management | 12 Asset Selection | 13 Simulation |
14 Statistical Validation | 15 Adaptive Control | 16 Cross-Venue/Cross-Asset |
17 Risk Management | 18 Operations | 19 Business Economics | 20 Institutional Reality

### KCMME Profitability Roadmap (Layers 0–13, ALL COMPLETE)
A KCMME-specific focused deep-dive — why the engine is GPNL-negative.
File: `~/Desktop/trading/1. Learnings/5. Market Making/learning-roadmap/profitability-roadmap.md`
Status: all 15 layers (0 through 13) marked ✅ Done as of 2026-07-09.

The KCMME roadmap is a subset of the Lifetime Roadmap — it covered Levels 4–13 in
depth against KCMME specifically. Levels 0–3 were assumed as background.

**What's next (UPDATED 2026-07-10)**: PO decided to restart the Lifetime Roadmap
from Level 0 and clear every level end-to-end, inside out, before advancing —
Levels 0–3 were never formally taught, and the KCMME coverage of 4–13 was
KCMME-angled, not canonical depth. Do NOT skip to Level 14. Next up:
**Level 0 — Mental Model, Step 1 terminology check.**

market-making.md was restructured for this (commit in the trading repo,
2026-07-10): `## Foundation` = light junior onboarding read; `## Intermediate to
Advance — Lifetime Depth (Levels 0–20)` = one section per level in chronological
order, the senior end-to-end read (heavy Foundation content moved here as
*(Interim)* entries under their home levels; standalone term entries grouped at
the end pending fold into home levels); `## Market making Profitability` = the
KCMME Layers 0–13 applied record, kept intact. Each level taught writes its
full-depth content into its `### Level N` section, replacing interim/pending
markers.

---

## 3. The Non-Negotiable Teaching Format

**Read `learning-template/topic-template.md` in full before starting any layer.**
That file is the contract. The sequencing rule is the most critical:

```
Step 1 — Terminology check     ← list all terms, explain each, wait for "clear"
Step 2 — Teaching              ← full layer content, interactive
Step 3 — Understanding check   ← explicit "is this clear?" — MUST confirm before Step 4
Step 4 — KCMME check           ← read actual source files, report inline
Step 5 — Doc update            ← write to market-making.md + engine-gaps.md + commit/push
```

**Steps 4 and 5 are FORBIDDEN before Step 3 confirmation.**
This was violated once (Layers 12 and 13 in a prior session — jumped to doc-writing
without teaching). User caught it. Do not repeat.

**Other HARD rules from the template:**
- Never self-advance. Wait for explicit user confirmation before moving to next layer.
- Terminology check is mandatory even for terms the user likely knows.
- Re-anchor prior-layer terms in every new layer with a concrete number — never just
  reference them by name and move on. p_tox, TailScore, VPIN, OFI, markout should
  feel like tools the user owns, not terms they remember hearing.
- Every defensive concept gets an offensive flip → `docs/architecture/alpha-strategies.md`.
  Layers 10–13 are missing their flip entries (gap to fill as you cover those levels
  in the Lifetime Roadmap or revisit them).

---

## 4. File Locations

| Purpose | File |
|---|---|
| Teaching content (all layers taught so far) | `~/Desktop/trading/1. Learnings/5. Market Making/market-making.md` |
| KCMME profitability roadmap + status | `~/Desktop/trading/1. Learnings/5. Market Making/learning-roadmap/profitability-roadmap.md` |
| Learning format rules | `~/Desktop/trading/1. Learnings/5. Market Making/learning-template/topic-template.md` |
| Engine gap register (single source of truth) | `KCMME repo: docs/architecture/gaps/engine-gaps.md` |
| Alpha strategies (offensive flips) | `KCMME repo: docs/architecture/alpha-strategies.md` |
| This handover file | `~/Desktop/trading/1. Learnings/5. Market Making/SESSION_HANDOVER.md` |

KCMME repo working branch: **`fugu-dev`** (all gap docs committed here, not `claude-dev`).
Last commit: `3953c67e6` — Layer 13 KCMME check body section.

---

## 5. High-Priority Open Gaps (engine-gaps.md)

These are the confirmed High-priority gaps from the KCMME profitability roadmap.
They inform where engine work should go next.

| Gap | Layer | Priority |
|---|---|---|
| No maker-first timer — Mode A/B dispatch IOC directly, skip maker-race phase | L11 | High |
| No λ_exit_side tracker per (asset, venue) — foundational for t* computation | L11 | High |
| No per-session attribution waterfall report script | L12 | High |
| No fill-type A/B/C classification | L12 | High |
| Walk-forward gate absent for strategy TOML params | L13 | High |
| No defer budget in chooser — DEFER_TO_MIRROR loops unbounded (M6: 2,407/2,463 defers) | M6 | High |
| Maker-P hardcoded 0 in chooser — every cost comparison wrong | M6 | High |
| G9/G10: per-quote-attempt BBO-distance not instrumented | M6 | High |

Full gap register with body sections: `docs/architecture/gaps/engine-gaps.md`.

---

## 6. What Was Learned (Layers Summary)

### KCMME Profitability Layers (all complete)
- **L0**: Fair value quality — raw mid vs microprice. VPIN weights low. Gap: no microprice.
- **L0.5**: Potemkin check — what proves fills are real, not fabricated.
- **L1**: Fill markout analysis — 100ms/500ms/1s/5s horizons, adverse selection vs carry.
- **L2**: Adverse selection / TailScore — VPIN, OFI, TailScore, CVaR.
- **L3**: Latency / stale quote — cancel RTT, stale fill probability, quote age.
- **L4**: Spread vs adverse move — half-spread, A-S formula, spread floor.
- **L4.5**: Queue / fill quality — queue position, BBO joining, sweep fills.
- **L5**: Inventory carry (single venue) — A-S reservation price, d*, skew.
- **L5.5**: Cross-venue delta neutrality — net delta per symbol, hedge band, axis-7.
- **L6**: Funding rate — perpetual basis, funding arbitrage, pre-funding urgency.
- **L7**: Cancel/replace churn — OTR, dead-band, queue destruction.
- **L8**: Asset-wise profitability — capital efficiency, scorecard, reallocation.
- **L9**: Per-asset calibration — online k_tox, EWMA anchor, walk-forward for classifier.
- **L10**: Market regime classification — HMM, σ/VPIN/OFI regime axes, adapt-not-freeze.
- **L11**: Post-fill monetization — 4 exit paths, IOC truth, maker-first timer t*, Mode A/B.
- **L12**: GPNL attribution decomposition — waterfall formula, fill-type A/B/C, M6 confirmation.
- **L13**: Validation discipline — ladder Sim→Testnet→Mainnet, fidelity gate, DSR, validate-freeze.

---

## 7. Immediate Next Steps

**Option A (continue learning)**: proceed to Lifetime Roadmap Level 14 — Statistical
Validation. Apply the same 5-step teaching format. This level was partially covered
in KCMME Layer 13 (DSR, MinTRL) but the Lifetime Roadmap version goes deeper:
distributions, calibration curves, reliability buckets, online learning drift.

**Option B (capstone)**: the profitability roadmap ends with a "One Fill End-to-End
Skill" exercise (at the bottom of profitability-roadmap.md). Take a real fill from a
recent KCMME session and decompose it completely using all 14 layers learned.

**Option C (engine work)**: the gap register is dense enough to drive a full engineering
campaign. L11-GAP-1 (maker-first timer) + L12-GAP-1 (waterfall report) + M6 defer-budget
are the highest-impact and most buildable gaps.

**Flip entries missing (low-effort cleanup)**: alpha-strategies.md ends at Layer 9.
Layers 10–13 each have defensive concepts without offensive flips filed. Add these
as part of the next session warmup if the user wants.

---

## 8. User Learning Style (from memory)

- Learns through repetition across contexts — terms need to appear in multiple layers
  with new concrete examples each time to truly stick.
- Wants 100% autonomous iteration within a bounded task — never ask for confirmation
  between steps within a layer, only at layer boundaries.
- Corrects format violations immediately and directly. When corrected, acknowledge
  once and execute correctly — do not over-explain.
- Prefers concise responses. No trailing summaries unless they add something.

---

## 9. Session Recovery Checklist (read at session start)

Before doing anything else:
- [ ] Read this file in full
- [ ] Read `learning-template/topic-template.md` in full
- [ ] Check `profitability-roadmap.md` progress table (should show all ✅)
- [ ] Confirm with user which option to pursue (A / B / C above)
- [ ] If continuing learning: confirm the next Lifetime Roadmap level, then start
      Step 1 (terminology check) — do NOT pre-write content
