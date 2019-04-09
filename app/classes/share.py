"""This file contains the share class."""

import datetime
from app.utils.get_price import get_price

class Share(object):
    """This class represents a share,
    and its metadata with respect to a portfolio.
    """

    def __init__(self, data_object):
        self.ticker = data_object["Ticker"]
        self.number_owned = data_object["Owned"]
        self.aim_percentage = data_object["Percentage"]
        self.morningstar_id = data_object["MorningstarID"]
        try:
            self._price = data_object["Price"][0]
            self.price_date = float(data_object["Price"][1])
            self._value_of_holding = data_object["Holding"]
        except:
            self._price = 0
            self.price_date = datetime.datetime(2018, 1, 1).timestamp()
            self._value_of_holding = 0


    def buy(self, amount):
        """Buy more of this specific share."""
        try:
            self.number_owned += amount
        except:
            self.number_owned = amount

    def sell(self, amount):
        """Sell this specific share."""
        if amount > self.number_owned:
            return False
        self.number_owned -= amount

    @property
    def price(self):
        """Returns the price of the share.
        Caches recent prices to reduce API calls.
        """
        if self.price_date < datetime.datetime.utcnow().timestamp() - 86400:
            self._price = get_price(self.morningstar_id)
            self.price_date = datetime.datetime.utcnow().timestamp()
        return self._price
    
    @property
    def value_of_holding(self):
        return self.price * self.number_owned

    def __str__(self):
        """Outputs the information for this holding."""
        string = ""

        string += f'Share name: {self.ticker}\n'
        string += f'Number owned: {self.number_owned}\n'
        string += f'Current price: £{self.price}\n'
        string += f'Aim percentage: {self.aim_percentage}%'

        return string
