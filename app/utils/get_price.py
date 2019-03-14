"""Functions relating to getting the price of a security."""

import re
from urllib.request import urlopen
from bs4 import BeautifulSoup

def get_price(morningstar_id):
    """Returns the price from morningstar given its Morningstar ID."""
    quote_page = "http://www.morningstar.co.uk/uk/etf/snapshot/snapshot.aspx?id=" + morningstar_id
    page = urlopen(quote_page)
    soup = BeautifulSoup(page, 'html.parser')
    price_box = soup.find('td', attrs={'class':'line text'})
    price_element = price_box.text
    price_raw = re.sub(r'[A-z ]', "", price_element)
    price = float(price_raw) / 100
    return price
