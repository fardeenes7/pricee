import requests
from bs4 import BeautifulSoup

url = "https://www.startech.com.bd/asus-vp229he-full-hd-monitor"

r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')

#print(soup.prettify())

product_name = soup.find('h1', {'class': 'product-name'}).text

product_price = soup.find('td', {'class': 'product-info-data product-price'}).text

description = soup.find('section', {'class': 'description'}).text

print(product_name + ": "+ product_price + ": " + description)