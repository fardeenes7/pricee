from unicodedata import category
from bs4 import BeautifulSoup
import requests

def get_urls_of_xml(xml_url):
    r = requests.get(xml_url)
    xml = r.text
    soup = BeautifulSoup(xml)

    links_arr = []
    for link in soup.findAll('loc'):
        linkstr = link.getText('', True)
        links_arr.append(linkstr)

    return links_arr

def get_product_data(url):
    r = requests.get(url)
    html = r.text
    soup = BeautifulSoup(html)
    title = soup.find('div', {'class': 'product_content'}).find('h1').getText('', True)
    regular_price = soup.find('span', {'class': 'rp-block'}).find('span').getText('', True)[17:]
    price = soup.find('span', {'class': 'sp-block'}).getText('', True)[17:]
    image = soup.find('img', {'class': 'xzoom order-lg-last'}).get('src')
    category = soup.find('div', {'class': 'category-pagination-section'}).find_all('a')[1].getText('', True)
    return {'title': title, 'regular_price': regular_price, 'price': price, 'image': image, 'category': category}



links_data_arr = get_urls_of_xml("https://www.ryanscomputers.com/product-sitemap.xml")
for link in links_data_arr[2:10]:
    print(link)
    print(get_product_data(link))

print(len(links_data_arr))
