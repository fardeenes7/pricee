from bs4 import BeautifulSoup
import requests

def get_urls_of_xml(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    print(soup.prettify()[:10000])

    links_arr = []
    for link in soup.findAll('loc'):
        linkstr = link.getText('', True)
        links_arr.append(linkstr)

    return links_arr



links_data_arr = get_urls_of_xml("https://www.techlandbd.com/sitemaps/product-sitemap.xml")
for link in links_data_arr:
    print(link)

print(len(links_data_arr))
