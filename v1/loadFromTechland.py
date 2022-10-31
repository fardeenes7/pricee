import concurrent.futures
from bs4 import BeautifulSoup
import requests
from .models import Product, Category, SubCategory, Feature, Techland

def get_urls_of_xml(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
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
        name = soup.find('div', {'class': 'title page-title'}).text if soup.find('div', {'class': 'title page-title'}) else ""
        price = int(soup.find('li', {'class': 'p_price'}).find('span').text.replace(',', '').replace('৳', '').strip()) if soup.find('li', {'class': 'p_price'}) else 0
        regular_price = int(soup.find('div', 'product-price-group').find('div', {'class': 'module-item-2'}).find('span').text.replace(',', '').replace('৳', '').strip()) if soup.find('div', {'class': 'product-price-group'}) else 0
        status = soup.find('li', {'class': 'product-stock in-stock'}).find('span').text if soup.find('li', {'class': 'product-stock in-stock'}) else "Out of Stock"
        brand = soup.find('li', {'class': 'product-manufacturer'}).find('a').text if soup.find('li', {'class': 'product-manufacturer'}) else ""
        model = soup.find('li', {'class': 'product-model'}).find('span').text if soup.find('li', {'class': 'product-model'}) else ""
        model = removeBrand(brand, model)
        image = soup.find('div', {'class': 'product-image'}).find('img')['src'] if soup.find('div', {'class': 'product-image'}) else ""
        cat = soup.find('ul', {'class': 'breadcrumb'})
        category = cat.findAll('li')[1].find('a').text.strip() if cat.findAll('li')[1] else ""
        sub_category = cat.findAll('li')[2].find('a').text.strip() if cat.findAll('li')[2] else ""
        
        if Category.objects.filter(name=category).exists():
            category = Category.objects.get(name=category)
        else:
            category = Category.objects.create(name=category)
            category.save()
        if SubCategory.objects.filter(name=sub_category, category = category).exists():
            sub_category = SubCategory.objects.filter(name=sub_category, category = category)[0]
        else:
            sub_category = SubCategory.objects.create(name=sub_category, category=category)
            sub_category.save()
        
        if Techland.objects.filter(link=url).exists():
            techland = Techland.objects.get(link=url)
            techland.price = price
            techland.regular_price = regular_price
            techland.status = status
            techland.save()
            if Product.objects.filter(techland=techland).exists():
                product = Product.objects.get(techland=techland)
            else:
                product = Product.objects.create(techland=techland)
            product.name = name
            product.brand = brand
            product.model = model
            product.image = image
            product.sub_category = sub_category
            product.save()          
        elif Product.objects.filter(brand=brand, model=model).exists():
            techland = Techland.objects.create(link=url, price=price, regular_price=regular_price, status=status)
            techland.save()
            product = Product.objects.filter(brand=brand, model=model)[0]
            product.name = name
            product.image = image
            product.sub_category = sub_category
            product.techland = techland
            product.save()
        else:
            techland = Techland.objects.create(link=url, price=price, regular_price=regular_price, status=status)
            techland.save()
            product = Product.objects.create(name=name, brand=brand, model=model, image=image, sub_category=sub_category, techland=techland)
            product.save()
        feature_tab = ""
        if soup.find('div', {'id': 'tab-specification'}):
            feature_tab = soup.find('div', {'id': 'tab-specification'}).find('tbody')
        elif soup.find('div', {'class': 'block-content  block-description'}):
            feature_tab = soup.find('div', {'class': 'block-content  block-description'})
        if feature_tab and feature_tab.find('tr'):
            for row in feature_tab.findAll('tr'):
                feature = row.findAll('td')[0].text[:255]
                value = row.findAll('td')[1].text.replace('\n', '<br>')[:255]
                if Feature.objects.filter(product=product, name=feature).exists():
                    feature = Feature.objects.get(product=product, name=feature)
                    feature.value = value
                    feature.save()
                else:
                    feature_obj = Feature.objects.create(product=product, name=feature, value=value)
                    feature_obj.save()
                    
        print('Loaded : ' + name)
        

    except Exception as e:
        print("Error loading " + url)
        print(e)




def load_from_techland():
    print("Loading from Techland")
    links_data_arr = get_urls_of_xml("https://www.techlandbd.com/sitemaps/product-sitemap.xml")
    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
        executor.map(get_product_data, links_data_arr)
    print("Loading from Techland Complete")

