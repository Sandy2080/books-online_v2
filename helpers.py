from bs4 import BeautifulSoup
import requests
import os
from os.path import exists
import etl_functions

def get_number_of_pages(soup : BeautifulSoup):
    '''
        Parameters
        ----------
        soup : BeautifulSoup
               content of web page 
        Returns
        ----------
        page_count : number
                     every category page count
    '''
    page_count = 1
    if soup.find('ul', {'class': 'pager'}):
        pages = soup.find('li', {'class': 'current'}).text.replace("\n", "").split(" ")
        pages = list(filter(lambda p: p != "", pages))
        page_count = int(pages[-1])
    return page_count

def get_category_pages(url : str, count: int):
    '''
        Parameters
        ----------
        url : string
              category name
        count : number
                number of pages per category
        Returns
        ----------
        urls : array of strings
               every category's page link
    '''
    urls = []
    index = 1
    while index <= count:
        _url = url.replace("index.html", "page-" + str(index) + ".html")
        urls.append(_url)
        index +=1
    return urls

def get_all_articles(url: str, soup: BeautifulSoup):
    '''
        Parameters
        ----------
        url : string
              category name
        soup : BeautifulSoup
               content of web page
        Returns
        ----------
        all_products : array 
                       every category's page content
    '''
    all_products = []
    pages_count = get_number_of_pages(soup)
    all_pages = get_category_pages(url, pages_count)
    for page in all_pages:
        page_content = etl_functions.get_page_content(page)
        for article in page_content.find_all('article', {'class': 'product_pod'}):
            all_products.append(article)
    return all_products

def download_img(directory: str, img_url: str):
    '''
        to create a path to directory and download image from url

        Parameters
        ----------
        directory : string
                    path to download image
        img_url : string
                  image link
        Returns
        ----------
        no return
    '''
    img_data = requests.get(img_url).content
    try:
        with open(directory, 'wb', encoding='utf8') as handler: 
            handler.write(img_data) 
    except IOError:
        print("I/O error:" + str(IOError))

def create_directory(path: str):
    '''
        Parameters
        ----------
        path : string
               path to create new directory
        Returns
        ----------
        no return
    '''
    if not exists(path): 
        os.mkdir(path)   

def create_category_directory(path: str, name: str):
    '''
        Parameters
        ----------
        path : string
               path to create new directory
        name : string
               category's name
        Returns
        ----------
        path : string
               path to new directory
    '''
    dir_category_name = name.split(" ")
    dir_category_name = "_".join(dir_category_name).lower()
    path = path+dir_category_name 
    if not exists(path): 
        os.mkdir(path) 
    return path

def display_ratings(rating_level: str):
    if rating_level == "one":
        return "1"
    elif rating_level == "two":
        return "2"
    elif rating_level == "three":
        return "3"
    elif rating_level == "four":
        return "4"
    elif rating_level == "five":
        return "5"
    else:
        return ""
