import functions


# 1- scraping books of home page
articles = []

soup = functions.request("http://books.toscrape.com/")

for article in soup.find_all('article', {'class': 'product_pod'}):
    articles.append(article)

products = functions.get_products(articles)
functions.dict_to_csv('data/products.csv', products, ["title","price", "link", "in stock", "ratings"])
