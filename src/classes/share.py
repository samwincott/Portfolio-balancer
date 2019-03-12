"""This file contains the share class."""

import datetime
from utils.get_price import get_price

class Share(object):
    """This class represents a share,
    and its metadata with respect to a portfolio.
    """

    def __init__(self, ticker, owned, percentage_of_portfolio, morningstar_id):
        self.ticker = ticker
        self.owned = owned
        self.aim_percentage_of_portfolio = percentage_of_portfolio
        self.morningstar_id = morningstar_id
        self.price_date = datetime.datetime(2018, 1, 1)
        self.price = self.get_price()

    def buy(self, amount):
        """Buy more of this specific share."""
        assert amount is not None, "Can't sell what you don't have"
        self.owned += amount

    def sell(self, amount):
        """Sell this specific share."""
        self.owned -= amount

    def get_ticker(self):
        """Return the ticker for this share."""
        return self.ticker

    def get_number_owned(self):
        """Return how many of this share are owned."""
        return self.owned

    def get_value_of_holding(self):
        """Return the current value of this holding."""
        return self.price * self.owned

    def get_price(self):
        """Returns the price of the share.
        Caches recent prices to reduce API calls.
        """
        if self.price_date.timestamp() < datetime.datetime.utcnow().timestamp() - 86400:
            print(f'Retrieving current price for {self.ticker}')
            self.price = get_price(self.morningstar_id)
            self.price_date = datetime.datetime.utcnow()
        return self.price

    def get_price_date(self):
        """Return the date when the latest price was retrieved."""
        return self.price_date

    def get_morningstar_id(self):
        """Return the morningstar ID for this share.
        Used to query the price."""
        return self.morningstar_id

    def get_aim_percentage(self):
        """Return the aim percentage of the portfolio for this share."""
        return self.aim_percentage_of_portfolio

    def set_aim_percentage(self, aim):
        """Sets the aim percentage of the portfolio for this share."""
        self.aim_percentage_of_portfolio = aim

    def pretty_print(self):
        """Outputs the information for this holding."""
        print(f'Share name: {self.get_ticker()}')
        print(f'Number owned: {self.get_number_owned()}')
        print(f'Current price: £{self.get_price()}')
        print(f'Aim percentage: {self.get_aim_percentage()}%')
