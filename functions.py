import requests
import csv
from bs4 import BeautifulSoup

# Extract
def request(url): 
    page = requests.get(url)
    return BeautifulSoup(page.content, 'html.parser')

# Transform
def get_products(items): 
    products = []
    for item in items:
        ratings_arr = []
        link = 'http://books.toscrape.com/' + item.find("div", {'class', 'image_container'}).a.get('href')
        link = link.replace("/../../../", "/catalogue/")
        title = item.h3.a.get('title')
        stock = item.find('p', {'class': 'instock availability'})
        stock = stock.text.replace("\n", "").replace(" ", "") 
        is_in_stock = "In stock" if stock == "Instock" else "not available"
        price = item.find('p', {'class': 'price_color'})
        star_rating = item.find('p', {'class', 'star-rating'}).get('class')
        ratings_arr.append(star_rating[1])

        book_dict = { 
            "Title": title, 
            "Price": price.text, 
            "Link": link,
            "In stock": is_in_stock, 
            "Ratings": star_rating[1]
        }
        book_details = get_product(link)
        book_dict = dict(list(book_dict.items()) + list(book_details.items()))
        products.append(book_dict)
    return products

def get_product(link):
    dictionary = {}
    link = link.replace("/../../../", "/catalogue/") # may be necessary to format links
    book = request(link)

    #book description
    product_description = book.find('div', {'id': 'product_description'})
    description_p = product_description.find_next_siblings("p")[0].text
    dictionary["Description"] = description_p

    #book category
    breadcrumb = book.find('ul', {'class': 'breadcrumb'})
    category = breadcrumb.find_all('li')[2]
    dictionary["Category"] = category.a.text

    #image_url
    thumbnail = book.find('div', {'class': 'thumbnail'})
    src = thumbnail.img.get('src')
    image_url = src.replace("../../", "https://books.toscrape.com/")
    dictionary["Image url"] = image_url
    
    #other book details
        # price_including_tax
        # price_excluding_tax
        # number_available (stock)
        # number of reviews
        # product_description
        # category
        # image url
    table = book.find('table', {'class': 'table table-striped'})
    all_tr = table.find_all('tr')
    for tr in all_tr:
        key = tr.find('th').text
        value = tr.find('td').text
        dictionary[key] = value

    return dictionary
    
# Load
def dict_to_csv(filename, items, field_names) :
    try:
        with open(filename, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=field_names)
            writer.writeheader()
            writer.writerows(items)
    except IOError:
        print("I/O error")