# NEON DRIFT — Go-to-Market, Launch & Product Refinement

> Researched: 2026-09-21 by Muse (main agent).
> Status: strategy brief, not a commitment. Revisit pricing/content scope before locking the Steam page.

**TL;DR:** Launch Steam-first at **$12.99** (10% launch discount → $11.69), anchored just above the closest comp Slipstream ($9.99). Ship a free demo into **Steam Next Fest February 2027** (October 2026 registration closed Aug 31). The product gap vs. Slipstream is modes and progression, not graphics — add a championship mode and time-trial leaderboards before launch. Mobile is phase 2.

---

## 1. Reference teardown: Slipstream (ansdor, solo dev, Steam May 2018)

Slipstream is the closest commercial reference: pseudo-3D Out Run-style arcade racer, custom engine, Steam-first. Verified facts from its [Steam page](https://store.steampowered.com/app/732810/Slipstream/):

| Fact | Slipstream | Implication for NEON DRIFT |
|---|---|---|
| Price | **$9.99** | The genre anchor. Don't launch above $14.99 without AA scope. |
| Reviews | ~1,700+, "Very Positive" | Achievable for a polished solo-dev racer; ~1.7k reviews ≈ 50–100k owners (Boxleiter-method estimate — *estimate*, not fact) |
| Achievements | 29 | Cheap to implement, feeds completionists and Steam engagement |
| Controller | Full support, "developers recommend controller" | Non-negotiable for the genre |
| Steam Deck | Verified | Entry ticket; test on Deck pre-launch |
| Tracks | 20 across cities/deserts/forests/mountains/beaches | Content bar: ≥12 tracks at launch or players call it thin |
| Modes | **6**: Grand Tour (branching road-trip), Cannonball (custom race), Grand Prix (5-race championship + car upgrades), Single Race, Time Trial, Battle Royale (elimination) | Modes are the depth story — see §3 |
| Cars | 5 models with distinct specs | Minimum viable roster: 4–5 |
| Music | 9 original songs + custom-music support | Synthwave OST is part of the fantasy; custom music is a cheap win |
| Visual options | 30fps mode, CRT/NTSC filters | Nostalgia filters cost little, market well |
| Multiplayer | Local up to 4 players | Couch multiplayer is a differentiator vs. mobile |

What Slipstream proves: a solo dev can ship a durable $9.99 pseudo-3D racer on Steam with modes + soundtrack doing the heavy lifting, not photorealism.

---

## 2. Selling points (what the Steam capsule should say)

NEON DRIFT's current pitch is "retro racer." That's a category, not a reason to buy. Sharpen to:

1. **"Out Run reimagined as an 80s anime film"** — the anime art direction is the single biggest visual differentiator vs. Slipstream's pixel look and Art of Rally's minimalism. Lead every screenshot with it.
2. **Drift-first handling** — if the drift feels great, say so explicitly ("twin-stick-style drift physics" or whatever the mechanic is). Slipstream's reviews praise "tight controls"; match that bar and name it.
3. **A real soundtrack, not loops** — commissioned synthwave/jazz-fusion tracks (Slipstream did 9 originals). Music is half the retro fantasy.
4. **Couch multiplayer** — 2–4 player split-screen is increasingly rare and markets itself to streamers.
5. **Free web demo, no install** — the existing web build is a marketing asset no comp has. "Play the demo in your browser right now" on the Steam page.

One-line test: *"Slipstream's arcade soul meets 80s anime — drift through neon cities in your browser or on Steam."*

---

## 3. Product refinements (before Steam launch)

Priority order — modes and progression first, because that's the documented gap vs. Slipstream:

1. **Championship/Grand Prix mode** — a 5-race series with points and car upgrades. Slipstream's Grand Prix is its retention backbone; a single-race-only game reads as a demo.
2. **Time Trial + leaderboards** — Steam leaderboards are nearly free via Steamworks and give speedrunners a reason to stay.
3. **Branching Grand Tour equivalent** — a road-trip mode with route choices (Out Run's fork mechanic). Distinctive, cheap to build from existing tracks.
4. **29-ish achievements** — copy Slipstream's count as a target; achievements drive completionist purchases and Steam profile visibility.
5. **CRT/scanline + NTSC filters** — nostalgia toggles that cost days, not weeks, and screenshot well.
6. **Full controller support + Steam Deck Verified** — test on Deck hardware before launch; "Verified" is a purchase filter for Deck owners.
7. **Custom music support** — let players drop in their own MP3s. Slipstream has it; synthwave fans have playlists ready.

Explicitly deferred: online multiplayer (cheating/netcode support burden for a solo dev — Slipstream skipped it too), story campaign, car tuning beyond simple upgrades.

---

## 4. Diversification ideas (post-launch revenue, ranked)

1. **Track-pack DLC ($4.99)** — 4–6 new tracks in a new biome (snow/mountain, harbor night). Racing DLC has the best attach rate in the genre; keep it cosmetic-track-only to avoid splitting the player base.
2. **Soundtrack DLC ($6.99)** — the OST as a Steam DLC. Synthwave fans buy soundtracks; near-zero marginal cost.
3. **New game modes as free updates** — Battle Royale/elimination mode (Slipstream has one) ships free to re-engage owners and trigger "recent reviews" bumps.
4. **Mobile port (phase 2)** — Android first via the existing WebView-wrapper experience, then iOS. See `steam-vs-mobile.md` §5: on mobile, evaluate free-with-ads or a subscription-catalog pitch (Apple Arcade-style) rather than a paid listing.
5. **Level editor / custom tracks** — only if the community asks; high support cost, do not pre-commit.

Do NOT diversify into: F2P conversion (destroys the premium positioning), NFT/blockchain anything, or a sequel before the DLC tail plays out.

---

## 5. Launch timeline (Steam-first)

> ⚠️ October 2026 Next Fest registration closed **August 31, 2026** — it is no longer an option. Next window: **February 2027** edition (exact dates TBA; 2026 pattern was late Feb).

| When | Milestone |
|---|---|
| Now → Nov 2026 | Steam "Coming Soon" page live (needs: capsule art, 5 screenshots, 1 trailer, short description). Start wishlist accumulation. |
| Nov → Jan 2027 | Free demo build (demos get their own store page). Press/streamer preview copies. |
| Feb 2027 | **Steam Next Fest** — demo front and center. Median Feb 2026 demo added ~800 wishlists; top decile far more (HowToMarketAGame survey, n=182 — *survey estimate*). |
| ~4–6 weeks post-fest | **Launch** at $12.99 with 10% launch discount. Controller support, achievements, Deck Verified on day one. |

> Companion viewing: [`transcripts/ocCLqI7EIlk.md`](../transcripts/ocCLqI7EIlk.md) — Gaby-ShareNut's Steam-marketing walkthrough (Chinese, 15:55). Corroborates this plan with 2026 case data: enter Next Fest with ~2,000 wishlists, one fest per lifetime (pick the last before launch), 10–15% launch discount, ~5,000–7,000 wishlists for a shot at Popular Upcoming, Discovery Queue as the #1 launch-day traffic source.

Why this order: Steam's discovery rewards momentum — wishlist velocity at launch pushes games into "Popular Upcoming." A demo in Next Fest is the cheapest momentum a solo dev can buy. (See `steam-vs-mobile.md` §3.)

---

## 6. Pricing rationale

- **Anchor:** Slipstream $9.99 (2018, 8 years old, frequently discounted). Inertial Drift $19.99. Art of Rally ~$24.99 (larger scope, console ports).
- **Recommendation: $12.99 list, 10% launch discount ($11.69).** Sits above the aging comp (justified by modern anime presentation + more modes) but below the $15+ tier where buyers expect AA scope. Regional pricing per Steam's recommended matrix.
- **Never launch above $14.99** without online multiplayer or a 20+ hour campaign — the genre's price ceiling for solo-dev scope is documented by the comps above.
- **Discount discipline:** first discount no earlier than 3 months post-launch, max 20–30%. Deep-discounting early trains buyers to wait (Slipstream's long tail survives on periodic 50%+ sales *years* after launch — that's a back-catalog strategy, not a launch one).

---

## 7. Marketing beats (solo-dev feasible)

1. **Demo link everywhere** — the free web demo is the funnel. Steam page, itch.io page, Reddit r/arcaderacing, Twitter/TikTok clips all point at "play in browser now."
2. **One good trailer** — 60 seconds, music-forward, drift montage. Trailers are the highest-ROI asset on a Steam page.
3. **Festival stacking** — beyond Next Fest, target genre-adjacent Steam fests (racing/driving themes) for free featuring.
4. **Streamer seeding** — 50 keys to small retro-gaming streamers pre-launch; the game's visual style clips well.
5. **Steam page SEO** — tags are the recommendation engine's input: `Racing`, `Arcade`, `Retro`, `Drift`, `1980s`, `Anime`, `Local Multiplayer`, `Controller`, `Steam Deck`. Copy Slipstream's tag set, then add the anime differentiators.

---

*Companion brief: `steam-vs-mobile.md` (platform economics). Update this file when the Steam page goes live or pricing locks.*
