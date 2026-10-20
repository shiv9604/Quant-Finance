# Career Portfolio — Proof of Skill

One entry per completed level: real work done on KCMME that proves the skill to an
employer. Written at Step 7 of each level. Source material for Level 19 (interviews,
resume, STAR stories).

Entry format:

### Level N — <skill>
- **What I did** (hands-on, on KCMME):
- **Result** (number, finding, artifact link):
- **What it proves** (which Junior / Mid / Senior bar):
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
