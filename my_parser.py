import http.client
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from base_func import create_table, insert_product
import time


def fetch(url):
    parsed_url = urlparse(url)
    connection = http.client.HTTPSConnection(parsed_url.netloc)
    connection.request("GET", parsed_url.path)
    response = connection.getresponse()
    if response.status == 200:
        return response.read().decode()
    else:
        return None


def get_data():
    url = 'https://xn----8sbznhlgig.xn--p1ai/katalog/ventilyaciya/'

    # Получение данных с URL
    src = fetch(url)
    if src is None:
        print("Failed to retrieve the webpage.")
        return

    soup = BeautifulSoup(src, "lxml")
    product_name = soup.find_all("div", class_="product__top-block")

    for name in product_name:
        text_name = name.find("a", class_='product__name').text
        text_price = name.find("div", class_='product__price').text
        text_price = float(" ".join(text_price.split('руб. / шт')))
        text_article = name.find('div', class_="vendor-code").find('span').text
        insert_product(text_name, text_price, text_article)


if __name__ == '__main__':
    start_time = time.time()
    create_table()
    get_data()
    end_time = time.time()
    print(f"Время выполнения: {end_time - start_time} секунд")
