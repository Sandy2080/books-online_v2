import functions

def page_number(soup):
    if soup.find('ul', {'class': 'pager'}):
        pages = soup.find('li', {'class': 'current'}).text.replace("\n", "").split(" ")
        pages = list(filter(lambda p: p != "", pages))
    return int(pages[-1])

def get_pages(url, count):
    urls = []
    index = 1
    while index <= count:
        _url = url.replace("index.html", "page-" + str(index) + ".html")
        print(_url)
        urls.append(_url)
        index +=1
    return urls

def get_all_products(url, soup):
    all_products = []
    pages_count = page_number(soup)
    all_pages = get_pages(url, pages_count)
    print(all_pages)
    for page in all_pages:
        page_content = functions.request(page)
        for article in page_content.find_all('article', {'class': 'product_pod'}):
            all_products.append(article)
    return all_products