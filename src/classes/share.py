class Share(object):

    def __init__(self, ticker, owned, percentage_of_portfolio, isin):
        self.ticker = ticker
        self.price = self.get_price()
        self.owned = owned
        self.aim_percentage_of_portfolio = percentage_of_portfolio
        self.isin = isin
    
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
        return 100.0
    
    def get_isin(self):
        return self.isin
    
    def get_aim_percentage(self):
        return self.aim_percentage_of_portfolio
    
    def set_aim_percentage(self, aim):
        self.aim_percentage_of_portfolio = aim
