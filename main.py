import functions
import helpers


fieldnames = ["Title","Category", "Description", "UPC", "Price", "Link", "Image url", "Product Type", "Price (excl. tax)", "Price (incl. tax)", "Tax", "In stock", "Availability", "Number of reviews", "Ratings"]
soup = functions.request("http://books.toscrape.com/")

# 1- scraping books of home page
def get_books():
    articles = []
    for article in soup.find_all('article', {'class': 'product_pod'}):
        articles.append(article)
    products = functions.get_products(articles)
    functions.dict_to_csv('data/products.csv', products, fieldnames)

# 2-a scraping books for one category
def get_books_by_category():
    articles_sequential_art = []
    url = "http://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html"
    soup_sequential_art = functions.request(url)

    for article in soup_sequential_art.find_all('article', {'class': 'product_pod'}):
        articles_sequential_art.append(article)

    products_sequential_art = functions.get_products(articles_sequential_art)
    functions.dict_to_csv('data/products_sequential_art/products.csv', products_sequential_art, fieldnames)

# 2-b scraping books for one category - all pages
def get_all_books_by_category():
    all_articles = helpers.get_all_products(url, soup_sequential_art)
    all_articles = functions.get_products(all_articles)
    functions.dict_to_csv('data/products_sequential_art/all_products.csv', all_articles, fieldnames)

# 3 scraping all books by category

def get_all_categories_and_all_books():
    categories = {}

    for a in soup.find('div', {'class': 'side_categories'}).ul.find_all('a'):
        category = a.text.replace('\n', '').replace('  ', '')
        if 'books_1' not in a.get('href'): 
            categories[category] = 'http://books.toscrape.com/' + a.get('href')
            
    for category, url in categories.items():
        page = functions.request(url)
        page_count = helpers.page_number(page)
        if page_count > 1:
            pages = helpers.get_pages(url, page_count)
            categories[category] = pages
        else:
            categories[category] = [url]

    for category, urls in categories.items():
        all_articles_by_category = []
        all_products_by_category = []
        for url in urls:
            soup_category = functions.request(url)
            for article in soup_category.find_all('article', {'class': 'product_pod'}):
                all_articles_by_category.append(article)
            all_products_by_category = functions.get_products(all_articles_by_category)
        dir_category_name = helpers.create_directory('data/', category)
        
        functions.dict_to_csv('data/'+dir_category_name+'/products.csv', all_products_by_category, fieldnames)


