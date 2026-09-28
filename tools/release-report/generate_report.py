#!/usr/bin/env python3
"""
generate_report.py — "Everything new since last deploy" report generator.

Reads the release ledger (pending.json + baselines.json) and the local
evidence/ image store, then emits a per-game markdown report with embedded
screenshots. No GitHub API calls, no re-downloads, no re-inspection.

Usage:
    python3 generate_report.py [--game neon|tokyo] [--out report.md]

The report covers everything merged-but-not-live since the last baseline
(Craig's last play). Run it when he asks "what's new" — it's instant.
"""
import json
import os
import sys
from datetime import datetime, timezone

BASE = os.path.dirname(os.path.abspath(__file__))
PENDING = os.path.join(BASE, "pending.json")
BASELINES = os.path.join(BASE, "baselines.json")
EVIDENCE = os.path.join(BASE, "evidence")

# Maps a ledger task id -> (short plain-English name, evidence filename prefix).
# Add rows here as new tasks ship; the generator picks them up automatically.
TASK_META = {
    # Tokyo multiplayer batch (v23)
    "td-096": ("host chase camera", "td096"),
    "td-097": ("start-grid train", "td097"),
    "td-098": ("redundant lobby prompts", "td098"),
    "td-099": ("multiplayer collisions", "td099"),
    "td-090": ("position HUD", "td090"),
    "td-089": ("input-overlay dismissal", "td089"),
    "td-095": ("TURN relay (lag fix)", None),      # networking — no screenshot
    "td-093": ("guest unfreeze", None),             # already live in v22
    "td-092": ("smoke-test mock fix", None),        # test-only
    # NEON visual batch
    "p3d-101": ("arch bridge", "p3d101"),
    "p3d-076": ("building side faces", "p3d076"),
    "p3d-103": ("HUD hearts", "p3d103"),
    "p3d-084": ("gantry labels", "p3d084"),
    "p3d-082": ("rival sprites", "p3d082"),
    "p3d-077": ("START banner", "p3d077"),
    "p3d-100": ("loader hang fix", None),           # not visual
    "p3d-081": ("speed rebalance", None),           # not visual
    "p3d-078": ("rail collision", None),            # has QA evidence in repo
    "p3d-079": ("collision sparks", None),          # has QA evidence in repo
    "p3d-104": ("nitro/steering", None),            # input — not visual
    "p3d-102": ("finish-line gating", None),        # logic — not visual
    "p3d-089": ("CPU regression docs", None),       # docs only
    "p3d-088": ("harbor snapshot", None),           # snapshot refresh
    "p3d-083": ("fork readability", None),          # check repo QA
    "todo122": ("ground-perspective reconcile", None),
}

GAME_NAMES = {"tokyo": "Tokyo Drift 3D", "neon": "NEON DRIFT"}
GAME_LINKS = {
    "tokyo": "https://doublehidenblade.github.io/tokyo-drift-3d-web/",
    "neon": "https://doublehidenblade.github.io/neon-drift-web/",
}
# Evidence screenshots live in the shared repo; the report links to each
# image's blob page (one link per image) instead of embedding image bytes.
# New evidence must be committed under this path for its link to resolve.
EVIDENCE_BLOB_BASE = ("https://github.com/doublehidenblade/game-dev-central"
                      "/blob/main/project-management/release-evidence")


def load_json(path, default):
    try:
        with open(path) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def evidence_images(prefix):
    """Return (paired, extra) image filenames for a task prefix."""
    if not prefix or not os.path.isdir(EVIDENCE):
        return [], []
    files = os.listdir(EVIDENCE)
    matches = [f for f in files if f.startswith(prefix + "-")]
    befores = sorted(f for f in matches if "-before" in f)
    afters = sorted(f for f in matches if "-after" in f)
    # Pair them; also keep unpaired afters (e.g. td090-hud-1of2/2of2)
    paired = list(zip(befores, afters))
    extra = afters[len(paired):]
    return paired, extra


def report_game(game, pending_items, baseline):
    lines = []
    name = GAME_NAMES.get(game, game)
    lines.append(f"# {name} — new since last deploy")
    lines.append("")
    lines.append(f"Play it: {GAME_LINKS.get(game, '')}")
    if baseline:
        sha = baseline.get('web_sha') or baseline.get('sha', '?')
        at = baseline.get('web_published_at') or baseline.get('published_at') or baseline.get('at', '?')
        lines.append(f"Last live: {sha[:8]} ({at})")
    lines.append("")
    lines.append(f"{len(pending_items)} change(s) merged, not yet live.")
    lines.append("")

    visual, nonvisual = [], []
    for item in pending_items:
        task = item.get("task", "?")
        meta = TASK_META.get(task, (item.get("summary", task)[:60], None))
        short, prefix = meta
        paired, extra = evidence_images(prefix)
        if paired or extra:
            visual.append((task, short, item, paired, extra))
        else:
            nonvisual.append((task, short, item))

    if visual:
        lines.append("## Visual fixes (screenshot links below)")
        lines.append("")
        for task, short, item, paired, extra in visual:
            lines.append(f"### {short} ({task}, PR #{item.get('pr', '?')})")
            lines.append(f"{item.get('summary', '')}")
            lines.append("")
            for b, a in paired:
                lines.append(f"Before / after:")
                lines.append(f"- [{task} before]({EVIDENCE_BLOB_BASE}/{b})")
                lines.append(f"- [{task} after]({EVIDENCE_BLOB_BASE}/{a})")
                lines.append("")
            for x in extra:
                lines.append(f"- [{task}]({EVIDENCE_BLOB_BASE}/{x})")
                lines.append("")

    if nonvisual:
        lines.append("## Other changes (no screenshots — code/logic/docs)")
        lines.append("")
        for task, short, item in nonvisual:
            lines.append(f"- **{short}** ({task}, PR #{item.get('pr', '?')}): "
                         f"{item.get('summary', '')}")
        lines.append("")

    return "\n".join(lines)


def main():
    game_filter = None
    out_path = None
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--game" and i + 1 < len(args):
            game_filter = args[i + 1]
            i += 2
        elif args[i] == "--out" and i + 1 < len(args):
            out_path = args[i + 1]
            i += 2
        else:
            i += 1

    pending = load_json(PENDING, {"pending": []})
    items = pending.get("pending", []) if isinstance(pending, dict) else pending
    baselines = load_json(BASELINES, {})

    by_game = {}
    for item in items:
        g = item.get("game", "?")
        if game_filter and g != game_filter:
            continue
        by_game.setdefault(g, []).append(item)

    parts = []
    for game in sorted(by_game):
        parts.append(report_game(game, by_game[game],
                                baselines.get(game, {})))
        parts.append("\n---\n")

    report = "\n".join(parts).rstrip() + "\n"
    if out_path:
        with open(out_path, "w") as f:
            f.write(report)
        print(f"Wrote {out_path} ({len(report)} chars)")
    else:
        print(report)


if __name__ == "__main__":
    main()
