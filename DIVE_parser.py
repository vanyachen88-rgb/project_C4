from bs4 import BeautifulSoup
import requests
import time
import random
from urllib.parse import urljoin

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/151.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7"
}

def parser(url):

    response = requests.get(url,headers=headers,)
    response.raise_for_status()
    return BeautifulSoup(response.text,"html.parser")

# =========================
# 首頁
# =========================

base_url = "https://divego.tw/areas/xiaoliuqiu"
soup = parser(base_url)
titles = soup.find_all("h3")
print("找到連結數量：", len(titles))


# =========================
# 抓前 2 個連結
# =========================

for n in titles[:2]:
    title_text = n.get_text(" ",strip=True)
    print(f'新聞標題: {title_text}')
    content = n.find_next("p")
    delay = random.uniform(2,3.5)      #亂數產生 2~3.5秒  
    time.sleep(delay)                  #讓電腦暫時休眠 指定的秒數後再開始工作 
    content_text = content.get_text(
            " ",
            strip=True
        )
    print(f'新聞內容: {content_text}')