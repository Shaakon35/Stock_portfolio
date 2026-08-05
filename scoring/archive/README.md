# Archived fundamentals snapshots

These dated `fundamentals_*.csv` snapshots predate the current conviction
formula and/or CSV schema. They are kept for historical reference only.

The live scorer (`scoring/score_holdings.py`) auto-picks the **newest**
`scoring/fundamentals_*.csv` at the top level via `default_csv()`, which globs
`scoring/fundamentals_*.csv` (not this subfolder), so nothing here is loaded
for live scoring. Point `--csv` at one of these explicitly only to reproduce a
past snapshot against today's formula.

## Why archived

- **`fundamentals_2026-06-25.csv`** — obsolete schema (no `ps_ratio`,
  `rev_growth_hist`, `net_margin_hist`). Loads gracefully (name-based parsing;
  missing columns degrade to neutral) but is not comparable to current output.
- **`fundamentals_2026-06-26.csv` / `2026-06-29.csv`** — current schema but
  predate the 2026-06-30 formula change (gross-margin + revenue-consistency in
  FUND/DCA quality) and the 2026-08-04 VAL change (absolute P/S co-signal +
  trough-PEG damping, margin-turnaround gate).
- **`fundamentals_2026-07-27.csv` / `2026-08-03.csv`** — current schema but
  predate the 2026-08-04 VAL/margin formula change.

The current live snapshot is `scoring/fundamentals_2026-08-04.csv`.
