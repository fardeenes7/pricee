import concurrent.futures
from bs4 import BeautifulSoup
import requests
from ..models import Feature, Shop
from .functions import get_urls_of_xml, removeBrand, set_category, save_images, save_product

# 
import os
from dotenv import load_dotenv
load_dotenv()
DEBUG = os.environ.get('DEBUG')


shop = Shop.objects.get_or_create(name="Startech", href="https://www.startech.com.bd/", logo="https://www.startech.com.bd/image/catalog/logo.png")[0]


def get_product_data(url):
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, features='html.parser')
        name = soup.find('h1', {'class': 'product-name'}).text if soup.find('h1', {'class': 'product-name'}) else ""
        if soup.find('td', {'class': 'product-info-data product-price'}):
            p = soup.find('td', {'class': 'product-info-data product-price'})
            if p.find('ins'):
                price = p.find('ins').text[:-1].replace(',', '').replace('৳', '') 
            else:
                price = p.text[:-1].replace(',', '').replace('৳', '') 
        else:
            price = 0
        price = 0 if(price in ["To be announced", "To be announce"]) else int(price)
        regular_price = soup.find('td', {'class': 'product-info-data product-regular-price'}).text[:-1].replace(',', '').replace('৳', '') if soup.find('td', {'class': 'product-info-data product-regular-price'}) else 0
        regular_price = 0 if(regular_price in ["To be announced", "To be announce"]) else int(regular_price)
        status = soup.find('td', {'class': 'product-info-data product-status'}).text if soup.find('td', {'class': 'product-info-data product-status'}) else ""
        brand = soup.find('td', {'class': 'product-info-data product-brand'}).text if soup.find('td', {'class': 'product-info-data product-brand'}) else ""
        model =""
        model_container = soup.find('div', {'class':'short-description'})
        for m in model_container.findAll('li'):
            if m.text[:5] == 'Model':
                model = removeBrand(brand, m.text[7:])
        images = [soup.find('img', {'class': 'main-img'})['src']] if soup.find('img', {'class': 'main-img'}) else ""

        category = soup.find('ul', {'class': 'breadcrumb'}).findAll('a')[1].find('span').text if soup.find('ul', {'class': 'breadcrumb'}).findAll('a')[1] else ""
        subcategory = soup.find('ul', {'class': 'breadcrumb'}).findAll('a')[2].find('span').text if soup.find('ul', {'class': 'breadcrumb'}).findAll('a')[2] else ""
        brand = brand if brand!="" else name.split(' ')[0]
        model = model if model!="" else name.split(' ')[1]
        #color = get_color(name)

        subcategory = set_category(category, subcategory)

        product = save_product(brand, model, name, subcategory, shop, url, price, status)
        save_images(product, images)
        
        for a,b in zip(soup.findAll('td', {'class': 'name'}), soup.findAll('td', {'class': 'value'}), ):
            try:
                feature = Feature.objects.get_or_create(product=product, name=a.text)[0]
            except:
                feature = Feature.objects.filter(product=product, name=a.text)[0]
            feature.value = b.text
            feature.save()
        
        print("Loaded: " + name)
    except Exception as e:
        print("Error loading " + url)
        print(e)

test_data = [
    "https://www.startech.com.bd/intel-13th-gen-core-i7-13700-processor",
    "https://www.startech.com.bd/corsair-h150-liquid-cpu-cooler",
    "https://www.startech.com.bd/hp-m22f-22-inch-monitor",
    "https://www.startech.com.bd/msi-mag-b660m-mortar-wifi-ddr4-12th-gen-motherboard",
]


def load_from_startech():
    print("Loading from startech")
    links_data_arr = get_urls_of_xml("https://www.startech.com.bd/sitemap.xml", "xml")
    # links_data_arr = test_data
    print("Total links found: " + str(len(links_data_arr)))
    # if DEBUG == 'True':
    #     links_data_arr = links_data_arr[1412:1512]
    # else:
    #     links_data_arr = links_data_arr[1412:]
    links_data_arr = links_data_arr[1412:]
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        executor.map(get_product_data, links_data_arr)

    print(f"Loading from Startech Complete")
