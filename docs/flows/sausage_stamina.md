# SausageStamina (香腸伯) flow

Claim windows: **05:00–17:00** and **17:00–05:00**, one claim each. Run the task once per window.

| Screen | Identified by | Action |
|---|---|---|
| Home, claim available | 香腸伯 label in right icon column (OCR, roi `[500,250,220,420]`) | tap icon (label −30 px) |
| Home, already claimed | Icon absent (column reflows) + `HomeAnchor` | done |
| Help overlay (2 pages) | OCR `可選擇直接領取` `[110,900,500,60]` | Back (tap outside does not close) |
| Event screen | Buttons 直接領香腸 (+50) at (240,1134), **擲骰拚一波** (+20~180) at (480,1134) | tap **擲骰拚一波** — never the fixed 50 |
| Dice animation → reward popup (點擊空白處關閉) → result screen | OCR `獲得能量` `[200,920,320,80]` | Back until event screen |
| Event screen, claimed | OCR `已完成香腸領取` (目前非活動時間或已完成香腸領取) | go home, done |

Energy may exceed the cap (observed 160/120).

Live runs (2026-10-17): already claimed, from home ✓ 8 s · from Profile ✓ 11 s.
Claim path walked manually (dice 4+1+3 → +40); **automated claim run pending the 05:00 window**.
