# AffectionClaim (培慾 → 契合度結算) flow

Affinity accrues in **5-minute chunks** while characters sit in the HOOK-UP room (cap 8 h ≈ +28,800 each).

| Screen | Identified by | Action |
|---|---|---|
| Home | `HomeAnchor` | tap 培慾 button `[110,1160,170,70]` (OCR of 培慾 is unreliable) |
| HOOK-UP, claimable | OCR `契合度結算` + ColorMatch yellow (245,217,64) in `[375,1185,160,55]` | tap |
| HOOK-UP, nothing yet (<5 min) | same OCR, button grey (129,125,124) | go home, done |
| 夥伴契合度結算 popup | `點擊.*關閉` `[0,870,720,90]` | tap |
| Level-up popup; Lv1–3 also "new story unlocked" (user) | not yet captured | `ClosePopup`, else Back ×≤6 (`Affection_DismissPopup`) |

Other controls: 進去玩他 per slot (Task 8), 培慾配置 (configure slots). Third slot locked.

Replay: yellow → settle HIT (445,1215) · grey → MISS · popup closed · open from home ✓.
Live (2026-10-17): nothing to settle → home ✓ 20 s. Manual settle +28,800 ×2.
**Pending:** capture real level-up / story popups (lion Lv4 at 298,500/300,000).
