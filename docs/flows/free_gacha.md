# FreeGacha (召喚 daily free single pull) flow

**Bell pulls have no confirmation dialog** (user). The only pull tap allowed is the 1-pull button
when it reads `Free`; the 11-pull is never a click target; no blind taps on summon screens.

| Screen | Identified by | Action |
|---|---|---|
| Home | `HomeAnchor` | tap 召喚 `[470,1160,150,70]` |
| Summon (opens on 常駐召喚) | 1-pull button: OCR `回召喚` `[115,895,140,60]` + `^Free$` `[250,900,95,45]` | tap the 回召喚 text (x≈172) |
| Pull animation | OCR `SKIP` top-left | tap |
| Result (has pull-again buttons!) | OCR `^關閉$` `[270,1180,180,60]` | tap 關閉 only |
| Summon, free used | title `召喚` + `回召喚`, no `Free` (button shows bell ×1) | go home, done |

PICK UP banner uses gold bells and has no free pull; summon reopens on 常駐召喚 regardless.

Replays: Free screen → HIT (172,920); used / result / PICK UP screens → MISS.
Live (2026-10-17): free pull done manually (bells 8 unchanged); task after → NoFree → home ✓ 22 s.
