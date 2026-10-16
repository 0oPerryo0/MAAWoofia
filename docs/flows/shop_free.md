# ShopFree (市集 → 每日市集) flow

Free items change daily, so the **FREE badge** is the marker — never the item.

| Screen | Identified by | Action |
|---|---|---|
| Home | `HomeAnchor` + OCR `市集` `[110,965,120,55]` | tap |
| Market | tab OCR `每日市集` `[95,1200,100,45]` | tap tab (ensures daily tab) |
| Claimable free card | OCR `^FREE` in grid `[0,420,720,580]` **and** `限購：[1-9]` right of that badge | tap card (badge +55,+60) |
| Claimed free card | badge present, `限購：0/1`, 已售完 | skip |
| Purchase dialog | OCR `購買數量` + price digit `^[0oO]$` (`only_rec`, `[464,752,30,32]`) | tap 購買 |
| Purchase dialog, price ≠ 0 | `購買數量` only | tap 取消 — spend guard |
| Reward popup | `點擊.*關閉` | tap, look for more free cards |
| Nothing left | title `每日市集` | go home |

OCR notes: the lone price digit under a card is not detected by OCR (too small); the 虹石 icon is
read as a bullet and 0 as "o" — hence the 限購 check and the tight `only_rec` price roi.

Replay checks (`tools/dev/reco_check.py`): unclaimed card HIT · claimed card MISS · free dialog →
購買 · paid dialog (3 虹石) → buy MISS, 取消 HIT.
Live (2026-10-17): claimed walked manually (精華 ×50, 虹石 unchanged 173); task run after claim ✓ 24 s.
