import requests
import csv
from bs4 import BeautifulSoup


url = "http://books.toscrape.com/"
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

# 1- scraping books of home page
articles = []

# Extract
for article in soup.find_all('article', {'class': 'product_pod'}):
    articles.append(article)

# Transform
def get_products(items): 
    products = []
    for item in items:
        ratings_arr = []
        link = 'http://products.toscrape.com/catalogue/' + item.find("div", {'class', 'image_container'}).a.get('href')
        title = item.h3.a.get('title')
        stock = item.find('p', {'class': 'instock availability'})
        stock = stock.text.replace("\n", "").replace(" ", "") 
        is_in_stock = "In stock" if stock == "Instock" else "not available"
        price = item.find('p', {'class': 'price_color'})
        star_rating = item.find('p', {'class', 'star-rating'}).get('class')
        ratings_arr.append(star_rating[1])
        products.append(
            { 
            "title": title, 
            "price": price.text, 
            "link": link, 
            "in stock": is_in_stock, 
            "ratings": star_rating[1]
        })
    return products

# Load
def dict_to_csv(filename, items, field_names) :
    try:
        with open(filename, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=field_names)
            writer.writeheader()
            writer.writerows(items)
    except IOError:
        print("I/O error")

products = get_products(articles)
dict_to_csv('data/products.csv', products, ["title","price", "link", "in stock", "ratings"])
