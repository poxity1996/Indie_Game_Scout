# Indie Game Scout

基於 Python 的 Steam 遊戲數據篩選工具。

## 簡介
本專案透過 SteamSpy API 獲取數據，根據好評率與評論數量篩選特定標籤的遊戲，並產生 JSON 格式供網頁端顯示。

## 篩選條件
* 好評率 (Positive Rating): > 95%
* 評論總數 (Total Reviews): 300 - 2000
* 價格 (Price): 排除免費遊戲
* 過濾清單 (Blacklist): 排除不符合特定類型的關鍵字

## 資料夾結構
* /public: 存放前端靜態資源 (HTML, CSS, JS)
* scout.py: 數據獲取與處理程式
* .gitignore: 版本控制排除清單

## 執行方式
1. 啟動環境並安裝必要套件：pip install requests。
2. 執行數據更新程式：執行 python scout.py 更新數據。
3. 開啟本地網頁伺服器：cd 進入 public 目錄並執行 python -m http.server 8000。
4. 使用瀏覽器訪問：http://localhost:8000