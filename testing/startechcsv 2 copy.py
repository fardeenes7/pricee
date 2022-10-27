import concurrent.futures
from bs4 import BeautifulSoup
import requests
import csv
import time
from datetime import datetime
date = datetime.now().date
print(date)



product_details_data = []

def get_product_data(url):
    print("Getting data from " + url)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    detail = {}
    name = soup.find('h1', {'class': 'product-name'}).text if soup.find('h1', {'class': 'product-name'}) else ""
    price = soup.find('td', {'class': 'product-info-data product-price'}).text if soup.find('td', {'class': 'product-info-data product-price'}) else ""
    regular_price = soup.find('td', {'class': 'product-info-data product-regular-price'}).text if soup.find('td', {'class': 'product-info-data product-regular-price'}) else ""
    status = soup.find('td', {'class': 'product-info-data product-status'}).text if soup.find('td', {'class': 'product-info-data product-status'}) else ""
    brand = soup.find('td', {'class': 'product-info-data product-brand'}).text if soup.find('td', {'class': 'product-info-data product-brand'}) else ""
    model_container = soup.find('div', class_='short-description')
    for m in model_container.findAll('li'):
        if m.text[:5] == 'Model':
            model = m.text[7:]
            print(m.text[7:])
    image = soup.find('img', {'class': 'main-img'})['src'] if soup.find('img', {'class': 'main-img'}) else ""
    features = []
    for a,b in zip(soup.findAll('td', {'class': 'name'}), soup.findAll('td', {'class': 'value'}), ):
        features.append({a.text: b.text}) if a.text and b.text else ""
    product_details_data.append(detail)


get_product_data("https://www.startech.com.bd/apple-macbook-air-13-3-inch-m1-chip-laptop-256gb-ssd")
print(product_details_data)