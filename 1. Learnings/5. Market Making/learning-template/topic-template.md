# Learning Topic Template

Use this structure for every topic in the learning program.
Two active roadmaps:
- **Lifetime Roadmap** (Levels 0–20, user-provided): the full institutional MM
  curriculum from market structure to operations. This is the long-term map.
- **KCMME Profitability Roadmap** (Layers 0–13, in `learning-roadmap/profitability-roadmap.md`):
  a focused KCMME-specific deep dive — why the engine is GPNL-negative and what fixes it.
  All 15 layers are COMPLETE as of 2026-07-09. UPDATE 2026-07-10: the Lifetime
  Roadmap restarted from Level 0 — every level gets cleared end-to-end in
  chronological order. Taught content goes into the `### Level N` section of
  `## Intermediate to Advance — Lifetime Depth (Levels 0–20)` in market-making.md.

Goal: understand each concept at professional-firm depth (Jane Street / Citadel level),
then map it to KCMME to find gaps and decide if they're real issues.

## Step Sequencing Rule (HARD — violation cost: re-teach the layer)

Every layer follows this exact order. No step can begin until the previous one is
explicitly confirmed complete.

```
Step 1 — Terminology check
         List all key terms. Explain each. Wait for "clear" per term.
         Do NOT proceed until user confirms every term is understood.

Step 2 — Teaching
         Teach the full layer using the Teaching Flow Rules below.
         Do NOT write anything to market-making.md yet.

Step 3 — Understanding confirmation
         Ask explicitly: "Is this clear, or does any part need more depth?"
         Do NOT proceed to KCMME check until user confirms understanding.

Step 4 — KCMME check
         Read the actual source files. Find what exists and what's missing.
         Report findings inline — do NOT write to engine-gaps.md yet.

Step 5 — Doc update
         Only now: write teaching content to market-making.md AND
         write confirmed gaps to docs/architecture/gaps/engine-gaps.md.
         Commit + push atomically to fugu-dev.
```

This sequence is not a preference — it is the contract. Steps 4 and 5 are
FORBIDDEN before Step 3 confirmation. The prior-session violation (jumping
directly to doc-writing without teaching) came from conflating these steps.

## Progression Rule (HARD)

After covering a topic, always come back to it and ask if there are any questions.
Only move to the next topic after the user explicitly confirms they have none.
Never self-advance to the next layer.

## Terminology Check Rule (HARD)

Before teaching a topic, identify every key concept or term that will appear in it.
Go through each one with the user — explain it simply, then confirm understanding before moving on.
Do not assume the user knows a term just because it was mentioned in a prior layer.
This applies to: signal names (VPIN, OFI, TailScore), model types (EWMA, distribution), structural concepts (regime, adverse markout, latency), and any acronym.
Format: explain the term → ask if it landed → only proceed when confirmed.
Goal: the user should never be reading through a topic while silently not understanding a foundational word.

## Non-Quant Accessibility Rule (HARD — added 2026-08-21, PO directive)

The learner is NOT from a quant/math/statistics background. Two obligations, everywhere
(terminology sections, teaching, KCMME checks, doc write-ups — no exception):

1. **Every symbol, every time.** Whenever a symbol or short variable name appears
   (q, γ, σ, δ, T, k, λ, α, m, r, …), attach its plain-language meaning in-line at
   EVERY appearance, not just the first — e.g. "q (how much inventory I currently
   hold)", "σ (how much the price typically moves per minute)". A bare symbol with no
   gloss is a violation even if it was defined two paragraphs earlier. The learner
   should never have to scroll back to decode a letter.

2. **Every math/stat/quant word gets a plain-words mini-explainer at first use in the
   section.** This covers terms like: quadratic, linear, variance, percentile,
   z-score, EWMA, sigmoid, regression, convex, argmax, distribution, correlation,
   half-life, "grows with the square", "cliff vs progressive", clamp, floor/cap.
   Format: the term, then one or two sentences of what it means using everyday
   objects/numbers, then the domain use. If a concept can't be explained without
   another math term, explain that one too — chain down to everyday language.

Test before sending any teaching block: read it as someone who stopped math at
school algebra. Every letter decoded? Every math word grounded? Then it ships.

Terms are not mastered after one explanation. Every time a prior-layer term appears
in a new layer, use it actively — do not just reference it by name and move on.

When a prior term reappears in a new context:
- Use it in the new context's formula or scenario with a concrete number
- Briefly re-anchor what it means in one clause: "p_tox — the probability the fill
  is from informed flow — now drives the spread through delta_adv"
- Never write "as we covered in Layer 2" and skip the re-use

The goal is that by Layer 8, terms like p_tox, TailScore, VPIN, adverse markout are
not things the user "learned once" — they are tools the user has picked up and put
down in five different contexts and can use without thinking.

## Teaching Flow Rules (HARD)

These rules define how every topic must be taught. Follow this exact flow every time.

1. **Start with why the naive approach fails**
   - Show what a beginner would do and where it breaks
   - Use a real-world analogy first (physical market, everyday scenario) before using financial numbers
   - The analogy must make the failure obvious without any domain knowledge

2. **Build each layer by showing what the previous layer missed**
   - Never introduce a more sophisticated method without first showing what the simpler one cannot see
   - End each layer with: "What this still misses: ..."
   - This gives the learner a reason to care about the next layer before it is introduced

3. **For every formula: explain WHY it is constructed that way**
   - Do not just state what the formula outputs
   - Walk through the logic: "why is X multiplied by Y?" with a plain English reason
   - Include a sanity check: what does the formula give in the simplest/edge case? Does that make sense?

4. **Use concrete numbers throughout**
   - Every concept gets a specific numerical example (real prices, real quantities, real outcomes)
   - Abstract descriptions alone are not enough — numbers make it believable
   - If you cannot make a concrete example, the explanation is not ready yet

5. **Answer the "why should I believe this?" question**
   - Every claim must be supported by a scenario that makes the learner feel it, not just understand it intellectually
   - If a concept requires a real-world scenario to land — write the scenario end-to-end
   - Do not move on until the WHY is answered, not just the WHAT

6. **End with a "sees vs misses" comparison**
   - For topics with multiple methods/layers, close with a table: Method | What it sees | What it misses
   - This anchors the full picture and shows how each layer is complementary, not redundant

7. **Update the notes file with the full richer version after Q&A**
   - The first pass of notes may be brief; after Q&A clarifies what needed more depth, rewrite that section fully
   - The final notes in market-making.md should reflect the deepest version of understanding reached, not the first draft

---

## Flip Rule (HARD)

Every defensive concept has an offensive equivalent. After learning how a mechanism
hurts us, always ask: if we were the faster / better-informed party, how would we use
the same mechanism against slower market makers?

Format: add a `### Strategy: <name>` entry under the relevant layer section in
`docs/architecture/alpha-strategies.md`. Keep it brief — just enough to know
what to revisit when infrastructure improves. Do NOT add offensive content to
engine-gaps.md or market-making.md — alpha-strategies.md is the only place.

Questions to answer for every flip:
- What does the victim look like? (slow cancel, weak signal, high spread)
- What infrastructure do we need to be on the hunting side?
- What is the rough economics? (profit per event, minimum move size to cover fees)
- Where in the engine does the offensive path already exist or need to be built?

Canonical reference: `docs/architecture/alpha-strategies.md` in the KCMME repo —
single consolidated register for all offensive strategies. Add new entries as
`### Strategy: <name>` under the relevant layer section as layers are completed.

Goal: we should never understand a weakness in our own engine without also
understanding how to exploit that same weakness in others when the conditions are met.

---

## Separation Rule (HARD)

**Learning file** (`market-making.md`) — pure concepts only:
- What it is, simple examples, how it works, professional standard, summary
- Terminology concepts learned along the way go in the Intermediate section as standalone entries
- No KCMME-specific content here — single source of truth for understanding the concept

**KCMME gap file** (`docs/architecture/gaps/engine-gaps.md`) — engine-specific only:
- Single consolidated file — one section per learning layer
- Add new gaps as `### Gap: <name>` entries under the relevant layer section
- Mark resolved gaps as `[RESOLVED <date>]` with one line on what fixed it
- Add `GH#<N>` reference when a gap is promoted to a GitHub issue
- No cross-reference in the learning file — the two are fully independent

---

# [Topic Name] — Learning

## 1. What It Is

Plain language. One or two paragraphs.
- What is this concept?
- Why does a market maker need to understand it?
- What breaks if you get it wrong?

---

## 2. Simple Example

Numbers-based, intuitive.
- Use a concrete scenario (specific prices, quantities, outcomes)
- Show what happens when it works correctly
- Show what happens when it fails
- No jargon. If you can't explain it with a simple example, you don't understand it yet.

---

## 3. How It Works (Simple → Sophisticated)

Build from the simplest version to the professional version.

### Basic approach
What a beginner would do. Where it falls short.

### Intermediate approach
What adds correctness. Why it's better than basic.

### Professional approach
What Jane Street / Citadel / Jump / Optiver actually do.
What data, signals, and models they use.
What makes their version structurally better.

Use formulas only when they're the clearest way to express the idea.
Skip derivations entirely.

---

## 4. Professional Standard (Jane Street / Citadel Level)

A clear picture of how the best firms handle this in practice:
- What inputs do they use?
- At what latency?
- What signals drive decisions?
- What does their system do that a typical system doesn't?

This is the benchmark. Everything below gets measured against this.

---

## 5. Summary

Quick reference. Fill this in last.

| | |
|---|---|
| **What it is** | One sentence |
| **Why it matters** | One sentence |
| **Professional standard** | One sentence |

---

## Notes & Open Questions

- Anything unclear that came up during learning
- Follow-up topics this connects to

---

## Math Reference (Optional)

Only include if a formula genuinely helps. No derivations.
Format: formula → what each variable means → what it tells you.

---
---

# [Topic Name] — KCMME Gap Analysis

*This section lives in `docs/architecture/gaps/<topic>.md` in the KCMME repo.*
*Copy this template there when starting a new topic.*

## How KCMME Handles It

- Formula or logic used
- Which signals are active
- Relevant `diag_*.jsonl` fields

## Gap vs Professional Standard

| Component | Professional Standard | KCMME | Gap |
|---|---|---|---|
| ... | ... | ... | ... |

## Is the Gap Actually an Issue?

For each gap:
- How large is the impact in practice?
- Is it a likely cause of current gpnl negativity?
- What would confirm it's a real problem?

Verdict per gap: **Likely issue / Investigate / Low priority**

## Open Questions

- Specific things to check in session data
