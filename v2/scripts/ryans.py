import concurrent.futures
from bs4 import BeautifulSoup
import requests
from django.template.defaultfilters import slugify
from v2.models import Product, Category, SubCategory, Link, Image, Feature, Shop
from .functions import get_urls_of_xml, removeBrand, set_category, save_images, save_product

import os
from dotenv import load_dotenv
load_dotenv()
DEBUG = os.environ.get('DEBUG')

shop = Shop.objects.get_or_create(name="Ryans", href="https://www.ryanscomputers.com/", logo="https://www.ryanscomputers.com/assets/images/ryans-logo.svg")[0]


def get_product_data(url):
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, features='lxml')
        name = soup.find('div', {'class': 'product_content'}).find('h1').getText('', True)
        regular_price = soup.find('span', {'class': 'rp-block'}).find('span').getText('', True)[17:].replace(',', '').strip() if soup.find('span', {'class': 'rp-block'}) else 0
        regular_price = 0 if regular_price == '' else int(regular_price)
        price = soup.find('span', {'class': 'sp-block'}).getText('', True)[17:].replace(',', '').replace("Coming Soon","").strip() if soup.find('span', {'class': 'sp-block'}) else 0
        price = 0 if price == "" else int(price)
        #image = soup.find('img', {'class': 'xzoom order-lg-last'}).get('src')
        images = []
        image_list = soup.find('div', {'class': 'xzoom-thumbs'}).find_all('a') if soup.find('div', {'class': 'xzoom-thumbs'}) else []
        for image in image_list:
            images.append(image.get('href'))
        category = soup.find('div', {'class': 'category-pagination-section'}).find_all('a')[1].getText('', True)
        sub_cat_finder = soup.find('div', {'class': 'category-pagination-section'}).find_all('a')
        subcategory = sub_cat_finder[3].getText('', True) if len(sub_cat_finder[3].getText('', True)) <= 20 else sub_cat_finder[2].getText('', True)
        brand = ""
        model = ""
        status = "In Stock" if price else "Out of Stock"
        features = {}
        for row in soup.find_all('div', {'class': 'row table-hr-remove'}):
            feature_title = row.find('span', {'class': 'att-title'}).getText('', True)
            feature_value = row.find('span', {'class': 'att-value'}).getText('', True)
            if feature_title == 'Brand':
                brand = feature_value
            elif feature_title == 'Model':
                model = removeBrand(brand,feature_value)
            else:
                features[feature_title] = feature_value
        brand = brand if brand!="" else name.split()[0]
        model = model if model!="" else name.split()[1]
        #color = get_color(title)
        
        subcategory = set_category(category, subcategory)

        product = save_product(brand, model, name, subcategory, shop, url, price, status)
        save_images(product, images)

        for f1, f2 in features.items():
            try:
                feature = Feature.objects.get_or_create(product=product, name=f1)[0]
            except:
                feature = Feature.objects.filter(product=product, name=f1)[0]
            feature.value = f2
            feature.save()
        print("Loaded: " + name)
    except Exception as e:
        print("Error loading "+ url)
        print(e)


def load_from_ryans():
    print("Loading from Ryans")
    
    links_data_arr = get_urls_of_xml("https://www.ryanscomputers.com/product-sitemap.xml", "xml")
    # if DEBUG == 'True':
    #     links_data_arr = links_data_arr[:100]
    # links_data_arr = test_data
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        executor.map(get_product_data, links_data_arr)
    print("Loading from Ryans Complete")

