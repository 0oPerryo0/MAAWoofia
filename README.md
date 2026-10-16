<!-- markdownlint-disable MD033 MD041 -->
<p align="center">
  <img alt="LOGO" src="https://cdn.jsdelivr.net/gh/MaaAssistantArknights/design@main/v1/icons/maa-logo_512x512.png" width="256" height="256" />
</p>

<div align="center">

# MaaWoofia

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white">
  <img alt="platform" src="https://img.shields.io/badge/platform-Windows-blueviolet">
  <img alt="Android" src="https://img.shields.io/badge/device-Android%20(ADB)-3DDC84?logo=android&logoColor=white">
  <img alt="license" src="https://img.shields.io/badge/license-MIT-green">
</p>

XXL Woofia 每日日常自動化小幫手 · 由 [MaaFramework](https://github.com/MaaXYZ/MaaFramework) 強力驅動

覺得好用的話，歡迎點個 Star ⭐

</div>

## 功能列表

- **啟動遊戲**
  - 自動開啟遊戲、略過片頭、點擊 TAP TO START 並回到主畫面
  - 遊戲停在其他頁面時會自動返回主畫面
- **香腸伯體力**
  - 每個時段（05:00、17:00）領取一次
  - 一律選擇「擲骰拚一波」（+20～180），不選固定 50
- **市集免費領取**
  - 每日市集中有 FREE 角標且限購尚未用完的商品
  - 購買視窗會再次確認總價為 0 才按下購買
- **培慾契合度結算**
  - 「契合度結算」按鈕為黃色時自動結算
  - 自動關閉等級提升、劇情解鎖等提示
- **公會簽到與任務**
  - 進入公會即完成簽到
  - 公會任務有可領取的獎勵時一鍵領取（簽到人數不足時自動略過）
- **每日免費單抽**
  - 只在「1 回召喚」顯示 Free 時抽一次
- **打工領取與派遣**
  - 一鍵領取完成的打工，再一鍵派遣
- **培慾額外好感（進去玩他）**
  - 每日免費一次，可選擇房間（第 3 間需月卡）與角色
  - 造型已解鎖：直接加速培慾
  - 造型未解鎖：自動進行卡牌遊戲，依角色喜好表選擇正確卡牌，其次選黃框卡牌
- **掃蕩關卡**
  - 主線、困難：自行輸入關卡（如 `11-36`、`11-4`）與次數
  - 觀光工坊：開啟「推薦」後掃蕩當日開放的最高等級，用完次數
  - 剩餘體力：可選擇保留或全部用於主線關卡
- **好友頂一下**（選用）
  - 追蹤清單中的每位好友頂一下
- **領取每日／每週任務**
  - 一鍵領取任務獎勵
  - 每日活躍：100 寶箱發光時點擊進度條一次領取全部
  - 每週活躍：任一寶箱發光就領取

## 使用說明

1. 在 BlueStacks 中開啟 **Android 偵錯橋（ADB）**（設定 → 進階），解析度設為 1280×720（遊戲為直向畫面）。
2. 安裝 Python 3.11 以上，並執行 `pip install maafw==5.14.3`（培慾卡牌遊戲、關卡導航、好友頂一下需要）。
3. 從 [Releases](https://github.com/0oPerryo0/MAAWoofia/releases) 下載對應平台的壓縮檔，解壓後開啟 MFAAvalonia。
4. 選擇裝置，勾選需要的任務後開始執行。**「領取每日／每週任務」請放在最後。**

> [!IMPORTANT]
> 主線與困難關卡預設為空白（會略過）。每日任務需要主線、困難、挑戰各掃蕩一次，
> 請先在「掃蕩關卡」選項中填入自己已三星通關的關卡，每日活躍才會達到 100。

各任務的畫面流程與判斷方式請見 [`docs/flows/`](./docs/flows/)。
回報問題時，請附上程式資料夾內 `debug` 資料夾中的日誌與出錯時的截圖。

### 安全原則

- 召喚只點顯示 **Free** 的單抽，**永遠不點 11 回召喚**（鈴鐺抽卡沒有二次確認）。
- 市集只領取 FREE 且價格為 0 的商品。
- 任何「…不足」「是否消耗…」等提示一律按 **取消**，不花虹石或道具。

## 開發相關

本專案基於 [MaaPracticeBoilerplate](https://github.com/MaaXYZ/MaaPracticeBoilerplate) 開發，
Pipeline 寫法與自訂動作請參考 [MaaFramework 文件](https://github.com/MaaXYZ/MaaFramework/tree/main/docs)。

```bash
pip install -r requirements.txt
python tools/dev/run_task.py StartUp    # 對模擬器執行單一任務
python -m pytest tests                  # 單元測試
```

- 設計與開發計畫：[`docs/superpowers/`](./docs/superpowers/)
- 開發工具（截圖、裁切、離線辨識檢查、OCR 傾印）：[`tools/dev/`](./tools/dev/)
- 原始截圖與資料表傾印放在 `dev/`（已加入 .gitignore，請勿提交；遊戲含成人內容）

## 免責聲明

本專案只「看畫面、點按鈕」，不修改遊戲、不讀取記憶體、不攔截封包。
使用自動化工具可能違反遊戲服務條款，帳號風險請自行評估。本專案與遊戲官方無任何關係。

## 鳴謝

- [MaaFramework](https://github.com/MaaXYZ/MaaFramework)：自動化框架
- [MaaPracticeBoilerplate](https://github.com/MaaXYZ/MaaPracticeBoilerplate)：專案模板
- [MFAAvalonia](https://github.com/SweetSmellFox/MFAAvalonia)：通用圖形介面
- 巴哈姆特 XXL Woofia 板的玩家們：培慾卡牌角色喜好整理（[原文](https://forum.gamer.com.tw/C.php?bsn=80107&snA=1014)）

### 貢獻者

感謝所有參與開發的朋友！

[![Contributors](https://contrib.rocks/image?repo=0oPerryo0/MAAWoofia&max=1000)](https://github.com/0oPerryo0/MAAWoofia/graphs/contributors)

## 聯絡我們

遇到問題或有建議，請先到 [Issues](https://github.com/0oPerryo0/MAAWoofia/issues) 回報。
