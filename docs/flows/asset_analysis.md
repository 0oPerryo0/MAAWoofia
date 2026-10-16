# Static asset analysis (read-only)

Build: `com.nightfun.xxlwoofia` 1.7.0, Unity 2022.3.62f2 (IL2CPP + HybridCLR hot update).
Tool: `tools/dev/dump_tables.py` (TextAsset / MonoBehaviour only, no textures). Output stays in git-ignored `dev/asset-dump/`.

## What is readable

- Downloaded resources live in `/sdcard/Android/data/com.nightfun.xxlwoofia/files/data/`
  (Addressables, UnityFS bundles with the engine version stripped from the header).
- `binarydata/localization-remote-string_*` — Unity Localization string tables, plain.
  zh-TW tables include 通用文字表, 商城文字表, 任務名稱表, 關卡名稱表, 角色名字表,
  培慾卡片名稱表 (94 guessing-game cards), 培慾正確/錯誤台詞表 (reaction lines).

## What is not

- `binarydata/main_data_assets_all_*.bundle` (game data tables, incl. which card each
  character wants) is encrypted — no UnityFS header. Per spec §9 we stop here; no decryption.

## Consequences

- `agent/data/interests.json` starts empty and is filled by observation (Task 8 logs
  `unknown: <character> <cards>` on every fallback guess).
- Card names from 培慾卡片名稱表 are known, so OCR'd card text can be checked against them.

## UI strings for pipelines (zh-TW, exact)

| Use | Text |
|---|---|
| Exit-game dialog | 是否離開遊戲？ (cancel = 取消) |
| Claim / claim all / claimed | 領取 / 一鍵領取 / 已領取 |
| Skip | 跳過 |
| Retry (network) | 重試 |
| Guild check-in / guild missions | 公會簽到, 簽到 / 公會任務 |
| Daily / weekly missions | 每日任務 / 每週任務 |
| Hard stages | 困難 |
| Daily reset | 每日05:00(UTC+8) |
