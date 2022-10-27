from bs4 import BeautifulSoup
import concurrent.futures
import requests
import csv
import time
from datetime import datetime
date = datetime.now().date
print(date)
from tabulate import tabulate

def get_urls_of_xml(xml_url):
    r = requests.get(xml_url)
    xml = r.text
    soup = BeautifulSoup(xml)
    links_arr = []
    for link in soup.findAll('loc'):
        linkstr = link.getText('', True)
        links_arr.append(linkstr)

    return links_arr

links_data_arr = get_urls_of_xml("https://www.startech.com.bd/sitemap.xml")
print(f"Got {str(len(links_data_arr))} links")


def get_product_data(url):
    print("Getting data from %s" % url)
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



def writeToCSV(data, filename):
    with open(filename+'.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = ["name", "price", "regular_price", "status", "sku", "brand", "image", "features"])
        writer.writeheader()
        writer.writerows(data)


def driver(n):
    start_time = time.time()
    for link in links_data_arr[1336:1336+n]:
        try:
            get_product_data(link)
        except:
            pass
    writeToCSV(product_details_data, 'single_thread_'+str(n))
    t = time.time() - start_time
    return t

def driver2(n):
    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        executor.map(get_product_data, links_data_arr[1336:1336+n])
    writeToCSV(product_details_data, 'multi_thread_'+str(n))
    t = time.time() - start_time

    return t

data = [['No. of URLs', 'Single Threaded', 'Multithreaded']]
for i in [5,10,20, 50, 100, 500, 1000, 5000, 12000]:
    product_details_data = []
    t1 = driver(i)
    product_details_data = []
    t2 = driver2(i)
    data.append([i, t1, t2])

print('\n\n')
print(tabulate(data, headers='firstrow', tablefmt='fancy_grid'))



