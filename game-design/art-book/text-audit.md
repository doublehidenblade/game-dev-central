# Kurogane Bay Art Book — Text Audit Report
**Date:** 2026-10-05
**Auditor:** TEXT-AUDIT worker (Muse subagent)

## Craig's Verdict (verbatim, the law)
> "there's a lot of fake japanese and even english texts in them. They should be real japanese. English is reserved for american army camp related or international port related parts."

## Method
- Every PNG opened and inspected by the auditor personally.
- All Japanese strings verified via the **gemini-consult** skill (`gemini-3.8-flash` on stored `custom.gemini` credential) — never the auditor's own Japanese.
- Showa-era signage conventions applied: kanji/kana usage, vertical storefront signboards, enamel signs, split-flap boards.
- **Hybrid fix method:** generate base scene with ALL signage blank via gemini-imagegen, then overlay exact corrected text via PIL using Noto CJK fonts. For paint-over fixes on existing art: clone-patches or opaque boxes, then PIL text overlay.
- Key lesson: `anchor="mm"` is provably accurate; always crop the target region and measure coordinates from the crop before placing text.

## Gemini Consult Verdicts (received 2026-10-05, relied on throughout)
- Taxi roof = company name or タクシー (chose 黒金タクシー); 空車 is interior flip sign, never roof. Taxi door: 黒金交通.
- Koban plate: 派出所 (交番 is post-1994). Expressway green signs MUST pair kanji with romaji below.
- Split-flap: 整理券配布中; 第1ターミナル 呼出番号 88.
- Worldmap: 天空エレベーター→軌道エレベーター; 鴎→かもめ町; 渚海岸→渚; 上層市街, 南エアリウム, 大黒埠頭, 黒金山, 天神, 浮体パネル群, 深海盆地 OK.
- Dust-tithe booth: 降塵税 徴収所. Car-wash: 洗車場.
- ゴリアテ 800 + 大型クレーン車 OK; callouts ブーム/フック/荷台/泥よけ/ラジエーターグリル/ウインチ/排気管 OK.
- オオトリ・ソブリン; specs: 全長 7,200mm / 車両重量 4,000kg / V型12気筒 ディーゼルターボ / 防弾仕様.
- Crate stencils: ワレモノ注意/取扱注意/輸出 + 天地無用.
- KMTED cruiser door: 黒金市警察 交通部; booth plaque: 第七区派出所; street signs: 第七区本通/工場街.
- Checkpoint banner: 海運組 検問. Iron Wheel banner: 鉄輪連合.
- Chalkboard: 高架橋 強風注意/軸重限度 20t/無線 89.4MHz. Pump: 軽油. Fascia: 鉄輪燃料給油所. Chop-shop plates: 営業中 + 持込整備.
- Bus destination blind: 天神駅前. Bus plate: 黒金 22 か 14-41 format.
- Address plaque: 渚町三丁目 (vertical, city name omitted). Shop signs: 大衆食堂, たばこ, 酒場, 丼物, 食堂 all OK.

---

## Chapter: upper-city
### mock-4-corporate-plaza.png — REGENERATED
- Strings: 黒金湾高速 / 天神出口 (green gantry sign)
- Verdict: Real Japanese. Expressway green signs per Gemini MUST pair kanji with romaji below (noted as limitation — see impl-1 below).

### impl-1-skyway-ribbon.png — REGENERATED
- Strings: 天神 / 黒金湾 / 第一ターミナル (3 small green signs)
- Verdict: Real Japanese. **Caveat:** Gemini requires romaji below kanji on green expressway signs; these small impl signs had no room — flagged for parent.

### impl-3-terminal-1.png — REGENERATED
- Strings: 第1ターミナル (rooftop band)
- Verdict: Real Japanese, correct.

## Chapter: outskirts
### impl-waystation-dusk.png — REGENERATED
- Strings: 鉄輪燃料 (red fascia)
- Verdict: Real Japanese.

### mock-waystation-dusk.png — REGENERATED
- Strings: 鉄輪燃料給油所 (fascia), 高架橋 強風注意 / 軸重限度 20t / 無線 89.4MHz (chalkboard), 軽油 (pump), 営業中 (plate)
- Verdict: All real Japanese, Gemini-verified.

## Chapter: factions
### mock-american-depot.png — REGENERATED
- Strings: U.S. ARMY stencils
- Verdict: English ALLOWED — American army camp context per Craig's rule.

### mock-kaiun-checkpoint.png — REGENERATED
- Strings: 海運組 / 検問 (banner)
- Verdict: Real Japanese, Gemini-verified.

### mock-kmted-cruiser.png — REGENERATED
- Strings: 黒金市警察 / 交通部 (door), 第七区本通 / 工場街 (street signs)
- Verdict: Real Japanese, Gemini-verified.

### impl-ironwheel-garage.png — REGENERATED
- Strings: 鉄輪連合 (checkered banner)
- Verdict: Real Japanese, Gemini-verified.

### impl-kmted-cruiser.png — REGENERATED
- Strings: 第七区派出所 (booth plaque)
- Verdict: Real Japanese (派出所 correct for Showa era, not 交番).

## Chapter: fleet-gear
### mock-goliath-800.png — REGENERATED
- Strings: ゴリアテ 800 / 大型クレーン車 (title), ブーム / フック / 荷台 / 泥よけ / ラジエーターグリル / ウインチ / 排気管 (callouts with PIL leader lines)
- Verdict: All real Japanese, Gemini-verified.

### mock-ohtori-sovereign.png — REGENERATED
- Strings: オオトリ・ソブリン, 全長 7,200mm / 車両重量 4,000kg / V型12気筒 ディーゼルターボ / 防弾仕様
- Verdict: All real Japanese, Gemini-verified.

### mock-hinode-carrier.png — REGENERATED
- Strings: 黒金タクシー (roof), 黒金交通 (door), HINODE (grille badge, kept — manufacturer badge)
- Verdict: Real Japanese, Gemini-verified.

### mock-cargo-lashing.png — REGENERATED
- Strings: ワレモノ注意 / 取扱注意 / 輸出 / 天地無用 (crate stencils)
- Verdict: All real Japanese, Gemini-verified.

### impl-hinode-carrier.png — REGENERATED
- Strings: タクシー (roof sign)
- Verdict: Real Japanese (company name or タクシー per Gemini; 空車 never on roof).

## Chapter: world-lore
### mock-dust-tithe.png — REGENERATED
- Strings: 降塵税 / 徴収所 (booth sign)
- Verdict: Real Japanese, Gemini-verified.

### impl-dust-tithe.png — REGENERATED
- Strings: 洗車場 (shed sign), タクシー (taxi roof)
- Verdict: Real Japanese, Gemini-verified.

### mock-worldmap.png — REGENERATED (10 bilingual labels)
- Strings: 上層市街/UPPER CITY, 南エアリウム/MINAMI AERIUM, 黒金山/MT. KUROGANE, 軌道エレベーター/ORBITAL ELEVATORS, 大黒埠頭/DAIKOKU PIERS, かもめ町/KAMOME, 天神/TENJIN, 渚/NAGISA, 浮体パネル群/PANEL FIELDS, 深海盆地/SHINKAI BASIN
- Verdict: All Gemini-verified (天空エレベーター→軌道エレベーター, 鴎→かもめ町, 渚海岸→渚). Remnant English labels painted over via clone-patch; visually verified clean.

## Chapter: lower-city
- 9 PNGs regenerated with verified-correct Japanese in prior work session (pre-compaction). Details in prior session summary; all written back to original paths.

---

## Earlier Mocks (12, mirrored at github.com/doublehidenblade/tokyo-drift-3d-web/tree/main/qa/kurogane-bay/)

### showa-dust/sd1-dust-shotengai.png — FIXED & RE-PUSHED
- Found: "酒 ひ ビール" (stray ひ), "酒 洋食 井物 うどん" (井物 = mangled 丼物), center sign garbled kanji, left red vertical "めうん大衆食堂" (garbled prefix)
- Fixed: removed ひ; 井物→丼物; center→大衆食堂; left red→大衆食堂 (garbled prefix painted over)
- Verdict: All fixed strings Gemini-verified real Japanese.

### showa-dust/sd2-dust-hauler.png — FIXED & RE-PUSHED
- Found: destination blind "呂比須" (fake kanji), building sign "ガエウ" (fake katakana)
- Fixed: blind→天神駅前; building→たばこ
- Verdict: Gemini-verified.

### showa-dust/sd3-tram-capsule-dust.png — PASS (no text issues found)

### showa-dust/sd4-masked-street.png — FIXED & RE-PUSHED
- Found: white sign "禁之洲" (fake kanji), taxi door "龍の" (fake)
- Fixed: white sign→酒場; taxi door→黒金交通 (vertical)
- Verdict: Gemini-verified. (Beer sign "アサヒビール" left as-is — real brand Japanese, not fake.)

### showa-dust/sd5-sandblasted-facade.png — PASS (no text issues found)

### showa-dust/sd6-noren-dustflap.png — FIXED & RE-PUSHED
- Found: blue oval plaque with fake kanji
- Fixed: plaque→渚町三丁目 (vertical, city omitted per Gemini)
- Verdict: Gemini-verified. (Noren crests are stylized mon symbols, not text — left as-is.)

### gig-city-v2/v2a-lower-dust-street.png — FIXED & RE-PUSHED
- Found: taxi trunk "HOBSBGAS" / "Kouiki 670" (fake English), shop sign "ポルキン" (fake katakana)
- Fixed: trunk text painted over (blank); shop→食堂
- Verdict: English removed per Craig's rule (not army/port context); 食堂 Gemini-verified.

### gig-city-v2/v2b-upper-city-cloudbreak.png — PASS (no text issues found)

### gig-city-v2/v2c-sky-elevator-terminal.png — FIXED & RE-PUSHED
- Found: red vertical banners "千席" (fake — "1000 seats" makes no sense for a terminal)
- Fixed: both banners→天神 (vertical)
- Verdict: Gemini-verified place name.

### gig-city-v2/v2d-outskirts-wacky-sea.png — PASS (no visible text; taxi roof/door blank at this resolution)

### gig-city-v2/v2e-bay-floating-panels.png — PASS (no text issues found)

### gig-city-v2/v2f-masked-driver.png — PASS (no text issues found)

### Push verification
All 6 fixed PNGs pushed to `doublehidenblade/tokyo-drift-3d-web` under `qa/kurogane-bay/` via git-data API (commits 59890131, e619d1f3). Each raw URL curl-verified HTTP 200 unauthenticated:
- https://raw.githubusercontent.com/doublehidenblade/tokyo-drift-3d-web/main/qa/kurogane-bay/sd1-dust-shotengai.png
- https://raw.githubusercontent.com/doublehidenblade/tokyo-drift-3d-web/main/qa/kurogane-bay/sd2-dust-hauler.png
- https://raw.githubusercontent.com/doublehidenblade/tokyo-drift-3d-web/main/qa/kurogane-bay/sd4-masked-street.png
- https://raw.githubusercontent.com/doublehidenblade/tokyo-drift-3d-web/main/qa/kurogane-bay/sd6-noren-dustflap.png
- https://raw.githubusercontent.com/doublehidenblade/tokyo-drift-3d-web/main/qa/kurogane-bay/v2a-lower-dust-street.png
- https://raw.githubusercontent.com/doublehidenblade/tokyo-drift-3d-web/main/qa/kurogane-bay/v2c-sky-elevator-terminal.png

---

## Rule Going Forward
**All future mocks get their Japanese strings pre-verified via the gemini-consult skill BEFORE generation.** The generation prompt must specify the exact verified Japanese strings and their placement. Image-gen models mangle text — iterate until text reads correctly, verified by opening the output. English appears ONLY in American-army-camp or international-port contexts.
