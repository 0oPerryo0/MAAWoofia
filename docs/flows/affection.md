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

# AffectionBonus (進去玩他) flow

One free use per day; afterwards the game asks 「可抽牌次數不足，是否直接消耗…後進行抽牌？」 → always 取消.
Options: `bonus_slot` (room 1/2/3, 3 = monthly card) and `bonus_character` (who is in that room).

Character states (user):
- **Skin unlocked** (3 yellow-border cards): button 加速培慾 → bonus affinity, maybe level-up / CG popups.
- **Skin locked**: button 抽牌 → card game, 3 rounds (第1/2/3回合). Each round draws 3 cards; pick one, 確定.
  Correct picks turn yellow and stay; wrong picks leave the deck (卡片 N shows deck size).

Per round (`agent/interest_guess.py`, custom action `interest_round`): tap each card and OCR its name
(`InterestGuess_CardName`) → pick a card in the character's list (`agent/data/interests.json`) → else a
yellow-border card → else the middle unknown card. Then 確定 and one tap to skip the animation.

`interests.json`: 50 characters × 3 cards from forum.gamer.com.tw bsn=80107 snA=1014 (edited
2026-10-07), names checked against the game's 培慾卡片名稱表 / 角色名字表 (fixed 打屁股→打屁鼓,
．→‧ in two names, 祟→崇).

| Screen | Identified by | Action |
|---|---|---|
| HOOK-UP list | OCR `進去玩他` in the slot roi | tap |
| Room, skin locked | `^抽牌$` `[280,1185,120,55]` | tap |
| Room, skin unlocked | `加速培慾` `[130,1185,330,55]` | tap |
| No free use | `次數不足` `[100,560,520,70]` | tap 取消 `[190,695,140,50]` |
| Round N | `第.?N.?回合` `[230,440,260,90]` | `interest_round`, then tap (330,280) |
| Dialogue / popups | — | tap (330,280), ≤40 |
| Room idle (after round 3) | `^卡` `[10,895,130,45]` + `抽牌\|加速培慾` | go home |

Manual (2026-10-17): tiger room, deck 28 → 25 after 3 wrong picks (對坐, 鬥劍, 試香 — tiger is 白威).
Live: free use spent → 抽牌 → prompt cancelled → home ✓ 40 s. **Pending:** full card game at next 05:00.
