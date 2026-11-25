# NOTES — 24 November 2026 world news

Bounty: make.fun `news-image-20261124`, "Sum up 24 November's world news
in one image" ($100, entries close 2026-11-26 00:00 UTC).
Research dates: 2026-11-24 (verification file) and 2026-11-25 (ChessBase
result + two more Reuters stories). All six stories below were verified
against reporting dated 24 November 2026. No headline was invented.

## The six stories in the image

### 1. SPORT — World chess title match opens with a Berlin draw (lead story)
- Game 1 of the 2026 FIDE World Championship, Fondation Martin Bodmer,
  Cologny/Geneva: Javokhir Sindarov (White, challenger) vs D. Gukesh
  (Black, defending champion) drew 0.5-0.5 in 38 moves by threefold
  repetition. Gukesh played the Berlin Defence (3...Nf6). After 17
  moves he was about 50 minutes behind on the clock, having spent
  almost 37 minutes on 17...Bb4; after 21 moves he had 16 minutes to
  Sindarov's 47. Sindarov played 32.Bxh6 Kg8 33.Rg5 Kh7 34.Rh5 and the
  moves were repeated. Both players are 20: the youngest title match
  in history by average age. 14-game match, $2.5m prize fund.
- Sources:
  - ChessBase, 24 Nov 2026 —
    https://en.chessbase.com/post/world-championship-2026-1
  - ChessBase India, published 2026-11-24T19:34:58Z —
    https://chessbase.in/news/world-championship-2026-game-1-report

### 2. DISASTER — M5.6 quake shakes Nepal near Tibet border
- Magnitude 5.6 (Nepal centre) / 5.3 (EMSC, USGS, India NCS) quake,
  Taplejung, Koshi Province, near the Nepal-Tibet border, Tue 24 Nov
  07:17 local (01:32 UTC). Felt in India, Bhutan and Bangladesh. No
  casualties or major damage reported so far.
- Sources:
  - Nature World News, 24 Nov 2026 —
    https://www.natureworldnews.com/articles/74007/20261124/magnitude-56-earthquake-shakes-eastern-nepal-near-tibet-border.htm
  - Nepal UK, 24 Nov 2026 —
    https://nepaluk.com/front-news/uk/taplejung-earthquake-olangchung-gola-5-6
  - Reuters via EMSC, 24 Nov 2026 (M5.3)

### 3. CHINA — China probes Politburo member Chen Jining
- Shanghai party chief Chen Jining, a member of the Politburo, is
  under investigation for "suspected severe violations of discipline
  and laws", Xinhua said on Tuesday 24 Nov — the fourth member of the
  top leadership body to be probed since 2025 (after He Weidong, Zhang
  Youxia, Ma Xingrui). Chen, 62, is a former Tsinghua president,
  environment minister and Beijing mayor.
- Source:
  - Reuters, 24 Nov 2026 —
    https://www.reuters.com/world/china-investigates-politburo-member-chen-jining-xinhua-says-2026-11-24/

### 4. MIDDLE EAST — Riyadh tower hit in 'terrorist attack'
- The Saudi-led coalition fighting Yemen's Iran-aligned Houthis said
  on Tuesday 24 Nov that a skyscraper in Riyadh's financial district
  had been targeted by a "terrorist attack", handled by the competent
  authorities, no further details. Riyadh's tallest skyscraper,
  headquarters of the Saudi sovereign wealth fund, was struck this
  month in a Houthi aerial attack: material damage, no injuries. The
  Houthis hit Aramco's building in Riyadh on 8 November.
- Source:
  - Reuters, 24 Nov 2026 —
    https://www.reuters.com/world/middle-east/saudi-led-coalition-says-tower-riyadh-finance-district-targeted-by-terrorist-2026-11-24/

### 5. DIPLOMACY — Trump to meet NATO chief Rutte on Wednesday
- US President Donald Trump will meet NATO Secretary-General Mark
  Rutte on Wednesday in Palm Beach, Florida, the White House said on
  Monday; reported by Reuters Tue 24 Nov 03:48 UTC.
- Source:
  - Reuters, 24 Nov 2026 —
    https://www.reuters.com/world/china/trump-meet-nato-chief-mark-rutte-wednesday-white-house-says-2026-11-24/

### 6. MIGRATION — 175 migrants unaccounted for off Senegal
- Around 175 migrants are unaccounted for after contact was lost with
  a Europe-bound wooden pirogue that left Dakar around 9-10 November,
  local officials and a human rights group said on Tuesday 24 Nov.
  Some 175 were aboard, Yoff mayor Seydina Issa Laye said; NGO Action
  for Human Rights and Friendship said 172 were believed missing.
  Senegal's navy rescued 974 migrants on five pirogues on Monday.
- Source:
  - Reuters, 24 Nov 2026 —
    https://www.reuters.com/world/africa/around-175-migrants-unaccounted-after-contact-lost-with-boat-senegal-2026-11-24/

## What was deliberately left out
- Stories dated 21-23 Nov, however big: Nvidia reinstating Jensen
  Huang (Mon 23 Nov), COP31 ending without a pact (Sun 22 Nov),
  Russia's "open war" warning to Estonia (Mon 23 Nov), the Merkury
  sinking (Sun 22 / confirmed Mon 23 Nov), Verstappen's Las Vegas GP
  win (Sat 21 Nov). Aggregator "24 Nov headlines" pages recycle these
  under a 24 Nov dateline; their primary-source dates rule them out.
- The Ma death-sentence case: first published Mon 23 Nov by Gold Wall
  Press and widely reported Tue 24 Nov (CNN dated 24 Nov), but Reuters
  could not independently verify it, and its first publication was
  23 Nov, so it fails this image's date rule (happened or first
  reported on 24 Nov). Excluded, not used with a caveat.
- Game 2 of the chess match (Wed 25 Nov) is a 25 Nov story and does
  not belong in a 24 Nov image.

## Requirements checked
- `GET https://make.fun/api/competitions/news-image-20261124/requirements`
  (read 2026-11-24): harness `program/v1`, entrypoint `main.py` at repo
  root (Python 3.13, run as `python3 -P -s /bot/main.py`, no network,
  read-only repo at `/bot`, writable `/output`, env `MAKEFUN_OUTPUT_DIR`,
  60 s / 1 CPU / 512 MB, two runs must be deterministic); image at most
  1024x1024 and 1 MiB; repo must carry an OSI-approved LICENSE, a README
  with the three live make.fun badges, and the entry needs a public
  GitHub repo + Solana wallet + transcript bundle at submission time.
- Judge: z-ai/glm-5.3-flash, no news feed, not told the day — the image
  names the day it sums up ("TUESDAY - 24 NOVEMBER 2026").
- Local verification: `python3 main.py` twice gives byte-identical
  output/entry.png, 1024x1024, 21,786 bytes
  (sha256 feed2426a97a8047067c25c147415a0c50dd8bee14df0acd68678b8629f0793c).
