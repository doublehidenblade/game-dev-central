# Video Transcription — Methods Log

How we get transcripts of YouTube videos for this hub. Newest first.
If a method stops working, note the date and move on to the next.

## 2026-09-21 session notes (ocCLqI7EIlk + BUGXF75K7Qk)

- **youtube-transcript-api: BLOCKED** — both videos return `TranscriptsDisabled`
  (creators disabled captions; no manual or auto subs). yt-dlp confirms no subtitles.
- **yt-dlp audio download: PARTIAL** — `BUGXF75K7Qk` downloaded fine (8.4 MB mp3,
  12:08 audio). `ocCLqI7EIlk` now fails with *"Sign in to confirm you're not a bot"*
  (HTTP 403 from YouTube's player API). The block is per-video/intermittent, not
  total — retry later or use the browser-transcript route for the blocked video.
- **faster-whisper tiny (Chinese): INADEQUATE for publishing** — 348 segments,
  language detected zh p=1.00, but heavy homophone errors on domain terms
  (e.g. speaker name garbled, game titles mangled). Fine for gist, not for a
  verbatim transcript file. Use medium or larger for Chinese.
- **faster-whisper medium: needs writable HF cache** — `/opt/hatch-image/models/asr`
  is read-only; set `HF_HOME=~/workspace/khub-venv/hf-cache`. Also set
  `HF_HUB_DISABLE_XET=1` (the XET/CAS download path failed with I/O errors).
- **huggingface_hub + proxy pitfall** — `no_proxy` contains bracketed IPv6 entries
  (`[::1]`, …) that crash httpx's env-proxy parsing (`InvalidURL: Invalid port`).
  Workaround: override `no_proxy`/`NO_PROXY` to `localhost,127.0.0.1` when calling
  huggingface_hub; keep `http_proxy`/`https_proxy` for egress.
- **TLS:** venv `certifi` needs the Hatch egress CA appended, else yt-dlp/hf fail
  on certificate verify:
  `cat /run/hatch/egress-tls/ca-bundle.pem >> $(venv/bin/python -c "import certifi; print(certifi.where())")`
- **VM reboots wipe /tmp** — keep venv, models, and audio under `~/workspace`.
- Audio files are ephemeral: delete after transcription. Transcripts only in the repo.

## Method 1: Official YouTube transcript panel (browser) — try first

- If the video has captions (manual or auto), open the video in the browser,
  expand the description, click "Show transcript" / "Open transcript", and copy
  the timestamped text. No download, no ASR errors.
- Fails exactly when Method 2 (API) fails — no captions, no panel.

## Method 2: youtube-transcript-api (timed-text API)

- Library: `youtube-transcript-api` (`YouTubeTranscriptApi().fetch(video_id)`).
- Fast, free, no download. Useless when creators disable captions.

## Method 3: Local ASR on audio-only download

- `yt-dlp -x --audio-format mp3` (audio only — never full video),
  then `faster-whisper` (**medium** minimum for Chinese, int8, CPU) with `language="zh"`.
- Quality check before publishing: listen-sample 3 random segments, check proper
  nouns / game titles / numbers; mark uncertain lines with `[?]`.
- Never fabricate unclear lines — `[inaudible]` beats a guessed word.

## Method 4 (avoid): third-party transcript sites

- Sites like youtubetotranscript.com wrap the same timed-text API — they fail
  exactly when Method 1/2 fail. Many are ad-heavy or ask for sign-in; skip.
- Paid ASR services are the only fallback if local ASR is unavailable.
