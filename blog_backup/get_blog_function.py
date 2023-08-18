import requests
from bs4 import BeautifulSoup
import hjson
import urllib
import os

def get_category(blog_id):
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
        category_id = category_id.replace("category", "")
        if category.get(category_id) is None:
            category[category_id] = category_name
    return category

def get_list(blog_id, category, max_page=None):
    results = []
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


        for post in posts_list:
            logNo = post.get('logNo')
            enc_title = urllib.request.unquote(post.get('title').replace("+", " "))
            category_no = post.get('categoryNo')

            parent_category_no = post.get('parentCategoryNo')
            category_text = category[category_no]
            
            results.append({
                "logNo": logNo,
                "title" : enc_title,
                "categoryNo" : category_no,
                "parentCategoryNo" : parent_category_no,
                "category" : category_text
            })

        bs = BeautifulSoup(paging_list, "lxml")
        next_tag = bs.select_one("a.next")
        if next_tag is None:
            break
        if max_page is not None and max_page <= page:
            break
        page += 1
    return results

def make_index(save_dir, post_list):
    with open(save_dir+ "\\index.html", "w", encoding="utf-8") as f:
        html = "<table>\n"
        f.write(html)
        for post in post_list:
            logNo = post.get("logNo")
            title = post.get("title")
            f.write("<tr><td>")
            f.write(f"<a href='{save_dir}\pages\{logNo}.html' target='_blank'>{title}</a>")
            f.write("</td></tr>")
            f.write("\n")

def get_detail(blog_id, logNo):
    url = f"https://blog.naver.com/PostList.naver?blogId={blog_id}&logNo={logNo}"
    r = requests.get(url)
    ns = BeautifulSoup(r.text, "lxml")
    mainContent = ns.select_one("div.se-main-container")
    if mainContent is None:
        mainContent = ns.select_one("div#postViewArea > div")
    return mainContent

def main():
    blog_id = "woojung357"
    
    current_path = os.path.dirname(os.path.realpath(__file__))  
    save_dir = current_path + "\\" + blog_id
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
        
    category = get_category(blog_id)
    post_list = get_list(blog_id, category, max_page=3)
    
    for post in post_list:
        logNo = post.get("logNo")
        contents = get_detail(blog_id, logNo)
        
        with open(save_dir+ f"\\pages\{logNo}.html", 'w', encoding="utf-8") as f:
            f.write(str(contents))
    make_index(save_dir,post_list)
main()