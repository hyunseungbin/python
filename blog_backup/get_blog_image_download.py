import requests
from bs4 import BeautifulSoup
import hjson
import urllib
import os
import get_blog_function as gb

def get_image(blog_id, logNo):
    contents = gb.get_detail(blog_id, logNo)
    imgs = contents.select("img")
    current_path = os.path.dirname(os.path.realpath(__file__))  
    save_dir = current_path + "\\" + "minahan"
    os.makedirs(save_dir+"\\images", exist_ok=True)
    
    for i, img in enumerate(imgs):
        try:
            img_req = requests.get(img.get('data-lazy-src'))
            with open(save_dir+ f"\\images\img_{i}.jpg", 'wb') as f:
                f.write(img_req.content)
        except:
            pass

def main():
    blog_id = "woojung357"
    
    current_path = os.path.dirname(os.path.realpath(__file__))  
    save_dir = current_path + "\\" + blog_id
    os.makedirs(save_dir,exist_ok=True)
    os.makedirs(save_dir+"\\pages", exist_ok=True)
    
    category = get_category(blog_id)
    post_list = get_list(blog_id, category, max_page=3)
    
    for post in post_list:
        logNo = post.get("logNo")
        contents = get_detail(blog_id, logNo)
        
        with open(save_dir+ f"\\pages\{logNo}.html", 'w', encoding="utf-8") as f:
            f.write(str(contents))
    make_index(save_dir,post_list)

