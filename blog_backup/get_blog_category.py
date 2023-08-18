import requests
from bs4 import BeautifulSoup
import hjson

blog_id = 'nkj2001'
url = f'https://blog.naver.com/WidgetListAsync.naver?blogId={blog_id}&enableWidgetKeys=category'
header = {
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Referer" : f"https://blog.naver.com/PostList.naver?blogId={blog_id}&categoryNo=0&from=postList"
}

r = requests.get(url, headers=header)
json = hjson.loads(r.text)

category_html = json.get('category').get('content')

category = {}

bs = BeautifulSoup(category_html, "lxml")
links = bs.select("a")
for lk in links:
    #pprint.pprint(lk)
    href = lk.get("href")
    if href is None or href == "#":
        continue
    category_name = lk.text
    category_id = lk.get("id")
    if category.get(category_id) is None:
        category[category_id] = category_name
        
print(category)