<!-- markdownlint-disable MD033 MD041 -->
<div align="center">

# MaaWoofia

XXL Woofia 每日自動化小幫手，基於 [MaaFramework](https://github.com/MaaXYZ/MaaFramework)。

</div>

> 本專案只「看畫面、點按鈕」，不修改遊戲、不讀記憶體、不攔截封包。
> 使用自動化工具可能違反遊戲服務條款，風險請自行評估。

## 支援範圍

- 遊戲：XXL Woofia 官方 APK（`com.nightfun.xxlwoofia`），繁體中文介面
- 平台：Android 模擬器（BlueStacks 測試）或 USB 連接的 Android 手機（ADB）
- 解析度：模擬器設為 1280×720（遊戲本身為直向 720×1280）

## 準備

1. BlueStacks：設定 → 進階 → 開啟 **Android 偵錯橋（ADB）**，記下連接埠（預設 `127.0.0.1:5555`）。
2. 安裝 Python 3.11 以上，並執行：

   ```bash
   pip install maafw==5.14.3
   ```

   （部分任務使用 Python agent：培慾卡牌遊戲、關卡導航、好友頂一下。）
3. 下載 Release，執行 MFAAvalonia，選擇裝置後勾選任務即可。

## 任務（依執行順序）

| 任務 | 說明 |
|---|---|
| 啟動遊戲 | 開啟遊戲、略過片頭、TAP TO START，回到主畫面 |
| 香腸伯體力（擲骰） | 每時段（05:00／17:00）一次，一律選「擲骰拚一波」 |
| 市集免費領取 | 每日市集中有 FREE 角標且價格為 0 的商品 |
| 培慾契合度結算 | 黃色「契合度結算」時領取（每 5 分鐘累積） |
| 公會簽到與任務 | 進入公會自動簽到，一鍵領取公會任務 |
| 每日免費單抽 | 只在「1 回召喚」顯示 Free 時抽 |
| 打工領取與派遣 | 一鍵領取 → 一鍵打工 |
| 培慾額外好感 | 每日免費一次：造型已解鎖 → 加速培慾；未解鎖 → 卡牌遊戲（依角色喜好表選牌） |
| 掃蕩關卡 | 主線／困難（自行輸入關卡，如 `11-36`、`11-4`）、觀光工坊（最高等級用完次數）、剩餘體力 |
| 好友頂一下（選用） | 每位好友每日一次 |
| 領取每日／每週任務 | **請放在最後**，一鍵領取並開啟活躍寶箱 |

### 選項

- **額外好感房間／角色**：選擇進去玩他的房間（第 3 間需月卡）與該房間角色，用於卡牌遊戲選對卡。
  角色喜好表：`agent/data/interests.json`（社群整理，已對照遊戲內卡牌名稱）。
- **掃蕩**：主線、困難可分別開關並輸入關卡與次數（次數 0 = 用到體力不足）；觀光工坊開關；剩餘體力保留或全部掃主線。
  > ⚠️ **主線與困難關卡預設為空白（會略過）**。每日任務需要主線、困難、挑戰各掃蕩一次，
  > 請先填入自己已三星通關的關卡（例：主線 `11-36`、困難 `11-4`），每日活躍才會達到 100。

## 安全原則

- 召喚只點顯示 **Free** 的單抽，**永不點 11 回召喚**（鈴鐺抽卡沒有二次確認）。
- 市集只領 FREE 且價格為 0 的商品；購買視窗再次確認總價為 0。
- 任何「…不足」「是否消耗…」提示一律按 **取消**，不花虹石或道具。

## 開發

- 開發流程與每個任務的畫面對照：`docs/flows/`
- 設計與計畫：`docs/superpowers/specs/`、`docs/superpowers/plans/`
- 開發工具：`tools/dev/`（截圖、裁切、單一任務執行、離線辨識檢查、OCR 傾印）

  ```bash
  pip install -r requirements.txt
  python tools/dev/run_task.py StartUp
  python -m pytest tests
  ```

- 原始截圖與資料表傾印放在 `dev/`（已加入 .gitignore，請勿提交；遊戲含成人內容）。

本專案基於 [MaaPracticeBoilerplate](https://github.com/MaaXYZ/MaaPracticeBoilerplate)。
