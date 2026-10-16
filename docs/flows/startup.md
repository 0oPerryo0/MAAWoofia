# StartUp flow

Screen space: **720x1280 portrait** (the game is portrait-only).

| Screen | Identified by | Action |
|---|---|---|
| Intro video | OCR `SKIP` at top-left `[0,60,180,70]` | tap it |
| Title | OCR `TAP TO START` `[100,1120,520,120]` | tap it |
| Home | `HomeAnchor`: OCR `出擊` `[280,1110,160,90]` + `培慾` `[100,1150,200,90]` | done |
| Back pressed on home | OCR `回到標題畫面` (提示 dialog) | tap 取消 `[190,700,140,50]` |

Home-screen buttons (center points): 香腸伯 (568,480) · 商城 (660,300) · 任務 (660,410) ·
推薦 (568,300) · 公會 (190,1083) · 夥伴 (540,1083) · 培慾 (190,1195) · 出擊 (360,1150) ·
召喚 (540,1195) · 市集 (150,995). Left bar: 公告 信箱 好友 圖鑑 背包 設定.

Notes
- Back closes sub-screens reliably; `GoHomeStep` relies on it.
- `adb shell input tap` does not land correctly in this portrait game on BlueStacks; use
  MaaFramework input (`tools/dev/act.py`).
- If nothing familiar appears within 60 s of launch (game left on a sub-menu), `StartUp_Recover`
  presses Back until home.
- Not yet observed: first-login-of-the-day popups (sign-in, announcements). `ClosePopup` is
  extended when they are captured.

Live runs (2026-10-17): from home ✓ 8 s · from Profile ✓ 77 s · exit dialog open ✓ 9 s · cold start ✓ 13 s.
