import etl_functions
import helpers

fieldnames = ["Title","Category", "Description", "UPC", "Price", "Link", "Image url", "Product Type", "Price (excl. tax)", "Price (incl. tax)", "Tax", "In stock", "Availability", "Number of reviews", "Ratings"]

def get_all_categories(soup):
    dict_all_categories = {}

    for a in soup.find('div', {'class': 'side_categories'}).ul.find_all('a'):
        category = a.text.replace('\n', '').replace('  ', '')
        if 'books_1' not in a.get('href'): 
            dict_all_categories[category] = 'http://books.toscrape.com/' + a.get('href')
    return dict_all_categories

def get_all_categories_pages(dict_all_categories):
    dict_all_categories_pages = {}

    for category, url in dict_all_categories.items():
        page = etl_functions.get_page_content(url)
        page_count = helpers.page_number(page)
        if page_count > 1:
            pages = helpers.get_pages(url, page_count)
            dict_all_categories_pages[category] = pages
        else:
            dict_all_categories_pages[category] = [url]
    return dict_all_categories_pages

def download_all_categories_books_images(dict_all_categories):
    for category, urls in dict_all_categories.items():
        all_articles_by_category = []
        all_products_by_category = []
        for url in urls:
            soup_category = etl_functions.get_page_content(url)
            for article in soup_category.find_all('article', {'class': 'product_pod'}):
                all_articles_by_category.append(article)
            all_products_by_category = etl_functions.get_products(all_articles_by_category)
        dir_category_path = helpers.create_category_directory('data/categories/', category)
        etl_functions.dict_to_csv(dir_category_path+'/products.csv', all_products_by_category, fieldnames)
        etl_functions.download_images(all_products_by_category, "Image url", dir_category_path)



