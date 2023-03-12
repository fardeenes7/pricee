import concurrent.futures
from bs4 import BeautifulSoup
import requests


def get_urls_of_xml(xml_url, feature):
    r = requests.get(xml_url)
    soup = BeautifulSoup(r.text, features=feature)
    links_arr = []
    for link in soup.findAll('loc'):
        linkstr = link.getText('', True)
        links_arr.append(linkstr)
        # if linkstr.__contains__('keyboard'):
        #     links_arr.append(linkstr)

    return links_arr



# session = requests.Session()
def get_product_data(url):
    if not url.__contains__('head'):
        #print("Skipping " + url)
        return
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, features='lxml')
        name = soup.find('div', {'class': 'info-block-title'}).text.strip()
        if name.lower().__contains__('coupon'):
            print(url)

    except Exception as e:
        print("Error loading " + url)
        print(e)



def load_from_techland():
    print("Loading from Techland")
    links_data_arr = get_urls_of_xml("https://www.techlandbd.com/sitemaps/product-sitemap.xml", "html.parser")
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        executor.map(get_product_data, links_data_arr)
    print("Loading from Techland Complete")



# load_from_techland()