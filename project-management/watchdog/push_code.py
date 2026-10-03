#!/usr/bin/env python3
"""Push watchdog code files to game-dev-central main via git-database API.
Reuses watch.py's _gh/_gh_api helpers (same auth). Aborts on moved ref."""
import sys, os, base64, subprocess

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import watch

# Self-gate (Craig 2026-10-03): the scriptification rule enforces itself —
# no code sync while ~/AGENTS.md holds an untagged post-rule lesson.
_here = os.path.dirname(os.path.abspath(__file__))
_ar = subprocess.run([sys.executable, os.path.join(_here, "watch.py"),
                      "scriptification-audit"],
                     capture_output=True, text=True)
sys.stdout.write(_ar.stdout)
if _ar.returncode != 0:
    sys.stderr.write(_ar.stderr)
    print("push_code: ABORT — scriptification-audit failed; tag new "
          "AGENTS.md lessons [SCRIPTED: watch.py <cmd>] or "
          "[JUDGMENT-ONLY: <why>] before syncing code.")
    sys.exit(1)

FILES = {
    "project-management/watchdog/watch.py": "watch.py",
    "project-management/watchdog/test_rules.py": "test_rules.py",
}
msg = sys.argv[1] if len(sys.argv) > 1 else "watchdog: sync code"

ref = watch._gh(f"/repos/{watch.WATCHDOG_REPO}/git/ref/heads/main")
base_commit = ref["object"]["sha"]
base_tree = watch._gh(
    f"/repos/{watch.WATCHDOG_REPO}/git/commits/{base_commit}")["tree"]["sha"]

entries, changed = [], 0
for repo_path, local in FILES.items():
    with open(local, "rb") as f:
        raw = f.read()
    try:
        blob0 = watch._gh(
            f"/repos/{watch.WATCHDOG_REPO}/contents/{repo_path}?ref=main")
        same = base64.b64decode(blob0["content"]) == raw
    except Exception:
        same = False
    if same:
        print(f"unchanged: {repo_path}")
        continue
    blob = watch._gh_api("POST", f"/repos/{watch.WATCHDOG_REPO}/git/blobs",
                         {"content": base64.b64encode(raw).decode(),
                          "encoding": "base64"})
    entries.append({"path": repo_path, "mode": "100644",
                    "type": "blob", "sha": blob["sha"]})
    changed += 1
    print(f"staged: {repo_path}")

if not changed:
    print("CODE-PUSH nothing changed")
    sys.exit(0)

new_tree = watch._gh_api(
    "POST", f"/repos/{watch.WATCHDOG_REPO}/git/trees",
    {"base_tree": base_tree, "tree": entries})["sha"]
commit = watch._gh_api(
    "POST", f"/repos/{watch.WATCHDOG_REPO}/git/commits",
    {"message": msg, "tree": new_tree, "parents": [base_commit]})["sha"]
ref_now = watch._gh(
    f"/repos/{watch.WATCHDOG_REPO}/git/ref/heads/main")["object"]["sha"]
if ref_now != base_commit:
    print(f"CODE-PUSH ABORTED: ref moved ({base_commit[:8]} -> {ref_now[:8]})")
    sys.exit(2)
watch._gh_api("PATCH", f"/repos/{watch.WATCHDOG_REPO}/git/refs/heads/main",
              {"sha": commit})
print(f"CODE-PUSH ok: {commit[:8]} ({changed} files)")
