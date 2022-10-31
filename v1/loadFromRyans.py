import concurrent.futures
from bs4 import BeautifulSoup
import requests
from .models import Product, Category, SubCategory, Ryans, Feature

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
        soup = BeautifulSoup(r.text, features='lxml')
        title = soup.find('div', {'class': 'product_content'}).find('h1').getText('', True)
        regular_price = soup.find('span', {'class': 'rp-block'}).find('span').getText('', True)[17:].replace(',', '').strip() if soup.find('span', {'class': 'rp-block'}) else 0
        regular_price = 0 if regular_price == '' else int(regular_price)
        price = soup.find('span', {'class': 'sp-block'}).getText('', True)[17:].replace(',', '').replace("Coming Soon","").strip() if soup.find('span', {'class': 'sp-block'}) else 0
        price = 0 if price == "" else int(price)
        image = soup.find('img', {'class': 'xzoom order-lg-last'}).get('src')
        category = soup.find('div', {'class': 'category-pagination-section'}).find_all('a')[1].getText('', True)
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
        if Ryans.objects.filter(link=url).exists():
            ryans = Ryans.objects.get(link=url)
            ryans.price = price
            ryans.regular_price = regular_price
            ryans.status = status
            ryans.save()
            if Product.objects.filter(ryans=ryans).exists():
                product = Product.objects.get(ryans=ryans)
            else:
                product = Product.objects.create(ryans=ryans)
            product.name = title
            product.image = image
            product.brand = brand
            product.model = model
            if product.sub_category is None:
                product.sub_category = SubCategory.objects.get_or_create(name=category, category=Category.objects.get_or_create(name=category)[0])[0]
            product.save()
        elif Product.objects.filter(brand=brand, model=model).exists():
            ryans = Ryans.objects.create(link=url, price=price, regular_price=regular_price, status=status)
            ryans.save()
            product = Product.objects.get(brand=brand, model=model)
            product.ryans = ryans
            product.save()
        else:
            ryans = Ryans.objects.create(link=url, price=price, regular_price=regular_price, status=status)
            ryans.save()
            product = Product.objects.create(name=title, image=image, brand=brand, model=model, ryans=ryans, sub_category=SubCategory.objects.get_or_create(name=category, category=Category.objects.get_or_create(name=category)[0])[0])
            product.save()

        for f1, f2 in features.items():
            if not Feature.objects.filter(product=product, name=f1).exists():
                feature = Feature.objects.create(product=product, name=f1, value=f2)
                feature.save()
        print("Loaded: " + title)
    except Exception as e:
        print("Error loading "+ url)
        print(e)


def load_from_ryans():
    print("Loading from Ryans")
    links_data_arr = get_urls_of_xml("https://www.ryanscomputers.com/product-sitemap.xml")
    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
        executor.map(get_product_data, links_data_arr)
    print("Loading from Ryans Complete")

