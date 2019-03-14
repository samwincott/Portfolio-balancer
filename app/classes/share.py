"""This file contains the share class."""

import datetime
from utils.get_price import get_price

class Share(object):
    """This class represents a share,
    and its metadata with respect to a portfolio.
    """

    def __init__(self, ticker, owned, percentage_of_portfolio, morningstar_id):
        self.ticker = ticker
        self.number_owned = owned
        self.aim_percentage = percentage_of_portfolio
        self.morningstar_id = morningstar_id
        self._price = 0
        self.price_date = datetime.datetime(2018, 1, 1)
        self._value_of_holding = 0

    def buy(self, amount):
        """Buy more of this specific share."""
        assert amount is not None, "Can't sell what you don't have"
        self.number_owned += amount

    def sell(self, amount):
        """Sell this specific share."""
        self.number_owned -= amount

    @property
    def value_of_holding(self):
        """Return the current value of this holding."""
        return self.price * self.number_owned

    @property
    def price(self):
        """Returns the price of the share.
        Caches recent prices to reduce API calls.
        """
        if self.price_date.timestamp() < datetime.datetime.utcnow().timestamp() - 86400:
            print(f'Retrieving current price for {self.ticker}')
            self._price = get_price(self.morningstar_id)
            self.price_date = datetime.datetime.utcnow()
        return self._price

    def __str__(self):
        """Outputs the information for this holding."""
        string = ""

        string += f'Share name: {self.ticker}\n'
        string += f'Number owned: {self.number_owned}\n'
        string += f'Current price: £{self.price}\n'
        string += f'Aim percentage: {self.aim_percentage}%'

        return string
