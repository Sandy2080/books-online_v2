import requests
import os
from os.path import exists
import etl_functions

def page_number(soup):
    if soup.find('ul', {'class': 'pager'}):
        pages = soup.find('li', {'class': 'current'}).text.replace("\n", "").split(" ")
        pages = list(filter(lambda p: p != "", pages))
        return int(pages[-1])
    else: return 1

def get_pages(url, count):
    urls = []
    index = 1
    while index <= count:
        _url = url.replace("index.html", "page-" + str(index) + ".html")
        urls.append(_url)
        index +=1
    return urls

def get_all_products(url, soup):
    all_products = []
    pages_count = page_number(soup)
    all_pages = get_pages(url, pages_count)
    for page in all_pages:
        page_content = etl_functions.request(page)
        for article in page_content.find_all('article', {'class': 'product_pod'}):
            all_products.append(article)
    return all_products

def download_img(directory, img_url):
    img_data = requests.get(img_url).content
    try:
        with open(directory, 'wb') as handler: 
            handler.write(img_data) 
    except IOError:
        print("I/O error:" + str(IOError))

def create_directory(path):
    if not exists(path): 
        os.mkdir(path)   

def create_category_directory(path, name):
    dir_category_name = name.split(" ")
    dir_category_name = "_".join(dir_category_name).lower()
    path = path+dir_category_name 
    if not exists(path): 
        os.mkdir(path) 
    return path