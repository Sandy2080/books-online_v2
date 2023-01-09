import requests
import os
from os.path import exists
import etl_functions

def get_number_of_pages(soup):
    ''' Function : get_number_page

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

print(get_number_of_pages.__doc__)

def get_category_pages(url, count):
    ''' Function : get_category_pages

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

print(get_category_pages.__doc__)

def get_all_products(url, soup):
    ''' Function : get_all_products

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

print(get_all_products.__doc__)

def download_img(directory, img_url):
    ''' Function : download_img

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
        with open(directory, 'wb') as handler: 
            handler.write(img_data) 
    except IOError:
        print("I/O error:" + str(IOError))

print(download_img.__doc__)

def create_directory(path):
    ''' Function : download_img

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

print(create_directory.__doc__)

def create_category_directory(path, name):
    ''' Function : download_img

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

print(create_category_directory.__doc__)