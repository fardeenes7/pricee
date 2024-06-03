from bs4 import BeautifulSoup
import requests
from django.template.defaultfilters import slugify
from ..models import Category, SubCategory, Image, Product, Link
import re

def get_urls_of_xml(xml_url, feature):
    r = requests.get(xml_url)
    soup = BeautifulSoup(r.text, features=feature)
    links_arr = []
    for link in soup.findAll('loc'):
        linkstr = link.getText('', True)
        links_arr.append(linkstr)

    return links_arr


def removeBrand(brand, model):
    brand = brand.lower().replace(' ', '').replace('-', '').strip()
    model = model.lower().replace(brand, '').strip().upper()
    return re.sub(r'\([^()]*\)', '', model)


def set_category(category_name, sub_category_name):
    if SubCategory.objects.filter(name=category_name).exists():
        try:
            return SubCategory.objects.get(name=category_name)
        except:
            return SubCategory.objects.filter(name=category_name)[0]
    else:
        if len(category_name) <= 20:
            try:
                category = Category.objects.get_or_create(name=category_name)[0]
            except:
                category = Category.objects.filter(name=category_name)[0]
        else:
            try:
                category = Category.objects.get_or_create(name='Others')[0]
            except:
                category = Category.objects.filter(name='Others')[0]
        category.save()
        if len(sub_category_name) <= 20:
            try:
                sub_category = SubCategory.objects.get_or_create(name=sub_category_name)[0]
            except:
                sub_category = SubCategory.objects.filter(name=sub_category_name)[0]
        else:
            try:
                sub_category = SubCategory.objects.get_or_create(name='Others')[0]
            except:
                sub_category = SubCategory.objects.filter(name='Others')[0]
        sub_category.category = sub_category.category if sub_category.category else category
        sub_category.save()
        """
        if not SubCategory.objects.filter(name=sub_category_name).exists():
            sub_category = SubCategory.objects.create(name=sub_category_name, category=category) if len(sub_category_name) <= 20 else SubCategory.objects.get_or_create(name='Others', category=category)[0]
            sub_category.save()
        else:
            sub_category = SubCategory.objects.get(name=sub_category_name)
        """
        return sub_category


def save_images(product, images):
    for image in images:
        if not Image.objects.filter(product=product, href=image).exists():
            Image.objects.create(product=product, href=image)


def save_product(brand, model, name, subcategory, shop, url, price, status):
    if Product.objects.filter(brand_slug = slugify(brand), model_slug = slugify(model)).exists():
        product = Product.objects.filter(brand_slug = slugify(brand), model_slug = slugify(model))[0]
        product.name = name if not product.name else product.name
        product.sub_category = subcategory if not product.sub_category else product.sub_category
        product.brand = brand if not product.brand else product.brand
        product.model = model if not product.model else product.model
        product.save()
    else:
        product = Product.objects.create(name=name, sub_category=subcategory, brand=brand, model=model)
        product.save()

    Link.objects.get_or_create(product=product, shop=shop, href=url, price=price, status=status)

    return product



colors = ['black', 'white', 'red', 'blue', 'green', 'yellow', 'orange', 'purple', 'pink', 'brown', 'grey', 'gray', 'silver', 'gold', 'golden', 'beige', 'multicolor', 'clear', 'other', 'ruby', 'copper', 'lavender', 'lilac']
def get_color(text):
    text = text.lower()
    for color in colors:
        if color in text:
            return color
    return ""


def printRed(skk):
    print("\033[91m {}\033[00m" .format(skk))
 
 
def printGreen(skk):
    print("\033[92m {}\033[00m" .format(skk))