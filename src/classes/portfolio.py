import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd


class Portfolio(object):

    def __init__(self, shares):
        self.shares = shares
        self.total_invested = self.calculate_total_investment()


    def calculate_total_investment(self):
        total = 0
        for share in self.shares:
            total += share.get_amount_invested()
        return total
            
    def pretty_print(self):
        for share in self.shares:
            print("---")
            print("Stock: %s" % (share.get_ticker()))
            print("Owned: %s" % (share.get_number_owned()))
            print("Price: £%.2f" % (share.get_price()))
            print("Aim of portfolio: %.2f%%" % (share.get_aim_percentage()))
            # print("Actual of portfolio: %.2f%%" % (share.get_actual_percentage(share)))
            # print("Ratio diff: %.2f" % (share.get_ratio_diff(share)))
        print("----")
        print("Total invested: £%.2f" % (self.total_invested))
    
    def update_actual_percentages(self, share):
        for share in self.shares:
            actual = (share.get_amount_invested() * 100) / self.total_invested
            share.set_actual_percentage(actual)
            ratio_diff = actual * 100 / share.get_aim_percentage()
            share.set_aim_actual_diff(ratio_diff)
    
    def update_percentage_diffs(self, share):
        return 60

    def buy_shares(self, ticker, number_of_shares):
        share = next((share for share in self.shares if share.ticker == ticker), None)
        share.buy(number_of_shares)

    def sell_shares(self, ticker, number_of_shares):
        share = next((share for share in self.shares if share.ticker == ticker), None)
        assert share is not None, "Can't sell what you don't have"
        assert number_of_shares <= share.get_number_owned(), "Not enough shares to sell"
        share.sell(number_of_shares)
        
    # def add_with_balancer(self, amount_to_invest):
    #     left_to_invest = amount_to_invest
    #     while left_to_invest >= min(share.get_price() for share in self.shares):
    #         share_to_buy = min(RATIO_DIFF, key=RATIO_DIFF.get)
    #         buy_shares(share_to_buy, 1)
    #         left_to_invest -= PRICES[share_to_buy]
    #         update_actual_ratio()
    #     calc_total()