# Guild (公會簽到＋公會任務) flow

Entering the guild performs the daily check-in automatically, so check-in and missions are one task.

| Screen | Identified by | Action |
|---|---|---|
| Home | `HomeAnchor` | tap 公會 `[110,1050,170,65]` |
| 公會簽到 popup (first entry of the day) | OCR `獎勵已放入背包` `[180,745,360,60]` | tap 確定 `[285,800,150,48]` |
| Guild main | OCR `公會任務` `[430,320,160,55]` | tap (icon above label) |
| 公會任務, claimable | OCR `鍵領取` + ColorMatch yellow `[275,1180,170,60]` | tap 一鍵領取 |
| Reward popup | `點擊.*關閉` | tap |
| Nothing claimable | `鍵領取`, button grey | go home, done |

Milestones depend on how many guild members checked in today (3/5/7/10/15…); a small guild may have
nothing claimable (grey button) — the task simply finishes, and a later run claims new milestones.
OCR reads the grey button as `鍵領取` (drops 一), hence the shorter pattern. Only one mission category (簽到).

Replays all as expected. Live (2026-10-17): after manual claim → home ✓ 31 s. Manual: check-in + claim all (50/60/70/80/90).
