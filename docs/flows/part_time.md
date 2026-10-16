# PartTime (打工) flow

Jobs last 10 h; the job list resets daily at 05:00. The refresh button (top-right) is never tapped.

| Screen | Identified by | Action |
|---|---|---|
| Home | `HomeAnchor` + OCR `^打工$` in right column | tap icon |
| Finished jobs | 一鍵領取 `鍵領取` + yellow `[370,1180,170,60]` | tap, close reward popup |
| Idle jobs | 一鍵打工 `鍵打工` + orange (243,123,36) `[185,1180,170,60]` | tap |
| 一鍵打工 dialog (game auto-assigns partners) | title `一鍵打工` + button `^打工$` `[385,1010,150,50]` | tap 打工 |
| Nothing to do | both buttons grey | go home, done |

Replays all as expected. Live (2026-10-17): manual claim + dispatch; task after → done → home ✓ 20 s.
