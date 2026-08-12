# Strategy: Weekly conviction-movement email report

**Status: STRATEGY / PROPOSAL ONLY — not implemented.**
Design for a weekly email to `val35131@gmail.com` summarising what moved in the
conviction score after each automated refresh, with a deep-dive on the biggest
movers.

### Confirmed decisions (from the owner)

1. **Sender = recipient**: send from and to `val35131@gmail.com` (one Gmail App
   Password, simplest).
2. **Thresholds**: accept the defaults (`>7` tier bar 0.15, `≤7` tier bar 0.40,
   zoom top 3) — tunable constants in the script.
3. **Scope**: **held names mostly**; watchlist / bench names appear **only if
   they moved a lot**. Concretely — *all* held names are always in scope (even
   small drift is reported); non-held names must clear the higher "big move" bar
   to appear at all. See §4.3.
4. **Cadence**: **weekly only** (schedule + manual dispatch); no email on the
   allocation-edit republish path.
5. **Delivery format**: a **structured standalone HTML file, styled with the same
   CSS/theme as the conviction GitHub Pages dashboard** — delivered as an
   **email attachment**, plus an inline email body summary. See §5.5.

---

## 1. Goal (restated from the request)

After the weekly automated workflow runs, send an email that:

1. **Overview** — what has been *moving* in the conviction (`conv`) score since
   the previous weekly run (week-over-week deltas).
2. **Zoom / deep-dive** — for names with **conv > 7**, focus on the one(s) that
   **moved the most** (explain *why*: which layer F/V/C drove it, flags, etc.).
3. **Filtered tail** — for names with **conv ≤ 7**, list **only** the ones that
   **moved a lot** (i.e. suppress the noise; show only material movers).

Email destination: **val35131@gmail.com**.

---

## 2. Key enabler — history is already in git

No new datastore is needed. The weekly refresh commits `docs/conviction.json`
with a message `Refresh conviction data (YYYY-MM-DD)`. That means **every past
week's full scoreboard is recoverable from git history**:

```
$ git log --oneline --grep="Refresh conviction data"
cd397c1 Refresh conviction data (2026-08-10)
79ade92 Refresh conviction data (2026-08-03)
7ce444c Refresh conviction data (2026-07-27)
```

and any prior snapshot reads cleanly:

```
git show <sha>:docs/conviction.json
```

So the delta engine is simply: **current `conviction.json`** vs the
**`conviction.json` from the immediately-preceding refresh commit**. This is
deterministic, auditable, and needs zero extra infrastructure.

Each record already carries everything the report needs:

```json
{ "ticker","wave","held","book_pct","strategy","conv","grade",
  "F","V","C","binding","coverage","peak","marg","has_data" }
```

---

## 3. Where it plugs in

The report runs as a **new final step inside the existing weekly workflow**
`.github/workflows/refresh-data.yml`, *after* the "Commit & push if changed"
step. Reasons:

- The refresh job already regenerates and commits the new `conviction.json`;
  once that commit exists, `HEAD` = this week and `HEAD~` (the previous refresh
  commit for that file) = last week — exactly the two snapshots we diff.
- Keeping it in the same job means the email fires **only on the weekly cadence**
  (Monday 06:00 UTC schedule) and after a successful refresh + validation gate.
- The allocation-change republish workflow (`republish-on-allocation-change.yml`)
  will **not** send email — that path is intra-week manual edits, not the weekly
  movement report. (Optional toggle discussed in §8.)

Trigger summary:
- ✅ Weekly `schedule` refresh → send report.
- ✅ Manual `workflow_dispatch` of the refresh → send report (useful for testing).
- ❌ Allocation-edit republish → no email.

---

## 4. New component: the delta / report builder

Add one self-contained, stdlib-only script:

```
scoring/report_conviction_movers.py
```

Consistent with the repo convention (the scorer and all `export_*.py` helpers
are pure-stdlib, no pip installs).

### 4.1 Inputs

- `--current docs/conviction.json` (this week, already on disk post-refresh).
- `--previous -` → the script resolves the prior week itself by shelling out to
  git: find the newest `Refresh conviction data` commit **before HEAD** that
  touched `docs/conviction.json`, and `git show <sha>:docs/conviction.json`.
  (Fallback: `HEAD~1:docs/conviction.json` if grep finds nothing — e.g. very
  first run.)
- `--out-html`, `--out-text` — render both an HTML body (rich table) and a
  plaintext fallback (multipart email).

### 4.2 Matching & delta

- Join current vs previous **by ticker**.
- For each ticker compute:
  - `d_conv = conv_now − conv_prev`
  - `d_F`, `d_V`, `d_C` (layer deltas — used in the zoom to attribute *why*).
  - flag transitions: `peak`, `marg`, `grade`, `binding`, `held`, `book_pct`.
- Classify each ticker:
  - **NEW** — present now, absent last week (newly added watchlist/held name).
  - **DROPPED** — present last week, absent now (removed from universe).
  - **MOVED** — present both weeks, `|d_conv| ≥ threshold`.
  - **STABLE** — present both weeks, `|d_conv| < threshold` (suppressed).

### 4.3 "Moved a lot" thresholds (tunable constants at top of script)

The universe is large (~750 names, mostly the 688-name watchlist bench), so the
report must be *opinionated* about what counts as a real move, and it must treat
the two conviction tiers differently exactly as requested:

```python
# --- MOVEMENT THRESHOLDS (tune here) ------------------------------
CONV_TIER          = 7.0    # the conv>7 vs conv<=7 split from the request
MOVE_MIN_HI        = 0.15   # conv>7 tier: min |Δconv| to be "moving"
MOVE_MIN_LO        = 0.40   # conv<=7 tier: only show BIG movers (higher bar)
ZOOM_TOP_N         = 3      # how many top movers to deep-dive in the zoom
FLAG_ALWAYS_REPORT = True   # a peak/marg/grade FLIP is always reported,
                            # regardless of Δconv size
# ------------------------------------------------------------------
```

**Held-vs-not is the primary gate (decision #3), tier is secondary.** A row is
included when:

```python
included = (
    is_held                                  # held: report even small drift…
    and abs(d_conv) >= (MOVE_MIN_HI if conv_hi_tier else MOVE_MIN_LO)
) or (
    not is_held                              # not held: only BIG movers…
    and abs(d_conv) >= MOVE_MIN_LO
) or (
    FLAG_ALWAYS_REPORT and flag_flipped      # …or any flag flip, either group
)
```

- **Held names** are the focus: a held name in the conv>7 tier reports on the
  *sensitive* 0.15 bar; a held name that has slipped to ≤7 uses the 0.40 bar (a
  big move to warrant attention) — but held names are never dropped for being on
  the bench, because they're not on the bench.
- **Non-held names** (watchlist / global bench) appear **only if they moved a
  lot** (`≥ MOVE_MIN_LO = 0.40`) — matching "the rest if they move a lot".
  Everything quieter is dropped from the email entirely.
- A **flag flip** (e.g. a name newly showing `[PEAK?]`, or `grade` crossing into
  AVOID/TRIM) is material regardless of `Δconv` magnitude, so it is surfaced
  even if the number barely moved (applies to both held and non-held).

Within the report, the **conv>7 vs conv≤7 split still drives the section layout
and the zoom** (§5): the zoom always deep-dives the top `ZOOM_TOP_N` movers that
sit in the >7 tier (held names ranked first on ties), and the ≤7 section lists
the remaining big movers.

Tier membership is decided as **"was-or-is > 7"** (a name that fell from 7.2 →
6.9 is still evaluated in the >7 tier logic so real high-conviction
deteriorations are never hidden) — see the edge-case handling in §7.

---

## 5. Report structure & delivery format

Subject: `Conviction movers — week of YYYY-MM-DD (▲N ▼M)`

Per decision #5 the deliverable is a **structured standalone HTML report file,
themed with the same CSS/design language as the conviction dashboard**, sent as
an **email attachment**, with a short inline body so the email is readable at a
glance even before opening the attachment.

### 5.1–5.5 Report sections (same in the HTML file and the inline summary)

1. **Header line** — refresh date, CSV snapshot name, universe size, and count
   of movers in each group (held / big-non-held). One-glance summary.

2. **§ HELD MOVERS** — every **held** name that cleared its bar (§4.3), sorted
   by `|Δconv|` desc. This is the primary section (decision #3).

   | Ticker | Wave | Book% | conv (prev → now) | Δconv | ΔF ΔV ΔC | Flags |
   |--------|------|-------|-------------------|-------|----------|-------|

3. **§ ZOOM — biggest high-conviction mover(s)** — deep-dive on the top
   `ZOOM_TOP_N` movers in the >7 tier (held ranked first on ties). For each:
   - Full before/after: conv, F, V, C, binding layer, grade, coverage.
   - **Attribution**: which layer moved most (`ΔF/ΔV/ΔC`) → plain-English cause,
     e.g. *"VAL +1.1 (cheaper: P/S fell / PEG improved); FUND flat; CYCLE −0.2"*.
   - Any flag change (`peak`, `marg`, grade, binding, book %).
   - Book weight if held.

4. **§ BIG MOVERS — NON-HELD (watchlist / bench)** — non-held names with
   `|Δconv| ≥ MOVE_MIN_LO` only (decision #3, "the rest if they move a lot").
   Split visually into a conv>7 block and a conv≤7 block. If none clear the bar,
   the section says *"No material non-held movers this week."*

5. **§ ENTRIES / EXITS** — NEW and DROPPED names (short list). A name crossing
   the 7.0 line in either direction is called out here too (e.g. *"CRDO crossed
   below 7.0: 7.05 → 6.82"*), since a tier crossing is itself signal.

6. **Footer** — link to the live dashboard (GitHub Pages) and the exact two
   commit SHAs diffed, for auditability.

### 5.5 Styling the HTML file to match the dashboard

The live dashboard (`docs/index.html`) loads styling from an **external**
`docs/style.css` and remote Google Fonts (`<link>`). Neither survives as-is in a
saved-and-opened HTML attachment offline, and email clients strip `<link>`/
remote CSS entirely. So the report is a **self-contained HTML document** that
reuses the dashboard's *design tokens* rather than linking its stylesheet:

- **Inline a `<style>` block** in the report `<head>` that imports the same CSS
  custom-properties (the `:root` palette in `style.css`: `--bg #020617`,
  `--panel #0f172a`, `--accent #34d399` emerald, `--red #f87171`, `--amber`,
  `--radius 16px`, `--shadow`, the slate text scale, etc.) and the same panel /
  table / pill / badge rules. This gives the dark-slate + emerald look identical
  to the site without an external file.
- **Extract, don't duplicate**: the build script reads the token block straight
  out of `docs/style.css` at generation time (parse the `:root { … }` block) and
  a small hand-kept subset of the panel/table rules, so the report theme tracks
  the dashboard if the palette is ever retuned — single source of truth.
- **Font**: keep the `Inter` `@import` for when the file is opened in a browser,
  but fall back to `system-ui, -apple-system, Segoe UI, Roboto, sans-serif`
  (already the dashboard's fallback) so it looks right offline / in mail clients.
- **Delta colour semantics** reuse the dashboard tokens: `Δconv > 0` →
  `--green/--green-bg`, `Δconv < 0` → `--red/--red-bg`, flags → `--amber-bg`
  pills, exactly like the grade/flag badges on the site — so the email reads as a
  native extension of the dashboard.
- Layout mirrors the site's **panel + rounded table** idiom (`--radius`,
  `--shadow`, `--border`), not a generic email template.

The **inline email body** (multipart HTML) carries a trimmed version of the same
theme (a compact header + the Held-movers table + the zoom), so the email is
useful on a phone without downloading the attachment; the full file is the
attachment for the complete tables.

---

## 6. Sending the email — mechanism & secrets

GitHub Actions has no built-in mailer, so use the well-maintained
`dawidd6/action-send-mail` SMTP action (or an equivalent SMTP `curl` step). The
report script writes the HTML/text bodies to files; the mail step attaches them.

### 6.1 Gmail SMTP (confirmed: sender = recipient = val35131@gmail.com)

- Per decision #1, the **same Gmail account is both sender and recipient** — one
  App Password to set up.
- Server: `smtp.gmail.com:465` (SSL).
- **Required GitHub repo secrets** (Settings → Secrets and variables → Actions):
  - `MAIL_USERNAME` = `val35131@gmail.com` (the sending + receiving account)
  - `MAIL_PASSWORD` = a Gmail **App Password** for that account (NOT the normal
    password; requires 2-Step Verification enabled on the Google account, then
    Google Account → Security → App passwords → generate a 16-char password)
  - `MAIL_SERVER` = `smtp.gmail.com` and `MAIL_PORT` = `465` — optional (the
    workflow can hardcode these Gmail constants and only require the two
    credential secrets above).

`MAIL_TO` is your own address, so it can be hardcoded to `val35131@gmail.com` in
the workflow rather than stored as a secret. Nothing secret is ever printed to
logs; the mail step reads credentials from `secrets`.

### 6.2 Workflow step sketch (illustrative — not committed yet)

```yaml
      - name: Build movers report
        id: report
        run: |
          set -euo pipefail
          # Emits: a themed standalone attachment (--out-file), a trimmed inline
          # HTML body (--out-inline), and the subject line.
          python3 scoring/report_conviction_movers.py \
            --current docs/conviction.json \
            --previous - \
            --scope held-plus-big \
            --out-file  /tmp/conviction_movers_$(date -u +%F).html \
            --out-inline /tmp/inline.html \
            --subject-out /tmp/subject.txt
          echo "subject=$(cat /tmp/subject.txt)" >> "$GITHUB_OUTPUT"
          echo "attach=/tmp/conviction_movers_$(date -u +%F).html" >> "$GITHUB_OUTPUT"

      - name: Email the report
        if: ${{ github.event_name == 'schedule' || github.event_name == 'workflow_dispatch' }}
        continue-on-error: true   # a send failure must not fail the data refresh
        uses: dawidd6/action-send-mail@v3
        with:
          server_address: smtp.gmail.com
          server_port:    465
          secure:         true
          username:       ${{ secrets.MAIL_USERNAME }}
          password:       ${{ secrets.MAIL_PASSWORD }}
          subject:        ${{ steps.report.outputs.subject }}
          to:             val35131@gmail.com
          from:           "Conviction Bot <${{ secrets.MAIL_USERNAME }}>"
          html_body:      file:///tmp/inline.html      # phone-readable summary
          attachments:    ${{ steps.report.outputs.attach }}  # full themed report
```

Placed **after** the commit/push step in `refresh-data.yml`, guarded so it only
mails on `schedule`/`workflow_dispatch` (decision #4: weekly only).

---

## 7. Edge cases & correctness

- **First run / no prior snapshot** — if no earlier `Refresh conviction data`
  commit exists, the script emails a "baseline established, no deltas yet" note
  instead of failing.
- **Same-day re-run** — the refresh workflow can run twice in a day
  (manual + schedule). The delta must compare against the *previous distinct*
  refresh, not a same-day earlier commit. The git-log resolver picks the newest
  refresh commit whose date differs from HEAD's (skip `[skip republish]` and
  same-`YYYY-MM-DD` commits).
- **Universe grew** (e.g. +122 names last week). NEW names are listed under
  Entries, never counted as "moves" (no prior conv to diff). Prevents a huge
  false "everything moved" report on weeks a batch is added.
- **Tier boundary flips** — a name straddling 7.0 is reported in **both** the
  crossing note (§5) and whichever tier its *current* conv sits in. To avoid a
  big drop being hidden (e.g. 7.6 → 6.5 would land in the ≤7 tier and might miss
  the sensitive bar), evaluate a name in the **high tier if EITHER week's conv
  was > 7** — so real high-conviction deteriorations are never suppressed by the
  higher low-tier bar.
- **`has_data:false` / `[GAP]` names** — thin-data scores are noisy; annotate
  their rows with a `⚠ thin data` marker so a move driven by newly-arrived data
  isn't misread as a fundamental shift.
- **Determinism** — the scorer is already deterministic; the report is a pure
  function of the two JSON files, so re-runs are reproducible.
- **Email failure isolation** — the mail step is the *last* step and
  `continue-on-error` is set so a transient SMTP failure never rolls back or
  red-flags the successful data refresh/commit. A failed send is visible in the
  Actions log and self-heals next week.

---

## 8. Decisions — CONFIRMED

All open questions are now settled (owner answers folded into the design above):

1. **Sender account** — ✅ same Gmail (`val35131@gmail.com`) as both sender and
   recipient; one App Password. (§6.1)
2. **Thresholds** — ✅ defaults accepted: `>7` bar 0.15, `≤7` bar 0.40, zoom top
   3; constants at the top of the script. (§4.3)
3. **Scope** — ✅ **held names mostly**: all held names in scope; non-held
   (watchlist/bench) only if they moved a lot (`≥0.40`). Implemented as
   `--scope held-plus-big`. (§4.3, §5)
4. **Cadence** — ✅ weekly only (schedule + manual dispatch); no email on the
   allocation-edit republish path. (§3, §6.2)
5. **Delivery format** — ✅ a structured **standalone HTML file themed with the
   dashboard's CSS**, sent as an attachment, plus a trimmed inline HTML body for
   phone reading. (§5.5)

---

## 9. Implementation checklist (for the build phase — NOT done yet)

- [ ] `scoring/report_conviction_movers.py` — delta engine + themed HTML renderer
      (stdlib only; git-resolver for the previous snapshot; tunable thresholds;
      `--scope held-plus-big` default; emits `--out-file` attachment +
      `--out-inline` body + `--subject-out`).
- [ ] CSS-token extractor: parse the `:root` block from `docs/style.css` at build
      time and inline it into the report `<head>` so the theme tracks the
      dashboard (single source of truth). (§5.5)
- [ ] Self-test mode (`--selftest`) diffing two committed snapshots (e.g.
      2026-07-27 vs 2026-08-03) to eyeball the HTML locally before wiring email.
- [ ] Add "Build movers report" + "Email the report" steps to
      `.github/workflows/refresh-data.yml` (after commit/push, schedule/dispatch
      guarded, `continue-on-error` on the send, Gmail SMTP with attachment).
- [ ] Add the two repo secrets `MAIL_USERNAME` / `MAIL_PASSWORD` (Gmail App
      Password) — documented in the workflow header comment and in `AGENTS.md`
      (new "Weekly email report" subsection).
- [ ] One manual `workflow_dispatch` dry-run to confirm the email renders in
      Gmail (inline body + attachment open with the dark-slate theme) before
      relying on the Monday schedule.

---

### TL;DR

Diff this week's `docs/conviction.json` against the previous weekly refresh
commit (history already in git). Report **all held names** that moved (sensitive
0.15 bar in the >7 tier), plus **non-held names only if they moved a lot** (0.40
bar), with a top-3 **zoom** explaining which F/V/C layer drove the biggest >7
move. Render a **standalone HTML report themed with the dashboard's own CSS
tokens**, attach it (plus a trimmed inline body) and send via **Gmail SMTP**
(sender = recipient = `val35131@gmail.com`) as the last step of the existing
**weekly** `refresh-data.yml`. Zero new infrastructure, stdlib-only script,
thresholds tunable in one block.
