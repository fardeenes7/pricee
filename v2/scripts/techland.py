import concurrent.futures
from bs4 import BeautifulSoup
import requests
from ..models import Product, Category, SubCategory, Feature, Techland

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


colors = ['black', 'white', 'red', 'blue', 'green', 'yellow', 'orange', 'purple', 'pink', 'brown', 'grey', 'gray', 'silver', 'gold', 'golden', 'beige', 'multicolor', 'clear', 'other', 'ruby', 'copper', 'lavender', 'lilac']
def get_color(text):
    text = text.lower()
    for color in colors:
        if color in text:
            return color
    return ""

# session = requests.Session()
def get_product_data(url):
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, features='lxml')
        name = soup.find('div', {'class': 'title page-title'}).text.strip() if soup.find('div', {'class': 'title page-title'}) else ""
        price = int(soup.find('div', 'product-price-group').find('div', {'class': 'product-price'}).text.replace(',', '').replace('৳', '').strip()) if soup.find('div', {'class': 'product-price-group'}) else 0

        regular_price = int(soup.find('div', 'product-price-group').find('div', {'class': 'module-item-2'}).find('span', {'class': "block-header-text"}).text.replace(',', '').replace('৳', '').strip()) if soup.find('div', {'class': 'product-price-group'}) else 0
        st = soup.find('div', {'class': 'product-details'}).find_all('tr')
        for i in st:
            if i.find_all('td')[0].text == 'Stock Status':
                status = i.find_all('td')[1].text
                break
        status = status.strip() if status else "N/A"
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
            category = Category.objects.create(name=category) if len(category) <= 20 else Category.objects.get_or_create(name='Others')[0]
            category.save()
        if SubCategory.objects.filter(name=sub_category, category = category).exists():
            sub_category = SubCategory.objects.filter(name=sub_category, category = category)[0]
        else:
            sub_category = SubCategory.objects.create(name=sub_category, category=category) if len(sub_category) <=20 else SubCategory.objects.get_or_create(name='Others', category=category)[0]
            sub_category.save()

        brand = brand if brand!="" else name.split()[0]
        model = model if model!="" else name.split()[1]

        if Techland.objects.filter(link=url).exists():
            techland = Techland.objects.get(link=url)
            techland.price = price
            techland.regular_price = regular_price
            techland.status = status
            techland.save()
            product = Product.objects.get_or_create(techland=techland)[0]
            product.name = name
            product.brand = brand
            product.model = model
            product.image = image
            product.sub_category = sub_category
            product.save()          
        elif Product.objects.filter(brand=brand, model=model).exists():
            techland = Techland.objects.create(link=url, price=price, regular_price=regular_price, status=status)
            techland.save()
            product = Product.objects.get_or_create(brand=brand, model=model, name=name)[0]
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
        """
        category, created = Category.objects.get_or_create(name=category)
        if len(category.name) > 20:
            category.delete()
            category = Category.objects.get_or_create(name='Others')


        sub_category, created = SubCategory.objects.get_or_create(name=sub_category, category=category)

        techland, created = Techland.objects.get_or_create(link=url, defaults={'price': price, 'regular_price': regular_price, 'status': status})

        product, created = Product.objects.get_or_create(brand=brand, model=model, techland=techland, defaults={'name': name, 'image': image, 'sub_category': sub_category})

        feature_tab = ""
        if soup.find('div', {'id': 'tab-specification'}):
            feature_tab = soup.find('div', {'id': 'tab-specification'}).find('tbody')
        elif soup.find('div', {'class': 'block-content  block-description'}):
            feature_tab = soup.find('div', {'class': 'block-content  block-description'})

        if feature_tab and feature_tab.find('tr'):
            for row in feature_tab.findAll('tr'):
                feature = row.findAll('td')[0].text[:255]
                value = row.findAll('td')[1].text.replace('\n', '<br>')[:255]
                Feature.objects.get_or_create(product=product, name=feature, defaults={'value': value})

        print('Loaded:', name)
"""

    except Exception as e:
        print("Error loading " + url)
        print(e)




def load_from_techland():
    print("Loading from Techland")
    links_data_arr = get_urls_of_xml("https://www.techlandbd.com/sitemaps/product-sitemap.xml")
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        executor.map(get_product_data, links_data_arr)
    print("Loading from Techland Complete")

