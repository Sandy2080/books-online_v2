import etl_functions
import etl_handlers
import helpers
import os

fieldnames = ["Title","Category", "Description", "UPC", "Price", "Link", "Image url", "Product Type", "Price (excl. tax)", "Price (incl. tax)", "Tax", "In stock", "Availability", "Number of reviews", "Ratings"]
url = "http://books.toscrape.com/"
url_category = "http://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html"
soup = etl_functions.get_page_content("http://books.toscrape.com/")
soup_category = etl_functions.get_page_content(url)

# create directories
helpers.create_directory("data/")
helpers.create_directory("data/images")

# 1- scraping books of home page
def get_books():
    books = []
    for article in soup.find_all('article', {'class': 'product_pod'}):
        books.append(article)
    products = etl_functions.get_products(books)
    etl_functions.dict_to_csv('data/products.csv', products, fieldnames)
    
# 2-a scraping books for one category
def get_books_by_category():
    all_books_by_category = []
    for article in soup_category.find_all('article', {'class': 'product_pod'}):
        all_books_by_category.append(article)
    products_sequential_art = etl_functions.get_products(all_books_by_category)
    etl_functions.dict_to_csv('data/all_products.csv', all_books_by_category, fieldnames)

# 2-b scraping books for one category - all pages
def get_all_books_by_category():
    all_books = helpers.get_all_products(url, soup_category)
    all_books = etl_functions.get_products(all_books)
    etl_functions.dict_to_csv('data/all_products.csv', all_books, fieldnames)
    etl_functions.download_images(all_books, "Image url", "data")

# 3 scraping all books by category
def get_all_categories_and_all_books():
    helpers.create_directory("data/categories/") 
    dict_all_categories = etl_handlers.get_all_categories(soup)
    dict_all_categories_pages = etl_handlers.get_all_categories_pages(dict_all_categories)
    etl_handlers.download_all_categories_books_images(dict_all_categories_pages)

# get_books()
# get_all_books_by_category()
get_all_categories_and_all_books()



