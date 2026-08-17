#!/usr/bin/env python3
# =========================================================================
# CONVICTION-MOVERS REPORT — weekly week-over-week delta email
# =========================================================================
# WHY: after the weekly refresh regenerates docs/conviction.json, we want an
# email that summarises what MOVED in the conviction (`conv`) score since the
# previous weekly run, with a deep-dive ("zoom") on the biggest high-conviction
# movers. See docs/email_report_strategy.md for the full design.
#
# The two snapshots diffed are:
#   * --current  : this week's conviction.json (already on disk post-refresh).
#   * --previous : last week's. Pass a literal path, OR "-" to auto-resolve the
#                  immediately-preceding weekly refresh commit from git history
#                  (git show <sha>:docs/conviction.json).
#
# Inclusion (decision #3 — "held mostly, the rest if they move a lot"):
#   * HELD names          -> reported even on small drift (sensitive bar).
#   * NON-HELD names      -> only if |Δconv| >= MOVE_MIN_LO (big movers only).
#   * A FLAG FLIP (peak / marg / grade / binding) -> always reported.
#
# Output artifacts:
#   * --out-file    : a SELF-CONTAINED HTML report themed with the dashboard's
#                     own CSS tokens (parsed from docs/style.css at build time,
#                     so the theme tracks the site). Sent as the email ATTACHMENT.
#   * --out-inline  : a trimmed inline HTML body (header + held table + zoom) so
#                     the email is phone-readable without opening the attachment.
#   * --subject-out : the subject line (written to a file for the workflow).
#
# Pure stdlib (matches the scorer + export_*.py convention — no pip installs).
#
# Usage:
#   python3 scoring/report_conviction_movers.py \
#       --current docs/conviction.json --previous - \
#       --out-file /tmp/report.html --out-inline /tmp/inline.html \
#       --subject-out /tmp/subject.txt
#
#   # local eyeball against two arbitrary snapshots:
#   python3 scoring/report_conviction_movers.py \
#       --current docs/conviction.json \
#       --previous <(git show 79ade92:docs/conviction.json) \
#       --out-file /tmp/report.html
#
#   # self-test: diff two committed weekly snapshots end-to-end
#   python3 scoring/report_conviction_movers.py --selftest

import argparse
import html
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
_DEFAULT_CURRENT = _REPO_ROOT / "docs" / "conviction.json"
_STYLE_CSS = _REPO_ROOT / "docs" / "style.css"
_DASHBOARD_URL = "https://shaakon35.github.io/Stock_portfolio/"

# --- MOVEMENT THRESHOLDS (tune here) ------------------------------------
CONV_TIER = 7.0          # the conv>7 vs conv<=7 split from the request
MOVE_MIN_HI = 0.15       # >7 tier: min |Δconv| for a HELD name to be "moving"
MOVE_MIN_LO = 0.40       # <=7 tier / all non-held: only show BIG movers
ZOOM_TOP_N = 3           # how many top >7 movers to deep-dive in the zoom
FLAG_ALWAYS_REPORT = True  # a peak/marg/grade/binding FLIP is always reported
# "Watchlist opportunities": non-held names crossing into high conviction on a
# meaningful UP move. Surfaced as its own INLINE section so a good riser is not
# buried by decliners in the (capped) zoom. Tune the bar here.
OPP_MIN_CONV = 7.5       # a non-held name must now be at/above this conv
OPP_MIN_DCONV = 0.30     # ...AND have risen by at least this much week-over-week
# ------------------------------------------------------------------------

# Fallback palette if docs/style.css can't be parsed (kept in sync with it).
_FALLBACK_TOKENS = {
    "bg": "#020617", "bg-2": "#0f172a", "panel": "#0f172a",
    "panel-2": "#131c31", "panel-hi": "#1e293b", "border": "#1e293b",
    "border-hi": "#334155", "text": "#e2e8f0", "text-dim": "#94a3b8",
    "text-mut": "#64748b", "accent": "#34d399", "accent-2": "#22d3ee",
    "indigo": "#818cf8", "violet": "#a78bfa", "green": "#34d399",
    "green-bg": "rgba(52, 211, 153, .12)", "amber": "#fbbf24",
    "amber-bg": "rgba(251, 191, 36, .12)", "red": "#f87171",
    "red-bg": "rgba(248, 113, 113, .12)", "blue": "#60a5fa",
    "blue-bg": "rgba(96, 165, 250, .12)", "radius": "16px",
    "radius-sm": "10px",
    "shadow": "0 1px 0 rgba(255,255,255,.02) inset, 0 10px 30px rgba(0,0,0,.35)",
    "maxw": "1180px",
}


# =========================================================================
# Snapshot loading
# =========================================================================
def _load_json(path):
    with open(path, "r") as fh:
        return json.load(fh)


def _records_by_ticker(payload):
    out = {}
    for r in payload.get("records", []):
        t = r.get("ticker")
        if t:
            out[t] = r
    return out


def resolve_previous_from_git(current_date_str, current_by=None):
    """Find the newest 'Refresh conviction data' commit whose date differs from
    the current snapshot's date, and return its docs/conviction.json content.
    Falls back to any earlier commit that is genuinely different from the
    current snapshot, then to None if nothing is resolvable.

    `current_by` is the {ticker: record} map of the CURRENT snapshot. It is
    used to reject any candidate whose content is identical to current — which
    happens in a shallow (depth-1) clone where the only commit in `git log` is
    this run's own refresh. Returning that tip as "previous" would diff the
    snapshot against itself and produce a false all-zeros report. When that is
    the only thing available we return None so the caller falls back to baseline
    mode (an honest "first run" email) instead of a silent self-diff.
    """
    try:
        # List refresh commits (newest first) with their subject.
        log = subprocess.run(
            ["git", "log", "--pretty=%H %s", "--", "docs/conviction.json"],
            cwd=_REPO_ROOT, capture_output=True, text=True, check=True,
        ).stdout.splitlines()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None, None

    def _is_current(content):
        """True if a candidate snapshot is identical to the current one."""
        if current_by is None:
            return False
        return _records_by_ticker(content) == current_by

    # Prefer explicit weekly refresh commits with a DIFFERENT date stamp.
    date_re = re.compile(r"Refresh conviction data \((\d{4}-\d{2}-\d{2})\)")
    for line in log:
        sha, _, subject = line.partition(" ")
        m = date_re.search(subject)
        if m and m.group(1) != (current_date_str or ""):
            content = _git_show(sha, "docs/conviction.json")
            if content is not None and not _is_current(content):
                return content, sha
    # Fallback: any earlier commit that touched the file and is not identical
    # to the current snapshot (never self-diff — see docstring).
    for line in log:
        sha, _, subject = line.partition(" ")
        content = _git_show(sha, "docs/conviction.json")
        if content is not None and not _is_current(content):
            return content, sha
    return None, None


def _git_show(sha, path):
    try:
        raw = subprocess.run(
            ["git", "show", f"{sha}:{path}"],
            cwd=_REPO_ROOT, capture_output=True, text=True, check=True,
        ).stdout
        return json.loads(raw)
    except (subprocess.CalledProcessError, json.JSONDecodeError):
        return None


# =========================================================================
# Delta computation
# =========================================================================
def _num(r, key):
    v = r.get(key)
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def _flag_flips(prev, cur):
    """Return a list of human-readable flag transitions between two records."""
    flips = []
    # boolean flags
    for key, label in (("peak", "PEAK?"), ("marg", "MARG?")):
        was, now = bool(prev.get(key)), bool(cur.get(key))
        if was != now:
            flips.append(f"{'+' if now else '−'}{label}")
    # categorical transitions
    for key, label in (("grade", "grade"), ("binding", "binding")):
        was, now = prev.get(key), cur.get(key)
        if was != now and (was or now):
            flips.append(f"{label} {was}→{now}")
    # held / book weight
    if bool(prev.get("held")) != bool(cur.get("held")):
        flips.append("now HELD" if cur.get("held") else "no longer held")
    bp0, bp1 = _num(prev, "book_pct") or 0.0, _num(cur, "book_pct") or 0.0
    if abs(bp1 - bp0) >= 0.01:
        flips.append(f"book {bp0:g}%→{bp1:g}%")
    return flips


def compute_movers(prev_by, cur_by):
    """Build the classified movers structure from two {ticker: record} maps."""
    prev_tk = set(prev_by)
    cur_tk = set(cur_by)

    entries = sorted(cur_tk - prev_tk)     # NEW this week (no prior conv)
    exits = sorted(prev_tk - cur_tk)       # DROPPED from universe

    moved = []
    for t in sorted(prev_tk & cur_tk):
        p, c = prev_by[t], cur_by[t]
        cv0, cv1 = _num(p, "conv"), _num(c, "conv")
        if cv0 is None or cv1 is None:
            continue
        d = cv1 - cv0
        held = bool(c.get("held"))
        # "was-or-is > 7" tier (so real high-conv deteriorations aren't hidden)
        hi_tier = (cv0 > CONV_TIER) or (cv1 > CONV_TIER)
        flips = _flag_flips(p, c)

        bar = MOVE_MIN_HI if (held and hi_tier) else MOVE_MIN_LO
        include = (abs(d) >= bar) or (FLAG_ALWAYS_REPORT and flips)
        if not include:
            continue

        crossed = None
        if cv0 > CONV_TIER >= cv1:
            crossed = f"crossed BELOW {CONV_TIER:g}"
        elif cv0 <= CONV_TIER < cv1:
            crossed = f"crossed ABOVE {CONV_TIER:g}"

        moved.append({
            "ticker": t, "held": held, "hi_tier": hi_tier,
            "wave": c.get("wave"), "book_pct": _num(c, "book_pct") or 0.0,
            "conv0": cv0, "conv1": cv1, "d_conv": d,
            "dF": _delta(p, c, "F"), "dV": _delta(p, c, "V"),
            "dC": _delta(p, c, "C"),
            "F0": _num(p, "F"), "F1": _num(c, "F"),
            "V0": _num(p, "V"), "V1": _num(c, "V"),
            "C0": _num(p, "C"), "C1": _num(c, "C"),
            "grade0": p.get("grade"), "grade1": c.get("grade"),
            "binding0": p.get("binding"), "binding1": c.get("binding"),
            "cov1": _num(c, "coverage"),
            "has_data": bool(c.get("has_data", True)),
            "flips": flips, "crossed": crossed,
        })

    # Sort by magnitude of move, held first on ties.
    moved.sort(key=lambda m: (abs(m["d_conv"]), m["held"]), reverse=True)
    return {"moved": moved, "entries": entries, "exits": exits,
            "prev_by": prev_by, "cur_by": cur_by}


def _delta(p, c, key):
    a, b = _num(p, key), _num(c, key)
    if a is None or b is None:
        return None
    return b - a


def _attribution(m):
    """Plain-English 'why it moved' from the F/V/C layer deltas."""
    names = {"dF": "FUND", "dV": "VAL", "dC": "CYCLE"}
    parts = []
    biggest, bmag = None, 0.0
    for k in ("dF", "dV", "dC"):
        dv = m[k]
        if dv is None:
            continue
        if abs(dv) > bmag:
            biggest, bmag = k, abs(dv)
        if abs(dv) >= 0.05:
            parts.append(f"{names[k]} {dv:+.1f}")
    if not parts:
        return "layers ≈ flat (score shift from tier/flag change)"
    lead = ""
    if biggest == "dV" and m["dV"] and m["dV"] > 0:
        lead = "cheaper — "
    elif biggest == "dV" and m["dV"] and m["dV"] < 0:
        lead = "richer — "
    elif biggest == "dF":
        lead = "quality — "
    elif biggest == "dC":
        lead = "cycle — "
    return lead + "; ".join(parts)


# =========================================================================
# CSS token extraction (theme tracks the dashboard)
# =========================================================================
def load_css_tokens():
    """Parse the :root { --name: value; } block from docs/style.css so the
    report theme is a single source of truth with the site. Falls back to a
    baked-in copy if the file is unreadable."""
    try:
        css = _STYLE_CSS.read_text()
    except OSError:
        return dict(_FALLBACK_TOKENS)
    m = re.search(r":root\s*\{(.*?)\}", css, re.S)
    if not m:
        return dict(_FALLBACK_TOKENS)
    tokens = {}
    for name, val in re.findall(r"--([\w-]+)\s*:\s*([^;]+);", m.group(1)):
        tokens[name.strip()] = val.strip()
    # Ensure required keys exist even if the stylesheet drops one.
    for k, v in _FALLBACK_TOKENS.items():
        tokens.setdefault(k, v)
    return tokens


def _root_css(tokens):
    lines = "\n".join(f"      --{k}: {v};" for k, v in tokens.items())
    return f":root {{\n{lines}\n    }}"


# =========================================================================
# HTML rendering
# =========================================================================
def _esc(x):
    return html.escape(str(x)) if x is not None else ""


def _delta_span(d, digits=2):
    if d is None:
        return '<span class="mut">—</span>'
    cls = "up" if d > 0 else ("down" if d < 0 else "flat")
    arrow = "▲" if d > 0 else ("▼" if d < 0 else "•")
    return f'<span class="{cls}">{arrow} {d:+.{digits}f}</span>'


def _flag_pills(flips):
    if not flips:
        return ""
    return " ".join(f'<span class="pill">{_esc(f)}</span>' for f in flips)


def _movers_table(rows, show_book=True):
    if not rows:
        return '<p class="mut">None this week.</p>'
    head = (
        "<tr><th>Ticker</th><th>Wave</th>"
        + ("<th>Book%</th>" if show_book else "")
        + "<th>conv (prev→now)</th><th>Δconv</th>"
        "<th>ΔF</th><th>ΔV</th><th>ΔC</th><th>Flags</th></tr>"
    )
    body = []
    for m in rows:
        held_cls = ' class="held"' if m["held"] else ""
        book = f"{m['book_pct']:g}%" if m["book_pct"] else "—"
        cross = f' <span class="cross">{_esc(m["crossed"])}</span>' if m["crossed"] else ""
        gap = ' <span class="pill warn">⚠ thin</span>' if not m["has_data"] else ""
        body.append(
            f"<tr{held_cls}>"
            f'<td class="tk">{_esc(m["ticker"])}{cross}{gap}</td>'
            f'<td>{_esc(m["wave"])}</td>'
            + (f"<td>{book}</td>" if show_book else "")
            + f'<td class="num">{m["conv0"]:.2f} → <b>{m["conv1"]:.2f}</b></td>'
            f'<td class="num">{_delta_span(m["d_conv"])}</td>'
            f'<td class="num">{_delta_span(m["dF"], 1)}</td>'
            f'<td class="num">{_delta_span(m["dV"], 1)}</td>'
            f'<td class="num">{_delta_span(m["dC"], 1)}</td>'
            f'<td>{_flag_pills(m["flips"])}</td>'
            "</tr>"
        )
    return f'<table class="movers"><thead>{head}</thead><tbody>{"".join(body)}</tbody></table>'


def _zoom_cards(rows):
    if not rows:
        return '<p class="mut">No high-conviction (&gt;7) movers this week.</p>'
    cards = []
    for m in rows:
        dirn = "gained" if m["d_conv"] > 0 else "lost"
        held = '<span class="pill hold">HELD</span>' if m["held"] else ""
        book = f' · book {m["book_pct"]:g}%' if m["book_pct"] else ""
        flips = f'<div class="zflags">{_flag_pills(m["flips"])}</div>' if m["flips"] else ""
        cards.append(f"""
      <div class="zoom">
        <div class="zoom-head">
          <span class="tk big">{_esc(m['ticker'])}</span>
          <span class="mut">{_esc(m['wave'])}{book}</span>
          {held}
        </div>
        <div class="zoom-conv">
          conv {m['conv0']:.2f} → <b>{m['conv1']:.2f}</b>
          &nbsp; {_delta_span(m['d_conv'])} &nbsp;
          <span class="mut">({dirn})</span>
        </div>
        <div class="zoom-why"><b>Why:</b> {_esc(_attribution(m))}</div>
        <table class="layers">
          <tr><th></th><th>prev</th><th>now</th><th>Δ</th></tr>
          <tr><td>FUND</td><td class="num">{_fmt(m['F0'])}</td><td class="num">{_fmt(m['F1'])}</td><td class="num">{_delta_span(m['dF'],1)}</td></tr>
          <tr><td>VAL</td><td class="num">{_fmt(m['V0'])}</td><td class="num">{_fmt(m['V1'])}</td><td class="num">{_delta_span(m['dV'],1)}</td></tr>
          <tr><td>CYCLE</td><td class="num">{_fmt(m['C0'])}</td><td class="num">{_fmt(m['C1'])}</td><td class="num">{_delta_span(m['dC'],1)}</td></tr>
        </table>
        <div class="mut small">grade {_esc(m['grade0'])} → {_esc(m['grade1'])}
          · binding {_esc(m['binding0'])} → {_esc(m['binding1'])}
          · coverage {_fmt(m['cov1'],0)}%</div>
        {flips}
      </div>""")
    return "\n".join(cards)


def _fmt(v, digits=1):
    if v is None:
        return "—"
    return f"{v:.{digits}f}"


def _entries_exits(movers):
    entries, exits = movers["entries"], movers["exits"]
    cross = [m for m in movers["moved"] if m["crossed"]]
    if not (entries or exits or cross):
        return '<p class="mut">No entries, exits, or 7.0-line crossings.</p>'
    parts = []
    if cross:
        items = ", ".join(
            f'{_esc(m["ticker"])} ({m["conv0"]:.2f}→{m["conv1"]:.2f}, {_esc(m["crossed"])})'
            for m in cross)
        parts.append(f'<p><b>Tier crossings:</b> {items}</p>')
    if entries:
        parts.append(f'<p><b>New ({len(entries)}):</b> '
                     f'<span class="mut">{_esc(", ".join(entries))}</span></p>')
    if exits:
        parts.append(f'<p><b>Dropped ({len(exits)}):</b> '
                     f'<span class="mut">{_esc(", ".join(exits))}</span></p>')
    return "\n".join(parts)


_STYLE_TMPL = """
    {root}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0; padding: 24px;
      background:
        radial-gradient(1200px 600px at 80% -10%, rgba(124,140,255,.10), transparent 60%),
        radial-gradient(900px 500px at 0% 0%, rgba(52,211,153,.07), transparent 55%),
        var(--bg);
      color: var(--text);
      font-family: "Inter", system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
      -webkit-font-smoothing: antialiased;
    }}
    .wrap {{ max-width: var(--maxw); margin: 0 auto; }}
    h1 {{ font-size: 22px; margin: 0 0 4px; }}
    h2 {{ font-size: 15px; letter-spacing: .06em; text-transform: uppercase;
         color: var(--text-dim); margin: 26px 0 10px; }}
    a {{ color: var(--accent); text-decoration: none; }}
    .sub {{ color: var(--text-dim); font-size: 13px; }}
    .panel {{ background: var(--panel); border: 1px solid var(--border);
      border-radius: var(--radius); box-shadow: var(--shadow);
      padding: 16px 18px; margin: 0 0 14px; }}
    .stat {{ display: inline-block; margin-right: 22px; }}
    .stat b {{ font-size: 20px; color: var(--text); }}
    .stat span {{ display: block; font-size: 11px; text-transform: uppercase;
      letter-spacing: .06em; color: var(--text-mut); }}
    table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
    th {{ text-align: left; color: var(--text-mut); font-weight: 600;
      font-size: 11px; text-transform: uppercase; letter-spacing: .05em;
      padding: 6px 8px; border-bottom: 1px solid var(--border-hi); }}
    td {{ padding: 7px 8px; border-bottom: 1px solid var(--border); }}
    tr.held td {{ background: var(--green-bg); }}
    .num {{ text-align: right; font-variant-numeric: tabular-nums; }}
    .tk {{ font-weight: 700; }}
    .tk.big {{ font-size: 18px; }}
    .mut {{ color: var(--text-mut); }}
    .small {{ font-size: 12px; }}
    .up {{ color: var(--green); }}
    .down {{ color: var(--red); }}
    .flat {{ color: var(--text-mut); }}
    .cross {{ color: var(--amber); font-size: 11px; }}
    .pill {{ display: inline-block; padding: 1px 8px; border-radius: 999px;
      font-size: 11px; background: var(--amber-bg); color: var(--amber);
      border: 1px solid var(--border-hi); margin: 1px 2px; }}
    .pill.hold {{ background: var(--green-bg); color: var(--green); }}
    .pill.warn {{ background: var(--red-bg); color: var(--red); }}
    .zoom {{ background: var(--panel-2); border: 1px solid var(--border-hi);
      border-radius: var(--radius-sm); padding: 14px 16px; margin: 0 0 12px; }}
    .zoom-head {{ display: flex; align-items: center; gap: 10px; }}
    .zoom-conv {{ font-size: 15px; margin: 8px 0; }}
    .zoom-why {{ color: var(--text-dim); font-size: 13px; margin-bottom: 10px; }}
    table.layers {{ width: auto; margin: 6px 0; }}
    table.layers th, table.layers td {{ padding: 3px 14px 3px 0; border: none; }}
    .zflags {{ margin-top: 8px; }}
    .foot {{ color: var(--text-mut); font-size: 12px; margin-top: 20px;
      border-top: 1px solid var(--border); padding-top: 12px; }}
"""


def _header_stats(cur_payload, prev_payload, movers, prev_sha):
    held_movers = [m for m in movers["moved"] if m["held"]]
    up = sum(1 for m in movers["moved"] if m["d_conv"] > 0)
    dn = sum(1 for m in movers["moved"] if m["d_conv"] < 0)
    cur_date = cur_payload.get("generated_utc", "?")
    prev_date = prev_payload.get("generated_utc", "?")
    return {
        "up": up, "dn": dn,
        "held_moved": len(held_movers),
        "total_moved": len(movers["moved"]),
        "cur_date": cur_date, "prev_date": prev_date,
        "csv": cur_payload.get("csv", "?"),
        "universe": cur_payload.get("count", "?"),
        "prev_sha": prev_sha or "n/a",
    }


def render_html(cur_payload, prev_payload, movers, tokens, prev_sha,
                inline=False):
    st = _header_stats(cur_payload, prev_payload, movers, prev_sha)
    held_rows = [m for m in movers["moved"] if m["held"]]
    nonheld_rows = [m for m in movers["moved"] if not m["held"]]
    zoom_rows = [m for m in movers["moved"] if m["hi_tier"]][:ZOOM_TOP_N]

    nonheld_hi = [m for m in nonheld_rows if m["conv1"] > CONV_TIER]
    nonheld_lo = [m for m in nonheld_rows if m["conv1"] <= CONV_TIER]

    # Watchlist opportunities: non-held names now at/above OPP_MIN_CONV that
    # ROSE by at least OPP_MIN_DCONV this week. Sorted best-conviction first so
    # the strongest candidate leads. Shown INLINE (unlike the full non-held
    # tables) so a good riser is never buried by the capped zoom.
    opp_rows = sorted(
        (m for m in nonheld_rows
         if m["conv1"] >= OPP_MIN_CONV and m["d_conv"] >= OPP_MIN_DCONV),
        key=lambda m: m["conv1"], reverse=True,
    )

    style = _STYLE_TMPL.format(root=_root_css(tokens))
    title = "Conviction movers"

    header = f"""
  <div class="wrap">
    <h1>◈ {title}</h1>
    <div class="sub">week of {_esc(st['cur_date'])} · snapshot {_esc(st['csv'])}
      · universe {_esc(st['universe'])} names</div>
    <div class="panel" style="margin-top:14px">
      <span class="stat"><b class="up">▲ {st['up']}</b><span>up</span></span>
      <span class="stat"><b class="down">▼ {st['dn']}</b><span>down</span></span>
      <span class="stat"><b>{st['held_moved']}</b><span>held moved</span></span>
      <span class="stat"><b>{st['total_moved']}</b><span>total movers</span></span>
    </div>"""

    held_sec = f"""
    <h2>Held movers</h2>
    <div class="panel">{_movers_table(held_rows)}</div>"""

    zoom_sec = f"""
    <h2>Zoom — biggest high-conviction movers (&gt;{CONV_TIER:g})</h2>
    {_zoom_cards(zoom_rows)}"""

    opp_sec = f"""
    <h2>Watchlist opportunities</h2>
    <div class="panel">
      <div class="sub" style="margin-bottom:8px">non-held · now conv &ge;
        {OPP_MIN_CONV:g} · rose &ge; +{OPP_MIN_DCONV:g}</div>
      {_movers_table(opp_rows)}
    </div>"""

    if inline:
        # Trimmed body: header + held table + zoom + watchlist opportunities.
        foot = f"""
    <div class="foot">
      Full report attached. Live dashboard:
      <a href="{_DASHBOARD_URL}">{_DASHBOARD_URL}</a><br>
      Diff: previous snapshot @ {_esc(st['prev_sha'])[:10]} → current.
    </div>
  </div>"""
        return (f"<!doctype html><html><head><meta charset='utf-8'>"
                f"<style>{style}</style></head><body>"
                f"{header}{held_sec}{zoom_sec}{opp_sec}{foot}</body></html>")

    nonheld_sec = f"""
    <h2>Big movers — non-held (watchlist / bench)</h2>
    <div class="panel">
      <div class="sub" style="margin-bottom:8px">conv &gt; {CONV_TIER:g}</div>
      {_movers_table(nonheld_hi)}
    </div>
    <div class="panel">
      <div class="sub" style="margin-bottom:8px">conv ≤ {CONV_TIER:g}</div>
      {_movers_table(nonheld_lo)}
    </div>"""

    ee_sec = f"""
    <h2>Entries / exits / crossings</h2>
    <div class="panel">{_entries_exits(movers)}</div>"""

    foot = f"""
    <div class="foot">
      Generated {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}
      · previous snapshot @ {_esc(st['prev_sha'])} → current {_esc(st['cur_date'])}<br>
      Live dashboard: <a href="{_DASHBOARD_URL}">{_DASHBOARD_URL}</a>
      · thresholds: held &gt;{CONV_TIER:g} bar {MOVE_MIN_HI}, big-move bar {MOVE_MIN_LO}
    </div>
  </div>"""

    return (f"<!doctype html><html lang='en'><head><meta charset='utf-8'>"
            f"<meta name='viewport' content='width=device-width, initial-scale=1'>"
            f"<title>{title}</title><style>{style}</style></head><body>"
            f"{header}{held_sec}{zoom_sec}{opp_sec}{nonheld_sec}{ee_sec}{foot}"
            f"</body></html>")


def build_subject(cur_payload, movers):
    st_up = sum(1 for m in movers["moved"] if m["d_conv"] > 0)
    st_dn = sum(1 for m in movers["moved"] if m["d_conv"] < 0)
    date = (cur_payload.get("generated_utc", "") or "").split(" ")[0] or "?"
    return f"Conviction movers — week of {date} (\u25b2{st_up} \u25bc{st_dn})"


# =========================================================================
# Orchestration
# =========================================================================
def generate(current_path, previous_arg, out_file=None, out_inline=None,
             subject_out=None, scope="held-plus-big"):
    cur_payload = _load_json(current_path)
    cur_by = _records_by_ticker(cur_payload)
    cur_date = (cur_payload.get("generated_utc", "") or "").split(" ")[0]

    prev_sha = None
    if previous_arg in (None, "-", "auto"):
        prev_payload, prev_sha = resolve_previous_from_git(cur_date, cur_by)
        if prev_payload is None:
            # First run / no history — baseline only.
            prev_payload = {"records": [], "generated_utc": "(baseline)"}
    else:
        prev_payload = _load_json(previous_arg)

    prev_by = _records_by_ticker(prev_payload)
    movers = compute_movers(prev_by, cur_by)
    tokens = load_css_tokens()

    subject = build_subject(cur_payload, movers)

    if out_file:
        htmldoc = render_html(cur_payload, prev_payload, movers, tokens,
                              prev_sha, inline=False)
        Path(out_file).write_text(htmldoc)
    if out_inline:
        inlinedoc = render_html(cur_payload, prev_payload, movers, tokens,
                                prev_sha, inline=True)
        Path(out_inline).write_text(inlinedoc)
    if subject_out:
        Path(subject_out).write_text(subject)

    return movers, subject


def _selftest():
    """Diff two committed weekly snapshots end-to-end and write /tmp files."""
    prev = _git_show("7ce444c", "docs/conviction.json")
    cur = _git_show("79ade92", "docs/conviction.json")
    if prev is None or cur is None:
        print("selftest: could not load committed snapshots", file=sys.stderr)
        return 1
    prev_by, cur_by = _records_by_ticker(prev), _records_by_ticker(cur)
    movers = compute_movers(prev_by, cur_by)
    tokens = load_css_tokens()
    Path("/tmp/movers_selftest.html").write_text(
        render_html(cur, prev, movers, tokens, "7ce444c", inline=False))
    Path("/tmp/movers_selftest_inline.html").write_text(
        render_html(cur, prev, movers, tokens, "7ce444c", inline=True))
    held = sum(1 for m in movers["moved"] if m["held"])
    print(f"selftest OK: {len(movers['moved'])} movers "
          f"({held} held), {len(movers['entries'])} new, "
          f"{len(movers['exits'])} dropped")
    print("  subject:", build_subject(cur, movers))
    print("  wrote /tmp/movers_selftest.html + _inline.html")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--current", default=str(_DEFAULT_CURRENT),
                    help="this week's conviction.json")
    ap.add_argument("--previous", default="-",
                    help="last week's conviction.json path, or '-' to "
                         "auto-resolve from git history")
    ap.add_argument("--scope", default="held-plus-big",
                    choices=["held-plus-big"],
                    help="inclusion scope (held names + big non-held movers)")
    ap.add_argument("--out-file", help="standalone themed HTML report (attachment)")
    ap.add_argument("--out-inline", help="trimmed inline HTML body")
    ap.add_argument("--subject-out", help="write the subject line to this file")
    ap.add_argument("--selftest", action="store_true",
                    help="diff two committed snapshots and write /tmp samples")
    args = ap.parse_args()

    if args.selftest:
        sys.exit(_selftest())

    movers, subject = generate(
        args.current, args.previous,
        out_file=args.out_file, out_inline=args.out_inline,
        subject_out=args.subject_out, scope=args.scope,
    )
    held = sum(1 for m in movers["moved"] if m["held"])
    print(f"{len(movers['moved'])} movers ({held} held), "
          f"{len(movers['entries'])} new, {len(movers['exits'])} dropped")
    print("subject:", subject)


if __name__ == "__main__":
    main()
