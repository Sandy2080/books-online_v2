import functions


# 1- scraping books of home page
articles = []
fieldnames = ["Title","Category", "Description", "UPC", "Price", "Link", "Product Type", "Price (excl. tax)", "Price (incl. tax)", "Tax", "In stock", "Availability", "Number of reviews", "Ratings"]
soup = functions.request("http://books.toscrape.com/")

for article in soup.find_all('article', {'class': 'product_pod'}):
    articles.append(article)

functions.get_product("http://books.toscrape.com/catalogue/its-only-the-himalayas_981/index.html")
products = functions.get_products(articles)
functions.dict_to_csv('data/products.csv', products, fieldnames)
