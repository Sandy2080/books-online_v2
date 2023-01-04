import functions
import helpers

fieldnames = ["Title","Category", "Description", "UPC", "Price", "Link", "Image url", "Product Type", "Price (excl. tax)", "Price (incl. tax)", "Tax", "In stock", "Availability", "Number of reviews", "Ratings"]

# 1- scraping books of home page
articles = []
soup = functions.request("http://books.toscrape.com/")

for article in soup.find_all('article', {'class': 'product_pod'}):
    articles.append(article)

products = functions.get_products(articles)
functions.dict_to_csv('data/products.csv', products, fieldnames)


# 2-a scraping books for one category
articles_sequential_art = []
url = "http://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html"
soup_sequential_art = functions.request(url)

for article in soup_sequential_art.find_all('article', {'class': 'product_pod'}):
    articles_sequential_art.append(article)

products_sequential_art = functions.get_products(articles_sequential_art)
functions.dict_to_csv('data/products_sequential_art/products.csv', products_sequential_art, fieldnames)

# 2-b scraping books for one category - all pages
all_articles = helpers.get_all_products(url, soup_sequential_art)
all_articles = functions.get_products(all_articles)
functions.dict_to_csv('data/products_sequential_art/all_products.csv', all_articles, fieldnames)