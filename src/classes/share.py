from utils.get_price import get_price
import datetime

class Share(object):

    def __init__(self, ticker, owned, percentage_of_portfolio, isin, morningstar_id):
        self.ticker = ticker
        self.owned = owned
        self.aim_percentage_of_portfolio = percentage_of_portfolio
        self.isin = isin
        self.morningstar_id = morningstar_id
        self.price_date = datetime.datetime(2018, 1, 1)
        self.price = self.get_price()
    
    def buy(self, amount):
        assert amount is not None, "Can't sell what you don't have"
        self.owned += amount
    
    def sell(self, amount):
        self.owned -= amount
    
    def get_ticker(self):
        return self.ticker

    def get_number_owned(self):
        return self.owned
    
    def get_amount_invested(self):
        return self.price * self.owned
    
    def get_price(self):
        if self.price_date.timestamp() < datetime.datetime.utcnow().timestamp() - 86400:
            self.price = get_price(self.morningstar_id)
            self.price_date = datetime.datetime.utcnow()
        return self.price
    
    def get_isin(self):
        return self.isin
    
    def get_aim_percentage(self):
        return self.aim_percentage_of_portfolio
    
    def set_aim_percentage(self, aim):
        self.aim_percentage_of_portfolio = aim
