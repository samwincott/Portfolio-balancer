import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd


class Portfolio(object):

    def __init__(self, shares = []):
        self.shares = shares
        self.actual_percentages = {}
        self.percentage_diffs = {}
        self.total_invested = 0
        self.update_meta_info()
    
    def update_meta_info(self):
        self.update_total_investment()
        self.update_actual_percentages()
        self.update_percentage_diffs()

    def update_total_investment(self):
        total = 0
        for share in self.shares:
            total += share.get_amount_invested()
        self.total_invested = total
            
    def pretty_print(self):
        for share in self.shares:
            print("---")
            print("Stock: %s" % (share.get_ticker()))
            print("ISIN: %s" % (share.get_isin()))
            print("Owned: %s" % (share.get_number_owned()))
            print("Price: £%.2f" % (share.get_price()))
            print("Aim of portfolio: %.2f%%" % (share.get_aim_percentage()))
            print("Actual of portfolio: %.2f%%" % (self.actual_percentages[share]))
            print("Ratio diff: %.2f%%" % (self.percentage_diffs[share]))
        print("----")
        print("Total invested: £%.2f" % (self.total_invested))
    
    def update_actual_percentages(self):
        actual_percentages = {}
        for share in self.shares:
            actual = (share.get_amount_invested() * 100) / self.total_invested
            actual_percentages[share] = actual
        self.actual_percentages = actual_percentages
    
    def update_percentage_diffs(self):
        percentage_diffs = {}
        for share in self.actual_percentages:
            diff = ((self.actual_percentages[share] * 100) / share.get_aim_percentage()) - 100
            percentage_diffs[share] = diff
        self.percentage_diffs = percentage_diffs

    def buy_shares(self, ticker, number_of_shares):
        share = next((share for share in self.shares if share.ticker == ticker), None)
        share.buy(number_of_shares)

    def sell_shares(self, ticker, number_of_shares):
        share = next((share for share in self.shares if share.ticker == ticker), None)
        assert share is not None, "Can't sell what you don't have"
        assert number_of_shares <= share.get_number_owned(), "Not enough shares to sell"
        share.sell(number_of_shares)
        
    def add_with_balancer(self, amount_to_invest):
        self.update_meta_info()
        left_to_invest = amount_to_invest
        shares_to_buy = {}
        while left_to_invest >= min(share.get_price() for share in self.shares):
            share_to_buy = min(self.percentage_diffs, key=self.percentage_diffs.get)
            self.buy_shares(share_to_buy.get_ticker(), 1)
            left_to_invest -= share_to_buy.get_price()
            if not share_to_buy in shares_to_buy:
                shares_to_buy[share_to_buy] = 1
            else:
                shares_to_buy[share_to_buy] += 1
            self.update_meta_info()
        for share_to_buy in shares_to_buy:
            print("Buy %d shares of %s" % (shares_to_buy[share_to_buy], share_to_buy.get_ticker()))