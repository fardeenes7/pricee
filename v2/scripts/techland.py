import concurrent.futures
from bs4 import BeautifulSoup
import requests
from django.template.defaultfilters import slugify
from ..models import Product, Category, SubCategory, Feature, Link, Image, Shop
from .functions import get_urls_of_xml, removeBrand, set_category, save_images, save_product
from alive_progress import alive_bar

import os
from dotenv import load_dotenv
load_dotenv()
DEBUG = os.environ.get('DEBUG')


# session = requests.Session()
def get_product_data(url):
    shop = Shop.objects.get_or_create(name="Techland", href="https://www.techlandbd.com/", logo="https://www.techlandbd.com/image/cache/wp/gp/techland/logo/techland-white-logo-300x48.webp")[0]
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, features='lxml')
        name = soup.find('div', {'class': 'title page-title'}).text.strip() if soup.find('div', {'class': 'title page-title'}) else ""
        price = int(soup.find('div', 'product-price-group').find('div', {'class': 'product-price'}).text.replace(',', '').replace('৳', '').strip()) if soup.find('div', {'class': 'product-price-group'}) else 0

        details = soup.find('div', {'class': 'product-details'}).find_all('tr')
        for i in details:
            if i.find_all('td')[0].text == 'Stock Status':
                status = i.find_all('td')[1].text
            elif i.find_all('td')[0].text.lower() == 'brand':
                brand = i.find_all('td')[1].find('a').text
            elif i.find_all('td')[0].text.lower() == 'model' or i.find_all('td')[0].text.lower() == 'product model':
                model = i.find_all('td')[1].text
        status = status.strip() if status else "N/A"
        brand = brand.strip() if brand else "N/A"
        model = model.strip() if model else "N/A"
        model = removeBrand(brand, model)
        images = [soup.find('div', {'class': 'product-image'}).find('img')['src']] if soup.find('div', {'class': 'product-image'}) else ""
        cat = soup.find('ul', {'class': 'breadcrumb'})
        category = cat.findAll('li')[1].find('a').text.strip() if cat.findAll('li')[1] else ""
        sub_category = cat.findAll('li')[2].find('a').text.strip() if cat.findAll('li')[2] else ""
        

        brand = brand if brand!="" else name.split()[0]
        model = model if model!="" else name.split()[1]

        subcategory = set_category(category, sub_category)

        product = save_product(brand, model, name, subcategory, shop, url, price, status)
        save_images(product, images)



        feature_tab = ""
        if soup.find('div', {'id': 'tab-specification'}):
            feature_tab = soup.find('div', {'id': 'tab-specification'}).find('tbody')
        elif soup.find('div', {'class': 'block-content  block-description'}):
            feature_tab = soup.find('div', {'class': 'block-content  block-description'})
        if feature_tab and feature_tab.find('tr'):
            for row in feature_tab.findAll('tr'):
                feature = row.findAll('td')[0].text[:255]
                value = row.findAll('td')[1].text.replace('\n', '<br>')[:255]
                try:
                    feature = Feature.objects.get_or_create(product=product, name=feature)[0]
                except:
                    feature = Feature.objects.filter(product=product, name=feature)[0]
                feature.value = value
                feature.save()
                    
        # print('Loaded : ' + name)

    except Exception as e:
        # print("Error loading " + url)
        # print(e)
        pass



def load_from_techland():
    print("Loading from Techland")
    links_data_arr = get_urls_of_xml("https://www.techlandbd.com/sitemaps/product-sitemap.xml", "xml")
    # if DEBUG == 'True':
    #     links_data_arr = links_data_arr[:100]
    for link in links_data_arr:
        get_product_data(link)
    # with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
    #     executor.map(get_product_data, links_data_arr)
    print("Loading from Techland Complete")

