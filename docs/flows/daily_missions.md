# DailyMissions (任務 → 每日／每週) flow — always the LAST task of the daily run

一鍵領取 claims finished missions only. Activity chests must be collected by tapping the **glowing**
progress bar once (user): daily only when the **100** chest glows (one tap collects all), weekly when
**any** chest glows.

| Screen | Identified by | Action |
|---|---|---|
| Home | `HomeAnchor` + OCR `^任務$` in right column | tap icon |
| QUEST tabs | `每日任務` `[30,1105,180,55]` / `每週任務` `[270,1105,180,55]` | tap |
| Claimable | OCR `鍵領取` + ColorMatch yellow `[275,1180,170,60]` | tap, close popup, repeat |
| Daily chests | ColorMatch green halo (G>120, R<120, ≥130 px) above the 100 chest `[535,300,70,18]` | tap chest, close popup |
| Weekly chests | same halo check per chest (x ≈ 235/320/405/490/570), `Or` | tap first glowing chest, close popup, repeat |
| Nothing claimable | `鍵領取`, grey | daily → weekly → home |

Chest states: glowing (halo + sparkles, ≈176–270 halo px) = claimable; flat green = collected; white = not reached
(both ≈66–70 halo px).

## Daily missions (15 points each)

| Mission | Covered by |
|---|---|
| 登入1次 | StartUp |
| 完成公會簽到1次 | Guild |
| 在任意市集購買商品1次 | ShopFree |
| 進行召喚1次 | FreeGacha |
| 結算培慾契合度1次 | AffectionClaim |
| 在培慾室「進去玩他」1次 | AffectionBonus |
| 消耗能量60點 | StageSkip |
| 通過任意主線／困難／挑戰關卡1次 | StageSkip — ticket skips count (user), **event stages do not** |
| 進化任意夥伴1次 | not automated |

Built tasks so far reach 75; AffectionBonus + StageSkip bring it to ≥100.

Correction (2026-10-17): the glowing 20–100 chests after claim-all were *not* collected until the bar was
tapped. Replays: daily glowing → HIT (571,332); collected / unreached → MISS. Weekly glowing → HIT;
collected / unreached → MISS. Live: weekly chest collected by the task ✓ 57 s.

Weekly (2026-10-17): 250 points, 200 chest opened; e.g. 登入5次, 完成公會簽到5次, 消耗能量1000點, 通過任意主線關卡30次.

Live: manual claim-all (5 missions, chests 20/40/60); task run after → nothing left → home ✓ 24 s.
