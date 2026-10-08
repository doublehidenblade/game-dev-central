#!/usr/bin/env python3
"""RedNote/Xiaohongshu video transcript fetcher — no login required.

Takes an xhslink.com share link or a xiaohongshu.com note URL, resolves it,
pulls the page's embedded __INITIAL_STATE__ JSON, and downloads the
platform-generated subtitle files (zh-CN source + en-US machine translation
when available).

Usage:
    python3 xhs_transcript.py <url> [--out DIR] [--text-only]

Output: <note_id>.zh.srt, <note_id>.en.srt, and <note_id>.txt (plain text)
in DIR (default: current directory). Prints the note title + description.
"""
import re, json, sys, os, urllib.request, html as htmlmod

UA = ("Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
      "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 "
      "Mobile/15E148 Safari/604.1")

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=40) as r:
        return r.read().decode("utf-8", errors="replace")

def extract_state(page):
    m = re.search(r"window\.__INITIAL_STATE__\s*=\s*", page)
    i = page.find("{", m.end())
    depth, instr, esc, q = 0, False, False, ""
    for j in range(i, len(page)):
        c = page[j]
        if instr:
            if esc: esc = False
            elif c == "\\": esc = True
            elif c == q: instr = False
        else:
            if c in "\"'": instr, q = True, c
            elif c == "{": depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    raw = page[i:j + 1]
                    break
    raw = re.sub(r":undefined([,}])", r":null\1", raw)
    return json.loads(raw)

def find_note(o, note_id=None):
    if isinstance(o, dict):
        if o.get("noteId") == note_id and "video" in o:
            return o
        if note_id is None and "noteId" in o and "video" in o and "title" in o:
            return o
        for v in o.values():
            r = find_note(v, note_id)
            if r: return r
    elif isinstance(o, list):
        for v in o:
            r = find_note(v, note_id)
            if r: return r
    return None

def srt_to_text(srt):
    lines = []
    for block in srt.strip().split("\n\n"):
        parts = block.split("\n")
        if len(parts) >= 3:
            lines.append(" ".join(parts[2:]).strip())
    return "\n".join(lines)

def main():
    url = sys.argv[1]
    out = "."
    if "--out" in sys.argv:
        out = sys.argv[sys.argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    m = re.search(r"(?:discovery/item|explore)/([0-9a-f]{24})", url)
    note_id = m.group(1) if m else None

    page = fetch(url)
    if not note_id:
        m = re.search(r"(?:discovery/item|explore)/([0-9a-f]{24})", page)
        note_id = m.group(1) if m else "unknown"
    st = extract_state(page)
    note = find_note(st, note_id if note_id != "unknown" else None)
    if not note:
        sys.exit("note detail not found in page state")

    print("TITLE:", note.get("title"))
    print("DESC:", (note.get("desc") or "")[:400])
    print("NOTE_ID:", note["noteId"])

    mv2 = json.loads(note["video"]["mediaV2"])
    subs = mv2["video"].get("subtitles", {})
    got = []
    seen_lang = set()
    for key in ("zh-CN", "source", "en-US"):
        if key in subs:
            lang = "zh" if key != "en-US" else "en"
            if lang in seen_lang:
                continue
            seen_lang.add(lang)
            surl = subs[key][0]["url"]
            data = fetch(surl)
            srt_path = os.path.join(out, f"{note['noteId']}.{lang}.srt")
            open(srt_path, "w", encoding="utf-8").write(data)
            txt_path = os.path.join(out, f"{note['noteId']}.{lang}.txt")
            open(txt_path, "w", encoding="utf-8").write(srt_to_text(data))
            got.append(srt_path)
    if "--text-only" in sys.argv:
        for p in got:
            if p.endswith(".zh.srt"):
                print(srt_to_text(open(p, encoding="utf-8").read()))
                break
        else:
            for p in got:
                print(srt_to_text(open(p, encoding="utf-8").read()))
                break
    else:
        print("WROTE:", ", ".join(got))

if __name__ == "__main__":
    main()
