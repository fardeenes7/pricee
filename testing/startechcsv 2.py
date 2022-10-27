import concurrent.futures
from bs4 import BeautifulSoup
import requests
import csv
import time
from datetime import datetime
date = datetime.now().date
print(date)

def get_urls_of_xml(xml_url):
    r = requests.get(xml_url)
    xml = r.text
    soup = BeautifulSoup(xml)
    links_arr = []
    for link in soup.findAll('loc'):
        linkstr = link.getText('', True)
        links_arr.append(linkstr)

    return links_arr

product_details_data = []

def get_product_data(url):
    print("Getting data from " + url)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    detail = {}
    detail["name"] = soup.find('h1', {'class': 'product-name'}).text if soup.find('h1', {'class': 'product-name'}) else ""
    detail["price"]= soup.find('td', {'class': 'product-info-data product-price'}).text if soup.find('td', {'class': 'product-info-data product-price'}) else ""
    detail["regular_price"]= soup.find('td', {'class': 'product-info-data product-regular-price'}).text if soup.find('td', {'class': 'product-info-data product-regular-price'}) else ""
    detail["status"]= soup.find('td', {'class': 'product-info-data product-status'}).text if soup.find('td', {'class': 'product-info-data product-status'}) else ""
    detail["sku" ]= soup.find('td', {'class': 'product-info-data product-code'}).text if soup.find('td', {'class': 'product-info-data product-code'}) else ""
    detail["brand"]= soup.find('td', {'class': 'product-info-data product-brand'}).text if soup.find('td', {'class': 'product-info-data product-brand'}) else ""
    detail["image"]= soup.find('img', {'class': 'main-img'})['src'] if soup.find('img', {'class': 'main-img'}) else ""
    features = []
    for a,b in zip(soup.findAll('td', {'class': 'name'}), soup.findAll('td', {'class': 'value'}), ):
        features.append({a.text: b.text}) if a.text and b.text else ""
    detail["features"] =features if features else ""
    product_details_data.append(detail)




def writeToCSV(data):
    with open('test2.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = ["name", "price", "regular_price", "status", "sku", "brand", "image", "features"])
        writer.writeheader()
        writer.writerows(data)



start_time = time.time()
links_data_arr = get_urls_of_xml("https://www.startech.com.bd/sitemap.xml")
print(f"Got {str(len(links_data_arr))} links in {str((time.time() - start_time))} seconds")

with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
    executor.map(get_product_data, links_data_arr[1336:2336])

print("Writing Data to CSV")
writeToCSV(product_details_data)

print(f"--- Scraped and saved {int(len(product_details_data))} products into csv ---")
print("--- %s seconds ---" % (time.time() - start_time))