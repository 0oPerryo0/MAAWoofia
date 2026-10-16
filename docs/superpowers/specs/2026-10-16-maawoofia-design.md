# MaaWoofia — Design Spec

Date: 2026-10-16
Status: Draft, awaiting review

## 1. Purpose

Automate the daily routine of the mobile game **XXL Woofia** (Mega Games TRY) with
[MaaFramework](https://github.com/MaaXYZ/MaaFramework), built on
[MaaPracticeBoilerplate](https://github.com/MaaXYZ/MaaPracticeBoilerplate).

Success = the user opens the packaged UI (MFAAvalonia, bundled by the boilerplate CI),
ticks the tasks they want, presses start, and the whole daily routine completes on their
real account without manual input — or stops cleanly with a log + screenshot when
something unexpected happens.

## 2. Scope

### In scope (v1)

The eleven tasks in §6, run in that order by "run all".

### Out of scope (v1)

- Actually playing battles (only ticket skip is used).
- Spending premium currency, paid gacha, purchases of any kind.
- The Google Play build (see §3) — kept addable, not built.
- Any modification of the game client, memory reading, traffic interception, or
  bypassing encryption / anti-cheat.

## 3. Platform and target build

| Item | Decision |
|---|---|
| Controller | ADB |
| Primary device | BlueStacks (`C:\Program Files\BlueStacks_nxt`, adb at `HD-Adb.exe`), ADB enabled in BlueStacks settings |
| Secondary device | Physical Android phone over USB ADB — same controller, only the device address differs; no extra pipeline work |
| Target build | **Official APK** (uncensored, adult) — the user's progressed account lives here |
| Other build | Google Play (censored, separate accounts). Not targeted in v1; likely shares the same menus, so it can later be added as a "Game version" option that only changes the package StartUp launches |
| Emulator resolution | Landscape 16:9 (1280×720 or 1920×1080). Pipelines are authored at the MaaFramework 720p baseline |
| UI language | Traditional Chinese, with some English art assets |

The user installs the official APK in BlueStacks after this spec is approved.

## 4. Architecture

**Approach A — pipeline-first, hybrid recognition, small Python agent.**

- Nearly all logic lives in MaaFramework pipeline JSON (debuggable in MaaDebugger /
  the Maa VSCode extension).
- A small Python agent (boilerplate `agent/` folder) only for logic the pipeline cannot
  express cleanly: the interest-answer lookup for the guessing game.
- StageSkip repeat counts use the pipeline v5 `max_hit` field, set from a UI input option;
  no agent code needed.

### Recognition strategy

| Target | Method |
|---|---|
| Buttons / labels with clean text (領取, 免費, 跳過, 確認, mission names) | OCR, always restricted by `roi` |
| Numbers (ticket count, stamina) | OCR (digits) |
| Icons with no text (red dot, mail, close X, back arrow) and English art | TemplateMatch |
| Enabled vs greyed-out buttons | ColorMatch |
| Ambiguous buttons that appear in several places | Template + nearby OCR confirmation |

OCR model: the boilerplate's PP-OCR small model (`assets/resource/model/ocr/`,
not committed, supplied by CI).

## 5. Project layout

Created from the boilerplate via GitHub "Use this template", cloned into
`C:\Users\Perry\Desktop\MAAWoofia`.

```
assets/
  interface.json                 # controller, resource, agent, tasks, options
  resource/
    pipeline/
      common.json                # GoHome, ClosePopup, ConfirmDialog, NetworkRetry
      startup.json
      sausage_stamina.json
      shop_free.json
      affection.json             # AffectionClaim + AffectionBonus + guessing game
      guild.json                 # GuildCheckIn + GuildMissions
      free_gacha.json
      daily_missions.json
      stage_skip.json
    image/
      common/ startup/ sausage/ shop/ affection/ guild/ gacha/ missions/ stage/
    model/ocr/                   # git-ignored
agent/
  main.py                        # registers custom actions/recognitions
  interest_guess.py
  data/interests.json            # character -> interests answer table
dev/                             # git-ignored: raw screenshots, asset-dump output
docs/superpowers/specs/          # this spec
```

## 6. Tasks

Every task begins with `GoHome` (§7). Each is a separate checkbox in the UI.

| # | Task | Behaviour | Done when | Options |
|---|---|---|---|---|
| 1 | **StartUp** | Launch the game package (or foreground it), tap through title, dismiss announcements / banners / login-bonus popups | Home-screen anchor detected | — |
| 2 | **SausageStamina** | Open the 香腸人 stamina minigame, choose the **random** reward (not the fixed 50), collect result | Reward collected or minigame already used today | — |
| 3 | **ShopFree** | Open shop, claim every item priced free / 免費 across the relevant tabs | No free item left | — |
| 4 | **AffectionClaim** | Open the affection room, claim accumulated affection | Claimed or nothing to claim | — |
| 5 | **AffectionBonus** | Pick the user-selected monthly-card character for extra affection. If the interest-guessing card game appears, answer via the table (§6.1) | Bonus used for today | `bonus_character`: dropdown of the user's monthly-card characters |
| 6 | **GuildCheckIn** | Open guild, check in | Checked in or already done | — |
| 7 | **GuildMissions** | Claim all claimable guild mission rewards | No claimable reward left | — |
| 8 | **FreeGacha** | Open gacha, do the daily free pull | Pull done or no free pull available | — |
| 9 | **DailyMissions** | Claim daily missions, then the 100-point daily chest; claim the weekly chest only if claimable | Nothing claimable left | — |
| 11 | **PartTime** | Open 打工, claim finished part-time jobs, send characters out again | Nothing to claim and no idle slot left | — (added 2026-10-17 at user request) |
| 12 | **FriendPoke** (optional, off by default) | Open 好友, poke every friend | Every friend poked | — (added 2026-10-17 at user request) |
| 10 | **StageSkip** | Ticket-skip farming in the chosen categories | Target count reached **or** tickets/stamina exhausted | `categories`: any of Event / Hard / Coin / EXP; per category a stage choice and `count` (number or "max") |

### 6.1 Interest-guessing game

- `agent/data/interests.json` maps character name → list of interests.
- The custom recognition reads the character name and the offered cards by OCR,
  picks the card matching a known interest.
- Unknown character or no match → pick randomly and log the character + options so the
  table can be extended.
- Seeded from read-only static asset analysis (§9) where possible, otherwise filled by
  observation.

## 7. Shared behaviour and safety

- **GoHome**: press back / close popups until the home anchor appears (bounded attempts).
- **Popup handling**: announcements, level-up, event banners are closed via interrupt-style
  nodes available from any task.
- **NetworkRetry**: reconnect / network-error dialogs → tap retry.
- **Timeouts**: a node that does not find its expectation within ~20 s fails the task with
  a log line and screenshot; never taps blindly.
- **Spend guard (hard rule)**: no node may tap a confirmation that spends premium currency
  or paid items. FreeGacha only taps a pull button whose OCR reads 免費 (or the free
  marker); otherwise it backs out. Shop only taps items whose price reads free.

## 8. Content handling

The target build contains explicit adult imagery. To keep the repo and releases safe to
share:

- Raw full screenshots live only in git-ignored `dev/screens/`; never committed or shipped.
- Templates are crops of UI elements only (buttons, icons, text, markers) — never
  character art.
- Screens featuring characters are recognised by UI elements and OCR text only.
- Interaction scenes are skipped / fast-forwarded; only the skip control is mapped.

## 9. Static asset analysis (optional, read-only)

Purpose: seed `interests.json`, collect exact UI strings and stage names.

- Prefer the Google Play APK's data tables (censored build); fall back to the official
  APK's data tables only if needed.
- Extract data assets only (TextAsset / JSON / ScriptableObject-style tables); do not
  extract textures.
- No repacking, patching, or decryption. If tables are encrypted, stop and fill the table
  by observation instead.
- Output goes to git-ignored `dev/asset-dump/`.
- The user accepts the ToS risk of data-mining and automation for their account.

## 10. Development workflow

1. User creates the repo from the template on GitHub; it is cloned into the project folder.
2. User installs the official APK in BlueStacks, enables ADB, logs in.
3. Optional asset analysis (§9).
4. Per task, in the order of §6: the user describes the flow, screenshots are taken over
   ADB, templates cropped, pipeline nodes written, then the task is run end to end.
5. Discovered facts — package names, exact screen flows, stage lists, monthly-card
   characters — are recorded in the pipelines and `interface.json` as they are found.

## 11. Testing

- Each task is run end to end on BlueStacks (MaaPiCli or the MaaFramework Python
  binding), from both the home screen and a non-home screen to exercise `GoHome`.
- "Already done today" path is checked for every daily task (second run must be a no-op).
- StageSkip checked with a small count and with "max" until tickets/stamina run out.
- FreeGacha spend guard checked by running it after the free pull is used: it must back
  out without pulling.
- A task is only considered done after a clean run with logs reviewed.
