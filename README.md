# 📚 Project Gutenberg 中文書籍爬蟲

本專案為一個針對 [Project Gutenberg](https://www.gutenberg.org/browse/languages/zh) 中文書籍的網頁爬蟲，能夠自動擷取最多 200 本書的標題與內容，並依書名儲存為純文字檔案。每本書的段落以 `---` 分隔，利於後續 NLP 分句或語意分析處理。

---

## 🧠 技術應用與邏輯思維

### 📌 技術堆疊

| 類別       | 技術名稱        | 說明                                       |
|------------|-----------------|--------------------------------------------|
| 爬蟲工具   | `requests`      | 發送 HTTP 請求取得原始 HTML                |
| HTML解析器 | `BeautifulSoup` | 使用 `lxml` 作為解析器，結構化處理 DOM     |
| 資料清理   | `re` (正則表達) | 過濾無關字元，僅保留中文與標點             |
| 系統操作   | `os`            | 檢查檔名是否重複、自動建立資料夾           |
| 格式化輸出 | `pprint`        | 美化 console 輸出，利於除錯與驗證結果     |

---

### 🧩 邏輯流程與實作細節

1. **初始化設定**
   - 設定目標 URL：https://www.gutenberg.org/browse/languages/zh
   - 使用 `requests` 取得 HTML，並以 `lxml` 解析。

2. **資料擷取**
   - 解析 HTML 結構中 `<li class="pgdbetext">` 的 `<a>` 標籤。
   - 擷取書名與超連結。

3. **處理與儲存**
   - 清洗書名（移除特殊符號），避免命名錯誤。
   - 自動命名避免重複，儲存為 `.txt`。
   - 訪問每本書的內容頁（`.html.images`）並擷取 `<p>` 段落。

4. **內容清洗**
   - 僅保留中文字與常用標點。
   - 分段儲存，每段以 `---` 分隔，方便後續處理。

5. **容錯與限制**
   - 最大下載上限 200 本書。
   - 遇到請求錯誤或內容為空時，自動跳過該本書。

---

## 🗂️ 專案結構

project_gutenberg/
├── 書名1.txt
├── 書名2.txt
├── ...

- 每本書為一個 `.txt` 檔案。
- 內容為經過清洗與段落分隔的純文字資料。

---

## 🚀 使用方法

```bash
# 環境需求
pip install requests beautifulsoup4 lxml

# 執行主程式
python main.py
```

---

## 成果
![](執行過程的擷圖或說明圖片)
(https://youtu.be/lm7bTKu8IvM)
