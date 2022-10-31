import concurrent.futures
from bs4 import BeautifulSoup
import requests
from datetime import datetime
from .models import Product, Feature, Startech


def get_urls_of_xml(xml_url):
    r = requests.get(xml_url)
    soup = BeautifulSoup(r.text, features='xml')
    links_arr = []
    for link in soup.findAll('loc'):
        linkstr = link.getText('', True)
        links_arr.append(linkstr)

    return links_arr


def removeBrand(brand, model):
    brand = brand.lower().replace(' ', '').replace('-', '').strip()
    return model.lower().replace(brand, '').strip().upper()


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
        model_container = soup.find('div', class_='short-description')
        for m in model_container.findAll('li'):
            if m.text[:5] == 'Model':
                model = removeBrand(brand, m.text[7:])
        image = soup.find('img', {'class': 'main-img'})['src'] if soup.find('img', {'class': 'main-img'}) else ""

        if Startech.objects.filter(link=url).exists():
            startech = Startech.objects.get(link=url)
            startech.price = price
            startech.regular_price = regular_price
            startech.status = status
            startech.save()
            product = startech.product
            product.name = name
            product.brand = brand
            product.model = model
            product.image = image
            product.save()
        elif Product.objects.filter(brand=brand, model=model).exists():
            startech = Startech.objects.create(link=url, price=price, regular_price=regular_price, status=status)
            startech.save()
            product = Product.objects.filter(brand=brand, model=model)[0]
            product.startech = startech
            product.save()
        else:
            startech = Startech.objects.create(link=url, price=price, regular_price=regular_price, status=status)
            startech.save()
            product = Product.objects.create(name=name, brand=brand, model=model, image=image, startech=startech)
            product.save()
        for a,b in zip(soup.findAll('td', {'class': 'name'}), soup.findAll('td', {'class': 'value'}), ):
            if Feature.objects.filter(product=product, name=a.text).exists():
                feature = Feature.objects.get(product=product, name=a.text)
                feature.value = b.text
                feature.save()
            else:
                feature = Feature.objects.create(product=product, name=a.text, value=b.text)
                feature.save()
        print("Loaded: " + name)
    except Exception as e:
        print("Error loading " + url)
        print(e)


def load_from_startech():
    print("Loading from startech")
    links_data_arr = get_urls_of_xml("https://www.startech.com.bd/sitemap.xml")
    print("Total links found: " + str(len(links_data_arr)))
    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
        executor.map(get_product_data, links_data_arr[1336:])
    #for link in links_data_arr[1336:1350]:
        #get_product_data(link)

    print(f"Loading from Startech Complete")

#print(f"--- Scraped and saved {int(len(product_details_data))} products ---")