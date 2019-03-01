from utils.get_price import get_price
import datetime

class Share(object):

    def __init__(self, ticker, owned, percentage_of_portfolio, morningstar_id):
        self.ticker = ticker
        self.owned = owned
        self.aim_percentage_of_portfolio = percentage_of_portfolio
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
    
    def get_price_date(self):
        return self.price_date

    def get_morningstar_id(self):
        return self.morningstar_id
    
    def get_aim_percentage(self):
        return self.aim_percentage_of_portfolio
    
    def set_aim_percentage(self, aim):
        self.aim_percentage_of_portfolio = aim
    
    def pretty_print(self):
        print("Share name: %s" % (self.get_ticker()))
        print("Number owned: %d " % (self.get_number_owned()))
        print("Current price: £%.2f " % (self.get_price()))
        print("Aim percentage: %d%%" % (self.get_aim_percentage()))
