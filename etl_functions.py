import requests
import csv
import os
from bs4 import BeautifulSoup
from os.path import exists
import helpers

# Extract
def get_page_content(url): 
    ''' Function : get_page_content

        Parameters
        ----------
        url : string 
              web page link
        Returns
        ----------
        page_content : BeautifulSoup
                       content of web page 
    '''
    try:
        page = requests.get(url)
        page_content = BeautifulSoup(page.content, 'html.parser')
        return page_content
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
    except requests.exceptions.RequestException as err:
        print ("OOps: Something Else",err)

print(get_page_content.__doc__)

# Transform
def get_products(items): 
    ''' Function : get_products

        Parameters
        ----------
        items : array 
                web page content and html tags
        Returns
        ----------
        products : dictionary
                   products information 
    '''
    products = []
    for item in items:
        ratings_arr = []
        link = 'http://books.toscrape.com/catalogue/' + item.find("div", {'class', 'image_container'}).a.get('href')
        link = link.replace("/../../../", "/") if link.find("/../../../") else link
        link = link.replace("/catalogue/catalogue/", "/catalogue/") # the word 'catalogue' may appear twice
        title = item.h3.a.get('title')
        stock = item.find('p', {'class': 'instock availability'})
        stock = stock.text.replace("\n", "").replace(" ", "") 
        is_in_stock = "✔️" if stock == "Instock" else "❌"
        price = item.find('p', {'class': 'price_color'})
        star_rating = item.find('p', {'class', 'star-rating'}).get('class')
        ratings_arr.append(star_rating[1])

        book_dict = { 
            "Title": title, 
            "Price": price.text, 
            "Link": link,
            "In stock": is_in_stock, 
            "Ratings": helpers.display_ratings(star_rating[1].lower())
        }
        book_details = get_product(link)
        book_dict.update(book_details)
        products.append(book_dict)
    return products

print(get_products.__doc__)

def get_product(link):
    ''' Function : get_product
    
        Parameters
        ----------
        link : string 
               product link
        Returns
        -------
        dictionary :  a dictionnary 
                      additional information for every product :
                    - price_including_tax
                    - price_excluding_tax
                    - number_available (stock)
                    - number of reviews
                    - product_description
                    - category
                    - image url
    '''
    dictionary = {}
    link = link.replace("/../../../", "/")  if "catalogue" in link else link.replace("/../../../", "/catalogue/")

    book = get_page_content(link)

    #book description
    product_description = book.find('div', {'id': 'product_description'})
    if product_description is not None: 
        description_p = product_description.find_next_siblings("p")[0].text
        dictionary["Description"] = description_p
    
    #book category (breadcrumb)
    breadcrumb = book.find('ul', {'class': 'breadcrumb'})
    if  breadcrumb is not None: 
        category = breadcrumb.find_all('li')[2]
        dictionary["Category"] = category.a.text

    #image_url
    thumbnail = book.find('div', {'class': 'thumbnail'})
    if  thumbnail is not None:
        src = thumbnail.img.get('src')
        image_url = src.replace("../../", "https://books.toscrape.com/")
        dictionary["Image url"] = image_url
    
    # table - other book details
    table = book.find('table', {'class': 'table table-striped'})
    if table is not None:
        all_tr = table.find_all('tr')
        for tr in all_tr:
            key = tr.find('th').text
            value = tr.find('td').text
            dictionary[key] = value
    
    dictionary["Number of reviews"] = "No Reviews" if dictionary["Number of reviews"] == 0 else dictionary["Number of reviews"]
    return dictionary

print(get_product.__doc__)

# Load
def dict_to_csv(filename, items, field_names) :
    ''' Function : dict_to_csv

        Parameters
        ----------
        filename: string
                  name of csv file to download data
                  
        items: array 
               list of products

        field_names: array of strings
                     list of fieldnames to appear on the csv file
                     
    '''
    try:
        with open(filename, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=field_names)
            writer.writeheader()
            writer.writerows(items)
    except IOError:
        print("I/O error")

print(dict_to_csv.__doc__)
        
def download_images(items, key, path):
    ''' Function : download_images

        Parameters
        ----------
        items : array 
                image links
        key : string 
              key name in dictionary "Image Url"  
        path : string
               name of directory where images are downloaded
    '''
    if not exists(path+'/images/'): 
        os.mkdir(path+'/images/')  
    for p in items:
        if key in p:
            image_url = p[key]
            title = image_url.split("/")[-1]
            images_path = path+"/images/"+title
            helpers.download_img(images_path, image_url)

print(download_images.__doc__)