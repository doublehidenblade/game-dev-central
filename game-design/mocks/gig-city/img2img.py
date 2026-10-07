#!/usr/bin/env python3
"""Image-to-image re-imagining via Gemini image model (nano-banana style).

Usage:
    img2img.py --in base.png --prompt "..." --out out.png [--model gemini-2.5-flash-image]

Auth via stored custom.gemini credential through authd surrogate; never sees the real key.
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import urllib.request

sys.path.insert(0, "/opt/hatch/skills/skill-creator/bin")
from dynamic_credentials import (  # noqa: E402
    DynamicCredentialError,
    read_json_response,
    url_with_surrogate_query_param,
)

ALLOWED_HOSTS = ("generativelanguage.googleapis.com",)
DEFAULT_MODEL = "gemini-2.5-flash-image"


def img2img(in_path: str, prompt: str, out_path: str, model: str) -> list[str]:
    with open(in_path, "rb") as fh:
        raw = fh.read()
    ext = os.path.splitext(in_path)[1].lower()
    mime = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg"}.get(
        ext.lstrip("."), "image/png"
    )
    url = url_with_surrogate_query_param(
        f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
        "custom.gemini",
        allowed_hosts=ALLOWED_HOSTS,
    )
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "inlineData": {
                            "mimeType": mime,
                            "data": base64.b64encode(raw).decode("ascii"),
                        }
                    },
                    {"text": prompt},
                ]
            }
        ],
        "generationConfig": {"responseModalities": ["IMAGE"]},
    }
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url, data=body, headers={"Content-Type": "application/json"}, method="POST"
    )
    opener = urllib.request.build_opener()
    proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
    if proxy:
        opener = urllib.request.build_opener(
            urllib.request.ProxyHandler({"https": proxy})
        )
    try:
        with opener.open(req, timeout=180) as resp:
            data = read_json_response(resp)
    except DynamicCredentialError:
        raise
    except Exception as exc:
        raise SystemExit(f"gemini img2img request failed: {exc}") from exc

    try:
        parts = data["candidates"][0]["content"]["parts"]
    except (KeyError, IndexError, TypeError):
        raise SystemExit(f"unexpected API response: {json.dumps(data)[:500]}")
    saved: list[str] = []
    for i, part in enumerate(parts):
        inline = part.get("inlineData")
        if not inline:
            continue
        img = base64.b64decode(inline["data"])
        out_mime = inline.get("mimeType", "image/png")
        out_ext = {"image/png": ".png", "image/jpeg": ".jpg"}.get(out_mime, ".png")
        base, _ = os.path.splitext(out_path)
        path = out_path if (i == 0) else f"{base}-{i}{out_ext}"
        if i == 0 and not path.endswith(out_ext):
            path = f"{path}{out_ext}"
        with open(path, "wb") as fh:
            fh.write(img)
        saved.append(path)
    if not saved:
        raise SystemExit(f"no image returned: {json.dumps(data)[:500]}")
    return saved


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--in", dest="in_path", required=True)
    p.add_argument("--prompt", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--model", default=DEFAULT_MODEL)
    a = p.parse_args()
    try:
        saved = img2img(a.in_path, a.prompt, a.out, a.model)
    except DynamicCredentialError as exc:
        raise SystemExit(f"credential error: {exc}") from exc
    print(json.dumps({"saved": saved}))


if __name__ == "__main__":
    main()
