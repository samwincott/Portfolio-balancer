from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

def get_price(id):
    quote_page = "http://www.morningstar.co.uk/uk/etf/snapshot/snapshot.aspx?id=" + id
    page = urlopen(quote_page)
    soup = BeautifulSoup(page, 'html.parser')
    price_box = soup.find('td', attrs={'class':'line text'})
    price_element = price_box.text
    price_raw = re.sub(r'[A-z ]', "", price_element)
    price = float(price_raw) / 100
    return price