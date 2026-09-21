# Steam vs Mobile (iOS/Android) for NEON DRIFT
## Go-to-market research brief — retro arcade racer, web-based (HTML5)

*Prepared 2026-09-21. All figures reflect 2025–2026 reporting, linked.*

> **Audit note (2026-09-21):** figures below mix first-party sources (Valve, Apple, Google docs) with
> third-party estimates (analyst blogs, surveys). Estimates are labeled *estimate*. Where a claim
> rests on a single weak source it is qualified inline. Pricing recommendation moved to
> `gtm-launch-and-refinement.md` (§6: **$12.99** list, 10% launch discount).

**TL;DR: Ship Steam-first.** The retro arcade-racer audience that pays upfront lives on Steam. A $100 recoupable listing fee, a real discovery algorithm, and a genre track record (Slipstream, Inertial Drift, Art of Rally) make Steam the highest-expected-value platform. Mobile is a second act — and on mobile, the "premium racer" path increasingly means a subscription/bundle deal (e.g., Apple Arcade, à la Horizon Chase 2) rather than a standalone paid listing. The existing web build is the perfect free demo funnel for a Steam "Coming Soon" page.

---

## 1. Costs & fees, review processes, timelines

### Steam
- **Steam Direct fee: $100 per game, one-time.** It is not refundable but is *recouped* (returned through normal revenue payments) once the game hits $1,000 in adjusted gross revenue. There are no other mandatory publishing fees. ([generalistprogrammer.com](https://generalistprogrammer.com/tools/steam-revenue-calculator), [GamesRadar/Gamalytic](https://www.gamesradar.com/games/over-5-000-games-released-on-steam-this-year-didnt-make-enough-money-to-recover-the-usd100-fee-to-put-a-game-on-valves-store-research-estimates/))
- **Review: 3–5 business days typical; Valve asks you to plan for 7+.** Two gates: the store page and the product build must each be submitted and approved ("mark as ready for review" on each checklist). Build review checks that the game launches on every listed OS, that listed features (achievements, cloud saves) actually work, and that any in-game transactions go through the Steam Wallet (no external payment links). After approval, updates do **not** need re-review. ([partner.steamgames.com](https://partner.steamgames.com/doc/store/review_process?l=german&language=english))
- **Practical timeline:** store page live as "Coming Soon" as early as possible; practitioners budget a practical minimum of ~4–6 weeks from first submission to launch, including resubmission slack. ([steam-publisher SKILL.md](https://github.com/gavinmcfall/agentic-config/blob/HEAD/config/skills/game-dev/steam-publisher/SKILL.md))

### Apple App Store
- **$99/year, every year.** Stop paying and your app gets delisted — unlike Google, the cost is an ongoing subscription to the platform. ([dev.to](https://dev.to/preciousky_45d956626d31c3/what-it-actually-costs-to-publish-an-android-app-on-google-play-from-india-2026-numbers-abk))
- **Review:** Apple says **90% of submissions reviewed within 48 hours, 1.5-day average**, processing 200k+ submissions/week; every submission gets human review. Developers still report a long tail — standard reviews taking 2–7 days, worst cases stuck "Waiting for Review" for weeks — partly because AI-assisted submissions surged ~84% in a quarter in early 2026 (The Information via 9to5Mac; Apple disputes that times are lengthening). ([9to5mac.com](https://9to5mac.com/2026/06/09/apple-tightens-app-review-guidelines-against-apps-that-do-not-add-value-to-the-app-store/), [entrepreneur.com](https://www.entrepreneur.com/business-news/app-store-submissions-are-the-highest-in-10-years))
- **Rejection risk is the highest of the three stores:** historically ~30–40% rejection rates, and over 40% of unresolved issues come from "app completeness" (placeholder content, crashes, missing info). Human reviewers review every submission. ([grokipedia.com](https://grokipedia.com/page/App_store), [appinstitute.com](https://appinstitute.com/app-store-review-checklist/))
- **iOS builds require a Mac** (or cloud Mac rental) for Xcode signing; organization accounts require a D-U-N-S number; builds must target the latest iOS SDK (from April 2026, Xcode 26 / iOS 26 SDK). ([capacitorjs iOS/Android comparison](https://github.com/cap-go/website/blob/HEAD/apps/web/src/content/blog/en/capacitor-build-pipelines-ios-vs-android.md), [appinstitute.com](https://appinstitute.com/app-store-review-checklist/))

### Google Play
- **$25 one-time. No renewal, no per-app fee, no update fee** — the cheapest storefront by far. ([dev.to](https://dev.to/preciousky_45d956626d31c3/what-it-actually-costs-to-publish-an-android-app-on-google-play-from-india-2026-numbers-abk))
- **Review is largely automated and fast** (often hours), with lower rejection rates than Apple — but Google has been tightening low-quality-app enforcement. ([grokipedia.com](https://grokipedia.com/page/App_store))
- **Catch for new personal accounts: before production access, you must run a closed test with at least 12 testers continuously opted in for 14 days.** This is the step that surprises most first-time solo devs. ([openmapx.org mobile-release docs](https://github.com/openmapx/openmapx/blob/HEAD/docs/docs/developer/mobile-release.md), [appypie.com](https://www.appypie.com/blog/app-store-vs-google-play-stats))

| | Steam | App Store | Google Play |
|---|---|---|---|
| Upfront cost | $100/game (recouped at $1,000 revenue) | $99/year | $25 one-time |
| Review speed | 3–5 biz days (plan 7+) | ~1–2 days typical, long tail to weeks | Hours (automated) |
| Post-approval updates | No re-review | Re-reviewed (but fast) | Re-reviewed (fast) |
| First-timer hurdle | Store page + build checklists | Human review, high rejection rate, needs a Mac | 12 testers × 14-day closed test |

## 2. Revenue splits

### Steam — tiered, favors hits
- **70/30** on the first $10M, **75/25** on $10–50M, **80/20** above $50M (tiers since Oct 2018; effectively every indie pays 30%). ([tech-insider.org](https://tech-insider.org/valve-10-publishers-steam-price-fixing-lawsuit-2026/), [generalistprogrammer.com](https://generalistprogrammer.com/tools/steam-revenue-calculator))
- **Payment processing is included in Valve's 30%** — no additional card fees. ([generalistprogrammer.com](https://generalistprogrammer.com/tools/steam-revenue-calculator))
- Median reality check: Gamalytic data via GamesRadar — **65.9% of 2025 Steam releases earned under $1,000** (never recouping the fee), 40% under $100. One analyst's *estimate* puts median 2025-release revenue at ~$249 (vs $222 in 2024); treat median-revenue figures as rough, methodology varies by source. ([gamesradar.com](https://www.gamesradar.com/games/over-5-000-games-released-on-steam-this-year-didnt-make-enough-money-to-recover-the-usd100-fee-to-put-a-game-on-valves-store-research-estimates/), [linkedin.com playbook](https://www.linkedin.com/pulse/brutal-math-steam-2026-founders-playbook-launching-most-malankar-8dpxf))

### Apple — 15% is the realistic indie rate
- **30% standard; 15% under the Small Business Program** (under $1M/year in proceeds). Subscriptions drop to 15% after the first year. IAP processing is included in the commission. ([grokipedia.com](https://grokipedia.com/page/App_store), [appypie.com](https://www.appypie.com/blog/app-store-vs-google-play-stats))
- The practical indie advantage over Steam: you keep 85% of the first $1M, vs. Steam's flat 70% — but the buyer pool willing to pay upfront for an arcade racer on mobile is much smaller (see §4).

### Google Play — 15% on the first $1M/year (but fee structure is in flux)
- **15% on the first $1M of annual revenue, 30% above** — and unlike Apple, the 15% applies to the first $1M even if you earn more. ([techzonedaily.com](https://techzonedaily.com/google-undercuts-apple-with-new-15-revenue-share-for-play-apps/), [dev.to](https://dev.to/preciousky_45d956626d31c3/what-it-actually-costs-to-publish-an-android-app-on-google-play-from-india-2026-numbers-abk))
- **Caveat for 2026:** following the Epic settlement, Google is rolling out a new structure — Play Billing at 5% + a base service fee of 10%, with IAP commissions landing at ~20% for new installs / ~25% for existing installs above $1M (dropping 5% more with alternative billing). Treat the 15%-on-first-$1M figure as current but not permanent. ([appleinsider.com](https://appleinsider.com/articles/26/06/25/googles-new-payment-policies-are-a-preview-of-what-could-come-to-apple-platforms), [9to5google.com](https://9to5google.com/2025/11/05/google-play-store-fees-android-17-court-proposal/))

### Bottom line on splits
For a solo dev under $1M/year, Apple (15%) and Google (15%) are cheaper per-sale than Steam (30%). The catch is volume × price: Steam sells more premium copies at $10–20 to an audience trained to buy; mobile sells few paid copies and the money is in IAP/ads (see §3–4).

## 3. Discoverability — the brutal math

### Steam: a real algorithm, gated by momentum
- **~20,000 releases/year, ~half invisible.** SteamDB: **19,112 games launched on Steam in 2025**; **9,327 had fewer than 10 reviews** and 2,229 had zero reviews at all. ([pcgamer.com](https://www.pcgamer.com/gaming-industry/more-than-19-000-games-launched-on-steam-this-year-but-almost-half-have-fewer-than-10-reviews/))
- **"Steam's discovery algorithm rewards momentum, so games that launch without a pre-built wishlist or community tend to drown before anyone notices they exist."** ([gamerant.com](https://gamerant.Com/steam-indie-games-ai-generated-content-discoverability/))
- The levers that work: **tags** (they feed the recommendation engine), the **Discovery Queue**, curator networks, and above all **wishlist velocity** — launch-week wishlist conversions push games into "Popular Upcoming" and the front page. Aggregated indie data puts wishlist→purchase conversion at **~15–20% on launch day, 40–60% over the first year** (*practitioner estimate*, varies widely by genre and pre-launch marketing). ([techspot.com](https://www.techspot.com/news/110592-nearly-half-19000-games-released-steam-year-went.html), [generalistprogrammer.com](https://generalistprogrammer.com/tools/steam-revenue-calculator))
- **Demos now get their own store pages** (separate from the main game) and are the single best momentum tool: a demo in a **Steam Next Fest** can be enormous — Funselektor's *Over the Hill* drew **500,000+ players to its Next Fest demo** and crossed **1.2M wishlists** as an indie studio. A "Coming Soon" page + free demo is the standard indie playbook. ([techtimes.com](https://www.techtimes.com/articles/326142/20260901/over-hill-art-rally-maker-sets-october-14-steam-launch-off-road-explorer.htm), [hunker-bunker steam pipeline doc](https://github.com/grounded-play/hunker-bunker/blob/HEAD/docs/steam-build-pipeline.md))
- ⚠️ **Timing (2026-09-21): October 2026 Next Fest registration closed Aug 31, 2026.** Next window is the February 2027 edition (dates TBA). Each game may enter only one Next Fest — pick the edition closest to launch readiness.
- Tail distribution is top-heavy: in early 2026, just three games captured ~43% of all Steam game revenue, and the median paid game earned ~$350 lifetime. Momentum or nothing. ([gamerant.com](https://gamerant.Com/steam-indie-games-ai-generated-content-discoverability/))

### Mobile: bigger money, almost none of it for paid indie games
- Scale: App Store ~**2.42M apps**, Play ~**1.58M**; 2025 consumer spend **$117.6B (Apple)** vs **$49.2B (Google)**; Play has ~3× the downloads (104.6B vs 36.6B). ([appypie.com](https://www.appypie.com/blog/app-store-vs-google-play-stats))
- But **games are the stagnant part of mobile**: 2025 mobile game IAP sat around the **$82B band (+1.3% YoY)**; in Q2 2025, **non-gaming apps overtook games in IAP revenue for the first time** ($21.1B vs $19.8B). ([sqmagazine.co.uk](https://sqmagazine.co.uk/mobile-games-statistics/), [gameworldobserver.com](https://gameworldobserver.com/2025/08/13/sensor-tower-in-the-second-quarter-of-2025-apps-surpassed-mobile-games-in-iap-revenue-for-the-first-time))
- **1.4M new releases hit the mobile stores in 2025 (up 25% YoY), and only ~10% attracted meaningful attention.** Discovery on mobile = editorial featuring (rare), ASO (table stakes), and **paid user acquisition** — global CPI rose **30% to $0.56 in 2025**, and the median paid-to-organic install ratio jumped 61%. ([pocketgamer.biz](https://www.pocketgamer.biz/games-revenue-growth-stalls-in-2025-as-strategy-emerges-as-the-fastest-growing-genre/), [accio.com](https://www.accio.com/business/top-revenue-mobile-games-2025-trend))
- **The ad model dominates:** the share of mobile games with ad monetization rose from 45.1% (2021) to **55.6% (mid-2026)**; arcade games take ~13% of ad-revenue share. A one-time-premium racer without ads/IAP fights the dominant business model of the platform. ([gameworldobserver.com](https://gameworldobserver.com/?p=3409))
- **Premium iOS games are in decline:** Sensor Tower data puts premium iOS game revenue at its lowest, with analysts partly blaming Apple Arcade for training players not to pay upfront. ([gameworldobserver.com](https://gameworldobserver.com/?p=3409))

## 4. Audience fit — where do retro arcade racers actually sell?

### Steam is the proven home for this genre
- **Slipstream** (the closest comp — Out Run-style pseudo-3D): **~1,700+ reviews, "Very Positive"**, $9.99, full controller support, **Steam Deck Verified**, 29 achievements. A genre-faithful indie that found a durable audience on Steam. ([steambase.io](https://steambase.io/games/slipstream/reviews), [store.steampowered.com](https://store.steampowered.com/app/732810/Slipstream/))
- **Inertial Drift** (twin-stick drift arcade racer, 2020): **~1,650 reviews, "Very Positive"**, $19.99. ([store.steampowered.com](https://store.steampowered.com/app/1184480/Inertial_D))
- **Art of Rally** (stylized retro rally): **~4,000+ English reviews, 93% "Very Positive"**, Steam Deck Verified. Steam first (2020); consoles a year later. ([store.steampowered.com](https://store.steampowered.com/app/550320/art_of_rally/))
- The pattern: Steam buyers pay $10–20 for exactly this kind of game, own controllers, and play on Deck. Steam Deck Verified + controller support are the genre's entry tickets.

### Mobile: the premium-racer success stories detoured around paid listings
- **Horizon Chase** (2015) *was* the mobile-first retro arcade racer hit — and even it went multi-platform (PC/consoles) to grow. Its sequel, **Horizon Chase 2, launched as an Apple Arcade exclusive** (subscription, no IAP at all) before coming to PC/consoles. The lesson: on mobile, the viable "premium" path for arcade racers in the 2020s is a **subscription/bundle deal**, not a $4.99 listing fighting F2P giants. ([jalopnik.com](https://www.jalopnik.com/horizon-chase-2-is-here-for-your-new-old-racing-game-fi-1849534760/), [fingerguns.net](https://fingerguns.net/reviews/2022/09/13/horizon-chase-2-review-ios-apple-arcade-arcade-paradise/))
- **Art of Rally's mobile ports (by Noodlecake) only arrived January 2024 — 3+ years after the Steam launch.** Mobile was the victory lap, not the launchpad. ([wikipedia.org](https://en.wikipedia.org/wiki/Art_of_Rally))
- Touch controls are a real design tax for a drift-heavy racer (reviewers consistently recommend controllers), and the mobile audience's expectation is free-with-ads or subscription. Arcade is a top *download* genre on mobile (2.52B downloads in Q2 2025), but downloads ≠ willingness to pay. ([gameworldobserver.com](https://gameworldobserver.com/2025/08/13/sensor-tower-in-the-second-quarter-of-2025-apps-surpassed-mobile-games-in-iap-revenue-for-the-first-time))

## 5. Recommendation: Steam-first, then mobile — with a concrete sequence

### The recommended order
1. **Web demo stays free forever** (current state) — it doubles as marketing and playtesting.
2. **Steam "Coming Soon" page + free demo** (demos get their own store page; target a Steam Next Fest). Wishlist velocity is the whole game; a demo is the cheapest way to build it. Ship Windows first, add Linux/Steam Deck — macOS can wait (signing/notarization overhead).
3. **Steam launch** at **$12.99** (10% launch discount) with controller support, achievements, and Steam Deck Verified — full pricing rationale in `gtm-launch-and-refinement.md` §6. (Earlier draft said $9.99–14.99; locked to $12.99 on 2026-09-21 to sit above the 8-year-old Slipstream comp without hitting the $15+ AA-scope tier.)
4. **Mobile port as phase 2** — Android first (Craig already has WebView-wrapper experience here; $25 one-time fee), iOS second. On mobile, consider free-with-ads or a small upfront price; or pitch the premium angle to a subscription catalog.

### Web/HTML5 porting realities
- **Steam from HTML5 is a solved problem: wrap, don't rewrite.** The standard path is **Electron** (ships the Chromium you developed against — WebGL behavior stays deterministic) or **NW.js** (smaller executables). For Steam integration (achievements, overlay, matchmaking), use **steamworks.js** (the maintained successor to the aging Greenworks). ([gamedevjs.com](https://gamedevjs.com/tutorials/publishing-web-games-on-steam-with-electron/), [drawize.com](https://www.drawize.com/blog/tech-how-to-release-html5-game-on-steam), [dev.to](https://dev.to/jacklehamster/releasing-a-web-game-onto-steam-47cd?url=https://dev.to/jacklehamster/releasing-a-web-game-onto-steam-47cd), [construct.net](https://www.construct.net/en/forum/construct-3/general-discussion-7/electron-alternative-export-178676))
- **Precedent:** *Vampire Survivors* shipped v1 on Electron; the HTML5 game *Drawize* shipped on Steam at $6.99 via Electron+Greenworks, releasing **Windows 64-bit only** at first since it covers 95%+ of Steam players. Avoid OS-webview wrappers (e.g., Tauri) — WebGL/codec behavior varies per machine and breaks on Steam Deck's WebKitGTK. ([hunker-bunker steam pipeline doc](https://github.com/grounded-play/hunker-bunker/blob/HEAD/docs/steam-build-pipeline.md), [drawize.com](https://www.drawize.com/blog/tech-how-to-release-html5-game-on-steam))
- **Mobile wrapper:** Capacitor/WebView around the same web build is the low-cost route (Craig's Tunnel Time experience applies directly). Budget review-risk work: Apple's manual review rejects thin website-wrappers (guideline 4.2 / app completeness), so ship native-feeling extras — offline play, Game Center, controller support, native menus. ([capacitorjs iOS/Android comparison](https://github.com/cap-go/website/blob/HEAD/apps/web/src/content/blog/en/capacitor-build-pipelines-ios-vs-android.md), [grokipedia.com](https://grokipedia.com/page/App_store))

### Key risks, stated plainly
- Steam is a **momentum lottery**: ~half of releases get <10 reviews. Without a demo/Next Fest/community push, NEON DRIFT lands in the invisible half regardless of quality. The web demo is the built-in hedge — use it.
- Mobile paid-premium is **structurally hostile** to this genre (ad-model dominance, Apple Arcade training players away from upfront payment, declining premium iOS revenue). Don't lead with mobile.
- Apple's review queue has a long tail in 2026 and requires a Mac + $99/year; Google's 12-tester/14-day gate adds ~2 weeks minimum to an Android launch. Neither blocks a Steam-first plan.

*Bottom line: Steam-first with a demo-driven wishlist strategy is the only path where this genre has repeatedly won. Mobile is a port-and-monetize-later decision, not a launch decision.*
