import requests as req
from bs4 import BeautifulSoup as bs
from pprint import pprint
import re
import os

url = "https://www.gutenberg.org/browse/languages/zh"

# 用 requests 的 get 方法把網頁抓下來
res = req.get(url) 

# 指定 lxml 作為解析器
soup = bs(res.text, "lxml") 
# 透過迭代取得所有 a 的文字內容
for a in soup.select('li.pgdbetext'):
    print(a.get_text())

# 創建 project_gutenberg 資料夾
output_dir = "project_gutenberg"
os.makedirs(output_dir, exist_ok=True)

list_data = []
book_count = 0  # 成功處理的書籍計數

# 假設 soup 已初始化
books = soup.select('li.pgdbetext > a[href]')
print(f"總共找到 {len(books)} 本書可處理")

for li in books:
    if book_count >= 200:  # 達到 200 本書結束
        print(f"已成功處理 {book_count} 本書，結束執行")
        break
    
    # 取得書名作為檔案名稱
    book_name = li.get_text().strip()
    book_name = re.sub(r'[^\w\u4e00-\u9fff]', '_', book_name)
    
    # 確保檔案名稱唯一
    base_name = book_name
    suffix = 0
    book_filename = os.path.join(output_dir, f"{book_name}.txt")
    while os.path.exists(book_filename):
        suffix += 1
        book_filename = os.path.join(output_dir, f"{base_name}_{suffix}.txt")
    
    # 取得書的 URL
    book_id = li.get('href')
    url_ = f"https://www.gutenberg.org/{book_id}.html.images"
    print(f"正在處理: {url_} ({book_name})")
    
    try:
        # 發送請求並解析
        res_ = req.get(url_, timeout=10)
        res_.raise_for_status()
        soup_ = bs(res_.text, "lxml")
        
        list_data = []  # 清空 list_data
        for content in soup_.select('p'):
            cleaned_text = re.sub(r'[^\u4e00-\u9fff\u3000-\u303f]', '', content.get_text())
            lines = [line for line in cleaned_text.splitlines() if line.strip()]
            list_data.extend(lines)
        
        # 檢查是否有內容
        if not list_data:
            print(f"無中文內容: {book_name}")
            continue
        
        # 寫入檔案
        try:
            with open(book_filename, "w", encoding="utf8") as file:
                for i, line in enumerate(list_data):
                    file.write(line + "\n")
                    if i < len(list_data) - 1:
                        file.write("---\n")
            # 成功寫入檔案後增加計數
            book_count += 1
            print(f"已完成 {book_count} 本書: {book_filename}")
        
        except IOError as e:
            print(f"檔案寫入失敗: {book_filename}, 錯誤: {e}")
            continue
    
    except req.exceptions.RequestException as e:
        print(f"請求失敗: {url_}, 錯誤: {e}")
        continue

# 最終輸出
print(f"總共成功處理 {book_count} 本書")
pprint(list_data, indent=4)