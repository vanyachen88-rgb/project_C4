# DiveGo 潛點資料爬蟲 README

## 專案說明

本專案使用 Python 爬取 DiveGo 潛水網站的區域頁面，透過 `Requests` 取得網頁 HTML，再使用 `BeautifulSoup` 解析 HTML 結構，擷取潛點名稱與對應的潛點介紹。

目前以小琉球區域頁面作為測試：

```text
https://divego.tw/areas/xiaoliuqiu
```

---

## 使用技術

* **Python**：主要開發語言
* **Requests**：發送 HTTP Request，取得網頁內容
* **BeautifulSoup**：解析 HTML、搜尋指定標籤
* **Random / Time**：設定隨機請求間隔，避免短時間連續請求

安裝套件：

```bash
pip install requests beautifulsoup4
```

---

## 程式運作流程

```text
指定網站 URL
      ↓
requests.get() 取得 HTML
      ↓
BeautifulSoup 解析 HTML
      ↓
搜尋所有 <h3>
      ↓
取得潛點名稱
      ↓
尋找該 <h3> 後面的第一個 <p>
      ↓
取得潛點介紹
      ↓
輸出資料
```

---

## 核心程式

```python
from bs4 import BeautifulSoup
import requests
import time
import random

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/151.0.0.0 Safari/537.36",
    "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7"
}


def parser(url):
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


# =========================
# 指定爬取頁面
# =========================

base_url = "https://divego.tw/areas/xiaoliuqiu"

soup = parser(base_url)

titles = soup.find_all("h3")

print("找到潛點數量：", len(titles))


# =========================
# 抓取前 2 個潛點
# =========================

for n in titles[:2]:

    # 取得潛點名稱
    title_text = n.get_text(" ", strip=True)
    print(f"潛點名稱：{title_text}")

    # 找到 h3 後面的第一個 p
    content = n.find_next("p")

    # 隨機等待 2～3.5 秒
    delay = random.uniform(2, 3.5)
    time.sleep(delay)

    # 取得潛點內容
    if content:
        content_text = content.get_text(" ", strip=True)
        print(f"潛點內容：{content_text}")
    else:
        print("潛點內容：找不到")

    print("-" * 50)
```

---

## 重要程式說明

### `parser(url)`

負責取得並解析網頁：

```python
response = requests.get(url, headers=headers)
```

向網站發送 GET Request。

```python
response.raise_for_status()
```

確認 HTTP Request 是否成功，若發生 404、403、500 等錯誤會拋出 Exception。

```python
BeautifulSoup(response.text, "html.parser")
```

將 HTML 轉換成 BeautifulSoup 可搜尋的結構。

### `find_all("h3")`

```python
titles = soup.find_all("h3")
```

找出頁面中所有 `<h3>`，目前將其視為潛點名稱。

### `find_next("p")`

```python
content = n.find_next("p")
```

從目前的 `<h3>` 往後尋找第一個 `<p>`，作為該潛點的介紹內容。

### `titles[:2]`

```python
for n in titles[:2]:
```

目前只抓前 2 筆作為測試。

若確認資料正確，要抓全部資料，可改成：

```python
for n in titles:
```

---

## 延遲機制

```python
delay = random.uniform(2, 3.5)
time.sleep(delay)
```

每次處理資料前隨機等待 2～3.5 秒，避免程式在短時間內連續發送大量 Request。

---

## 注意事項

目前程式是依照 DiveGo 頁面的 HTML 結構進行解析，因此如果網站修改 `<h3>`、`<p>` 或其他 DOM 結構，Selector 可能需要重新調整。

另外，如果網站資料是由 JavaScript 動態載入，`requests` 取得的 HTML 可能不包含瀏覽器畫面中看到的資料，此時需要進一步檢查網站 API 或改用瀏覽器自動化工具。

確認目前的 HTML 結構與資料擷取方式穩定後，可以再擴充成 **CSV / Excel / JSON 匯出、批次爬取不同地區，以及完整潛點資料庫**。
