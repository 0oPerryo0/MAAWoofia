# MaaWoofia Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** A MaaFramework project that runs XXL Woofia's ten-step daily routine on BlueStacks (official APK, real account) from the MFAAvalonia UI.

**Architecture:** Repo created from MaaPracticeBoilerplate. Pipeline JSON (one file per task + `common.json`) does all screen logic with OCR / TemplateMatch / ColorMatch; a Python AgentServer adds only the interest-guess recognition. Small dev scripts capture screens, crop templates and run single tasks against the emulator.

**Tech Stack:** MaaFramework 5.x pipeline v5 + ProjectInterface v2, Python 3.13 with `maafw==5.14.3`, Pillow, pytest, `@nekosu/maa-tools` (checker), BlueStacks `HD-Adb.exe`.

**Spec:** `docs/superpowers/specs/2026-10-16-maawoofia-design.md`

## Global Constraints

- Python package pinned: `maafw==5.14.3` (in `requirements.txt` at repo root).
- Controller: ADB only. ADB binary default `C:\Program Files\BlueStacks_nxt\HD-Adb.exe`, serial default `127.0.0.1:5555`; both overridable via env `MAA_ADB_PATH` / `MAA_ADB_SERIAL`.
- Coordinate space: 1280×720 landscape (MAA `display_short_side` 720). All `roi`/`target` values and templates are in this space.
- Templates are crops of UI elements only — never character art. Raw screenshots and asset-dump output live only under git-ignored `dev/`.
- Spend guard: no node taps anything that spends premium currency or paid items. Gacha pulls and shop items are only tapped when OCR in the button/price `roi` reads `免費`.
- Node naming: task entry = task name (`StartUp`, `SausageStamina`, `ShopFree`, `AffectionClaim`, `AffectionBonus`, `GuildCheckIn`, `GuildMissions`, `FreeGacha`, `DailyMissions`, `StageSkip`); internal nodes `<Task>_<Step>`; shared nodes in `common.json` have no prefix.
- Node `timeout` stays at the MaaFramework default (20000 ms) unless a step's live test shows a longer load.
- UI strings in `interface.json` labels are Traditional Chinese.
- Nothing is pushed or tagged without the user's explicit go-ahead.

## Review Focus

1. Back pressed on the home screen opens an "exit game?" dialog — `GoHome` must cancel it, never confirm (test in Task 3).
2. Second run of any daily task on the same day must succeed as a no-op, not fail or tap stale buttons (test case in every game task via the Mapping Procedure).
3. FreeGacha after the free pull is used: a paid pull button sits where the free one was — the task must back out without tapping (test in Task 9).
4. StageSkip running out of stamina/tickets opens a "buy with gems?" dialog — must cancel and finish successfully (test in Task 11).
5. Emulator not running or wrong ADB serial — `run_task.py` must exit non-zero with a message naming the serial, not hang (test in Task 2).

---

## Mapping Procedure (used by Tasks 3–11)

Every game task follows the same steps; each task below lists only what is specific to it.

1. **Walk-through:** the user describes the flow from the home screen; for each screen run `python tools/dev/screencap.py <task>_<nn>` and the user performs the tap, until the flow ends.
2. **Flow note:** write `docs/flows/<task>.md` — one line per screen: screenshot name, what identifies it, what is tapped, which recognition (OCR text / template / color) per the spec §4 table.
3. **Templates:** `python tools/dev/crop.py dev/screens/<shot>.png x y w h assets/resource/image/<folder>/<name>.png` for each icon; record the printed `roi` (crop box padded by 20 px, clamped to the screen) in the node.
4. **Pipeline:** write the task's nodes in its pipeline file using the entry name from Global Constraints. The entry's `next` is `["<Task>_<FirstStep>", "[JumpBack]GoHomeStep"]` so it always starts from home. Every waiting node lists `[JumpBack]ClosePopup` and `[JumpBack]NetworkRetry` after its real successors.
5. **Static check:** `npx @nekosu/maa-tools check` → no errors; `python tools/validate_schema.py --schema-dir deps/tools --resource-dirs assets/resource --interface-files assets/interface.json` → exit 0.
6. **Live runs** (`python tools/dev/run_task.py <Entry>`): (a) from the home screen, (b) from some other menu, (c) immediately again (already-done → succeeds, no rewards claimed). Each must print `SUCCEEDED`; review the log and the last screenshot. Plus the task's own cases.
7. **Commit:** `git add assets docs/flows && git commit -m "feat: <Task> task"`.

---

### Task 1: Bootstrap repo from the template

**Files:**
- Create (via template): whole boilerplate tree in `C:\Users\Perry\Desktop\MAAWoofia`
- Create: `requirements.txt`
- Modify: `assets/interface.json`, `.gitignore`
- Delete: `assets/resource/pipeline/my_task.json`, `agent/my_action.py`, `agent/my_reco.py`, `assets/resource/image/empty.png`

**Interfaces:**
- Produces: `interface.json` with one controller `"name": "Android (ADB)"`, one resource `"name": "官方 APK"` (path `./resource`), `agent` `{ "child_exec": "python", "child_args": ["./agent/main.py"] }`, empty `task` list; `agent/main.py` unchanged apart from imports.

- [ ] **Step 1:** User clicks "Use this template" on MaaPracticeBoilerplate → new repo `MaaWoofia`. Clone it into the scratchpad and move its contents (including `.git`) into the project folder, keeping the existing `docs/superpowers/`.
- [ ] **Step 2:** `git submodule update --init` and `npm ci`; `python tools/configure.py` → prints `OCR model configured.` and `assets/resource/model/ocr/` holds `det.onnx`, `rec.onnx`, `keys.txt`.
- [ ] **Step 3:** Write `requirements.txt` (`maafw==5.14.3`, `json-with-comments`, `pillow`, `pytest`) and `pip install -r requirements.txt`.
- [ ] **Step 4:** Edit `interface.json` per Interfaces (name `MaaWoofia`, `github` = the new repo URL, description/welcome in Traditional Chinese, remove Win32 controller and B 服 resource and all sample tasks/options); delete the sample files listed above; remove their imports from `agent/main.py`; append `dev/` to `.gitignore`.
- [ ] **Step 5:** Static check (Mapping Procedure step 5) → both pass.
- [ ] **Step 6:** Commit spec, plan and bootstrap: `git add -A && git commit -m "chore: bootstrap MaaWoofia from boilerplate"`.

### Task 2: Dev tooling (screencap, crop, single-task runner)

**Files:**
- Create: `tools/dev/adb.py`, `tools/dev/screencap.py`, `tools/dev/crop.py`, `tools/dev/run_task.py`
- Test: `tests/test_crop.py`, `tests/test_adb.py`

**Interfaces:**
- Produces:
  - `adb.py`: `adb_path() -> str`, `adb_serial() -> str` (env overrides, defaults from Global Constraints).
  - `screencap.py <name>` → saves `dev/screens/<name>.png`, resized so the short side is 720.
  - `crop.py`: `crop_template(src: Path, box: tuple[int,int,int,int], out: Path) -> tuple[int,int,int,int]` returns the padded roi; CLI prints `roi: [x, y, w, h]`.
  - `run_task.py <Entry> [--no-agent]` → loads `assets/resource`, connects `AdbController(adb_path(), adb_serial(), …)`, starts `agent/main.py` via `AgentClient` unless `--no-agent`, runs the entry, prints `SUCCEEDED`/`FAILED`, exit code 0/1.

- [ ] **Step 1: Write failing tests**

```python
# tests/test_crop.py
def test_crop_returns_padded_roi(tmp_path):  # 1280x720 source, box (100,100,50,40)
    assert crop_template(src, (100, 100, 50, 40), tmp_path/"t.png") == (80, 80, 90, 80)
    assert Image.open(tmp_path/"t.png").size == (50, 40)

def test_crop_roi_clamped_to_screen(tmp_path):
    assert crop_template(src, (0, 0, 30, 30), tmp_path/"t.png") == (0, 0, 50, 50)

def test_crop_rejects_box_outside_screen(tmp_path):
    with pytest.raises(ValueError):
        crop_template(src, (1270, 700, 50, 50), tmp_path/"t.png")

# tests/test_adb.py
def test_serial_env_override(monkeypatch):
    monkeypatch.setenv("MAA_ADB_SERIAL", "emulator-5554")
    assert adb_serial() == "emulator-5554"

def test_serial_default(monkeypatch):
    monkeypatch.delenv("MAA_ADB_SERIAL", raising=False)
    assert adb_serial() == "127.0.0.1:5555"
```

- [ ] **Step 2:** `pytest tests -v` → FAIL (modules missing).
- [ ] **Step 3:** Implement `adb.py` and `crop.py` per Interfaces (Pillow; padding 20 px; clamp to 1280×720).
- [ ] **Step 4:** `pytest tests -v` → all PASS.
- [ ] **Step 5:** Implement `screencap.py` (`<adb> -s <serial> exec-out screencap -p`, resize with Pillow) and `run_task.py` (maafw 5.14.3 API: `Toolkit.init_option`, `Resource.post_bundle`, `AdbController.post_connection`, `AgentClient.bind/identifier/connect`, `Tasker.bind/post_task`). Connection failure prints `cannot connect to ADB device <serial>` and exits 1 within 30 s.
- [ ] **Step 6:** With BlueStacks stopped: `python tools/dev/run_task.py StartUp` → prints the serial error, exit 1 (Review Focus 5).
- [ ] **Step 7:** Commit `tools/dev tests requirements.txt` — `feat: dev tooling for screen capture, cropping and task runs`.

### Task 3: Device setup, shared nodes, StartUp

**Files:**
- Create: `assets/resource/pipeline/common.json`, `assets/resource/pipeline/startup.json`, `assets/resource/image/common/*`, `assets/resource/image/startup/*`, `docs/flows/startup.md`
- Modify: `assets/interface.json` (add task `StartUp`, label `啟動遊戲`, `default_check: true`)

**Interfaces:**
- Produces (`common.json`), used by every later task:
  - `HomeAnchor` — recognition only, hits only on the home screen.
  - `GoHomeStep` — `next: ["ClosePopup", "NetworkRetry", "ExitDialogCancel", "PressBack"]`; used as `[JumpBack]GoHomeStep`.
  - `ClosePopup` — closes announcement / banner / level-up popups (template close X, OCR `關閉`/`確認` in popup roi).
  - `NetworkRetry` — taps retry on network/reconnect dialogs.
  - `ExitDialogCancel` — on the "exit game?" dialog taps cancel.
  - `PressBack` — `ClickKey` keycode 4, `max_hit: 15`.

- [ ] **Step 1 (user):** Install the official APK in BlueStacks, set display to 1280×720 landscape, enable Settings → Advanced → Android Debug Bridge, log in. Note the ADB port shown there; export `MAA_ADB_SERIAL` if it is not 5555.
- [ ] **Step 2:** `"<adb>" -s <serial> shell pm list packages | grep -i woof` → record the package name in `startup.json` (`StartUp_Launch`: `"action": "StartApp", "package": "<pkg>"`).
- [ ] **Step 3:** Mapping Procedure for StartUp: title screen → login popups → home; define `HomeAnchor` from a home-only element.
- [ ] **Step 4:** Extra live cases: game force-stopped (cold start with banners); on home, press Back once so the exit dialog shows, then run → dialog cancelled, task SUCCEEDED (Review Focus 1).
- [ ] **Step 5:** Commit — `feat: shared navigation nodes and StartUp task`.

### Task 4: SausageStamina

**Files:** `pipeline/sausage_stamina.json`, `image/sausage/*`, `docs/flows/sausage_stamina.md`; interface task `SausageStamina`, label `香腸人體力`.

- [ ] **Step 1:** Mapping Procedure. The reward choice node taps the **random** option (OCR on its label), never the fixed-50 option.
- [ ] **Step 2:** Extra case: already played today → task SUCCEEDED without entering the minigame.
- [ ] **Step 3:** Commit — `feat: SausageStamina task`.

### Task 5: ShopFree

**Files:** `pipeline/shop_free.json`, `image/shop/*`, `docs/flows/shop_free.md`; interface task `ShopFree`, label `商店免費領取`.

- [ ] **Step 1:** Mapping Procedure, covering every shop tab the user says has free items. Item tap requires OCR `免費` in that item's price roi.
- [ ] **Step 2:** Extra case: a priced item next to a free one is never tapped (check log: only `免費` hits).
- [ ] **Step 3:** Commit — `feat: ShopFree task`.

### Task 6: AffectionClaim

**Files:** `pipeline/affection.json` (create), `image/affection/*`, `docs/flows/affection.md`; interface task `AffectionClaim`, label `領取好感度`.

- [ ] **Step 1:** Mapping Procedure. Screens with characters are identified by UI elements/OCR only.
- [ ] **Step 2:** Commit — `feat: AffectionClaim task`.

### Task 7 (optional): Read-only data-table analysis

**Files:**
- Create: `tools/dev/dump_tables.py`; output `dev/asset-dump/` (git-ignored); `agent/data/interests.json` seed if found.

- [ ] **Step 1:** After the game has downloaded all post-login resources, pull the raw files: every path from `adb shell pm path <pkg>` into `dev/apk/`, plus `/sdcard/Android/data/<pkg>` and `/sdcard/Android/obb/<pkg>` (if present) into `dev/asset-dump/raw/`. No root; if the tables turn out to live only in `/data/data/<pkg>`, stop and ask the user.
- [ ] **Step 2:** Identify the engine (e.g. Unity → `assets/bin/Data`). If Unity, `dump_tables.py` uses UnityPy to export only `TextAsset` and typetree-readable `MonoBehaviour` objects; it never reads `Texture2D`/`Sprite`.
- [ ] **Step 3:** Search the dump for interest/hobby tables and UI strings (`免費`, `跳過`, stage names). If found, write `agent/data/interests.json` as `{"<角色名>": ["<興趣>", …]}`.
- [ ] **Step 4:** If assets are encrypted or no table exists, stop; record that in `docs/flows/asset_analysis.md`. No decryption attempts.
- [ ] **Step 5:** Commit `tools/dev/dump_tables.py agent/data docs/flows` — `chore: interest table from data analysis`.

### Task 8: AffectionBonus + interest guess

**Files:**
- Modify: `assets/resource/pipeline/affection.json`, `agent/main.py` (import `interest_guess`)
- Create: `agent/interest_guess.py`, `agent/data/interests.json` (if Task 7 skipped: `{}`), `image/affection/*`
- Test: `tests/test_interest_guess.py`
- Interface: task `AffectionBonus`, label `月卡角色額外好感`, option `bonus_character` (`select`, one case per monthly-card character, each overriding `AffectionBonus_PickCharacter`'s OCR `expected`).

**Interfaces:**
- Produces: `pick_card(character: str, cards: list[str], table: dict[str, list[str]]) -> int | None` (index of the matching card); custom recognition `interest_guess` that OCRs `InterestGuess_Name` and each roi in `custom_recognition_param.card_rois`, calls `pick_card`, falls back to a random index, logs `unknown: <character> <cards>` on fallback, and returns that card's box.

- [ ] **Step 1: Write failing tests**

```python
TABLE = {"阿虎": ["釣魚", "烤肉"]}
def test_picks_matching_card():           assert pick_card("阿虎", ["唱歌", "烤肉", "跑步"], TABLE) == 1
def test_normalizes_whitespace_and_width(): assert pick_card(" 阿虎 ", ["釣 魚", "唱歌"], TABLE) == 0
def test_no_match_returns_none():          assert pick_card("阿虎", ["唱歌", "跑步"], TABLE) is None
def test_unknown_character_returns_none(): assert pick_card("小狼", ["釣魚"], TABLE) is None
```

- [ ] **Step 2:** `pytest tests/test_interest_guess.py -v` → FAIL.
- [ ] **Step 3:** Implement `pick_card` (normalize with `unicodedata.normalize("NFKC", s)` and strip all whitespace) and the `interest_guess` recognition.
- [ ] **Step 4:** `pytest tests -v` → PASS.
- [ ] **Step 5:** Mapping Procedure for AffectionBonus: pick the option's character, use the bonus, enter `InterestGuess` nodes when the guessing game appears.
- [ ] **Step 6:** Extra cases: guessing game appears → a card is chosen and the game finishes; a run where it doesn't appear → SUCCEEDED.
- [ ] **Step 7:** Commit — `feat: AffectionBonus with interest guessing`.

### Task 9: GuildCheckIn, GuildMissions, FreeGacha

**Files:** `pipeline/guild.json`, `pipeline/free_gacha.json`, `image/guild/*`, `image/gacha/*`, `docs/flows/guild.md`, `docs/flows/free_gacha.md`; interface tasks `GuildCheckIn` (`公會簽到`), `GuildMissions` (`公會任務`), `FreeGacha` (`免費抽卡`).

- [ ] **Step 1:** Mapping Procedure for GuildCheckIn, then GuildMissions (claim until no claimable reward remains).
- [ ] **Step 2:** Mapping Procedure for FreeGacha: the pull node is OCR `expected: "免費"` in the pull button roi; if it misses, `FreeGacha_Leave` backs out and the task succeeds.
- [ ] **Step 3:** Extra case (Review Focus 3): run FreeGacha after the free pull was used → no pull tapped (log shows `FreeGacha_Leave`), currency unchanged on screen.
- [ ] **Step 4:** Commit — `feat: guild and free gacha tasks`.

### Task 10: DailyMissions

**Files:** `pipeline/daily_missions.json`, `image/missions/*`, `docs/flows/daily_missions.md`; interface task `DailyMissions`, label `每日任務`.

- [ ] **Step 1:** Mapping Procedure: claim all daily missions, then the 100-point chest, then the weekly chest only when its claim state (ColorMatch/red dot) says claimable.
- [ ] **Step 2:** Extra case: weekly chest not claimable → skipped, task SUCCEEDED.
- [ ] **Step 3:** Commit — `feat: DailyMissions task`.

### Task 11: StageSkip

**Files:** `pipeline/stage_skip.json`, `image/stage/*`, `docs/flows/stage_skip.md`; interface task `StageSkip`, label `掃蕩關卡`.

**Interfaces:**
- Options: `skip_event`, `skip_hard`, `skip_coin`, `skip_exp` (`switch`, override `enabled` of `StageSkip_Event` / `_Hard` / `_Coin` / `_Exp`); per category a `select` of stages found during mapping (override that category's stage OCR `expected`); per category an `input` count (`pipeline_type: int`, default `999` = until out) overriding `max_hit` of that category's `<…>_DoSkip` node.

- [ ] **Step 1:** Mapping Procedure for each category, one at a time.
- [ ] **Step 2:** Extra cases: count 1 → exactly one skip; count 999 → runs until out; the "buy stamina/tickets?" dialog is cancelled and the task SUCCEEDED (Review Focus 4).
- [ ] **Step 3:** Commit — `feat: StageSkip task`.

### Task 12: Full-routine run and release prep

**Files:** Modify `assets/interface.json` (task order = spec §6, `default_check` true for tasks 1–9), `README.md` (setup: BlueStacks settings, `pip install -r requirements.txt`, Python required for the agent).

- [ ] **Step 1:** Run all ten tasks in order via MFAAvalonia from the CI build or `run_task.py` in sequence → every task SUCCEEDED; repeat once → all no-op SUCCEEDED.
- [ ] **Step 2:** Confirm `git ls-files dev` is empty and every image under `assets/resource/image` is a UI crop (visual review).
- [ ] **Step 3:** Commit — `docs: README and task order`.
- [ ] **Step 4 (user go-ahead required):** push, and `git tag v0.1.0 && git push origin v0.1.0` to trigger the release workflow.
