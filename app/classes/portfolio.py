"""This file holds the portfolio class."""

import json
import os
from app.classes.share import Share


class Portfolio(object):
    """This class will model a portfolio of shares."""

    PRICE_DEVIATION = 1.05

    def __init__(self, shares=None):
        if shares is None:
            self.shares = []
        else:
            self.shares = shares
        self.actual_percentages = {}
        self.percentage_diffs = {}
        self.total_invested = 0
        self.update_meta_info()

    def load(self, filename):
        """Loads in portfolio information from a json file."""
        # Remove previous share data
        if self.shares:
            self.shares = []

        # Load in new data
        with open(filename, "r") as portfolio:
            file_contents = json.load(portfolio)
            for share in file_contents["shares"]:
                tmp = Share(share)
                self.shares.append(tmp)

        self.update_meta_info()

    def save(self, filename):
        """Saves the state of a portfolio to a json file."""
        portfolio_data = self.get_json()
        filename += ".json"
        with open(filename, 'w') as outfile:
            json.dump(portfolio_data, outfile)

    # Printing

    def __str__(self):
        """Outputs the portfolio information to the console."""
        return_string = ""
        for share in self.shares:
            return_string += '----\n'
            return_string += f'Stock: {share.ticker}\n'
            return_string += f'Owned: {share.number_owned}\n'
            return_string += f'Price: £{round(share.price, 2)}\n'
            return_string += f'Aim of portfolio: {round(share.aim_percentage, 2)}%\n'
            return_string += f'Actual of portfolio: {round(self.actual_percentages[share], 2)}%\n'
            return_string += f'Ratio diff: {round(self.percentage_diffs[share], 2)}%\n'
        return_string += '----\n'
        return_string += f'Total invested: £{round(self.total_invested, 2)}'
        return return_string

    def get_json(self):
        """Returns all current data in json format."""
        portfolio_data = {}
        for share in self.shares:
            share_info = {}
            share_info["Owned"] = share.number_owned
            share_info["Percentage"] = share.aim_percentage
            share_info["MorningstarID"] = share.morningstar_id
            share_info["Price"] = (share.price, share.price_date.__str__())
            share_info["Holding"] = share.value_of_holding
            portfolio_data[share.ticker] = share_info
        return portfolio_data

    # Buying and selling shares

    def buy_shares(self, ticker, number_of_shares):
        """Tool to buy a certain amount of a given share."""
        share = next(
            (share for share in self.shares if share.ticker == ticker), None)
        assert share is not None, "This ticker is not part of the portfolio currently."
        share.buy(number_of_shares)

        self.update_meta_info()

    def sell_shares(self, ticker, number_of_shares):
        """Tool to sell a certain amount of a given share."""
        share = next(
            (share for share in self.shares if share.ticker == ticker), None)
        assert share is not None, "You don't have any holdings for this ticker."

        share.sell(number_of_shares)

        self.update_meta_info()

    def invest(self, amount_to_invest):
        """Suggests what shares to buy to maintain the appropriate
        distribution of shares in the portfolio.
        """
        self.update_meta_info()
        shares_to_buy = {}
        # The price may deviate slightly between running this program and the order being executed

        while amount_to_invest >= min(share.price * self.PRICE_DEVIATION for share in self.shares):
            share_to_buy = min(self.percentage_diffs,
                               key=self.percentage_diffs.get)
            self.buy_shares(share_to_buy.ticker, 1)
            amount_to_invest -= share_to_buy.price * self.PRICE_DEVIATION
            try:
                shares_to_buy[share_to_buy] += 1
            except:
                shares_to_buy[share_to_buy] = 1

        advice = "Buy:\n"
        for share in shares_to_buy:
            advice += f'{shares_to_buy[share]} shares of {share.ticker} at {share.price*1.05*shares_to_buy[share]}\n'

        return advice

    # Updating info

    def update_meta_info(self):
        """Updates all the metadata for the portfolio."""

        # Update total value of portfolio
        self.total_invested = sum(
            share.value_of_holding for share in self.shares)

        # Update the actual percentages that invidual holdings are of the portfolio
        def actual_percentages(value, total): return round(
            ((value * 100) / total), 2)
        self.actual_percentages = {share: actual_percentages(
            share.value_of_holding, self.total_invested) for share in self.shares}

        # Update the difference between actual and aim percentage of a holding in the portfolio
        def ratio_diffs(actual, aim): return round(
            (((actual * 100) / aim) - 100), 2)
        self.percentage_diffs = {share: ratio_diffs(
            self.actual_percentages[share], share.aim_percentage) for share in self.shares}

    def get_share(self, ticker):
        share = next(
            (share for share in self.shares if share.ticker == ticker), None)
        return share
