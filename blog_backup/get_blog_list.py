import requests
from bs4 import BeautifulSoup
import hjson
import urllib


blog_id = 'woojung357'
page = 2
while True:
    url = f'https://blog.naver.com/PostTitleListAsync.naver?blogId={blog_id}&viewdate=&currentPage={page}&categoryNo=0&parentCategoryNo=&countPerPage=30'
    header = {
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Referer" : "https://blog.naver.com/PostList.naver?blogId=woojung357&categoryNo=0&from=postList"
    }

    r = requests.get(url, headers=header)
    json = hjson.loads(r.text)
    posts_list = json.get("postList")
    paging_list = json.get("pagingHtml")

    blogInfo = {}

    for post in posts_list:
        logNo = post.get('logNo')
        ## replace 
        encodingTitle = urllib.request.unquote(post.get('title').replace("+", " "))
        categoryNo = post.get('categoryNo')
        
        url = f"https://blog.naver.com/PostList.naver?blogId={blog_id}"
        r = requests.get(url)
        ns = BeautifulSoup(r.text, "lxml")
        mainContent = ns.select_one("div.se-main-container")
        print(mainContent)

    bs = BeautifulSoup(paging_list, "lxml")
    next_tag = bs.select_one("a.next")
    if next_tag is None:
        break
    page += 1