"""This file holds the portfolio class."""

import json
from classes.share import Share

class Portfolio(object):
    """This class will model a portfolio of shares."""

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
        with open(filename, "r") as portfolio:
            shares = json.load(portfolio)
            for share in shares:
                tmp = Share(share,
                            shares[share]['Owned'],
                            shares[share]['Percentage'],
                            shares[share]['MorningstarID'])
                self.shares.append(tmp)
        self.update_meta_info()

    def save(self, filename):
        """Saves the state of a portfolio to a json file."""
        portfolio_data = self.get_json()
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
            portfolio_data[share.ticker] = share_info
        return portfolio_data

    # Buying and selling shares

    def buy_shares(self, ticker, number_of_shares):
        """Tool to buy a certain amount of a given share."""
        share = next((share for share in self.shares if share.ticker == ticker), None)
        share.buy(number_of_shares)
        self.update_meta_info()

    def sell_shares(self, ticker, number_of_shares):
        """Tool to sell a certain amount of a given share."""
        share = next((share for share in self.shares if share.ticker == ticker), None)
        assert share is not None, "Can't sell what you don't have"
        assert number_of_shares <= share.number_owned, "Not enough shares to sell"
        share.sell(number_of_shares)
        self.update_meta_info()

    def invest(self, amount_to_invest):
        """Suggests what shares to buy to maintain the appropriate
        distribution of shares in the portfolio.
        """
        self.update_meta_info()
        left_to_sell = amount_to_invest
        shares_to_buy = {}
        while left_to_sell >= min(share.price * 1.05 for share in self.shares):
            share_to_buy = min(self.percentage_diffs, key=self.percentage_diffs.get)
            self.buy_shares(share_to_buy.ticker, 1)
            left_to_sell -= share_to_buy.price * 1.05
            if share_to_buy not in shares_to_buy:
                shares_to_buy[share_to_buy] = 1
            else:
                shares_to_buy[share_to_buy] += 1
        for share in shares_to_buy:
            print(f'Buy {shares_to_buy[share]} shares of {share.ticker}')

    # Updating info

    def update_meta_info(self):
        """Updates all the metadata for the portfolio."""

        def update_total_investment(portfolio):
            """Updates the total amount invested in the portfolio."""
            total = 0
            for share in portfolio.shares:
                total += share.value_of_holding
            portfolio.total_invested = total

        def update_actual_percentages(portfolio):
            """Updates the actual percentages that specific shares are of the portfolio."""
            actual_percentages = {}
            for share in portfolio.shares:
                actual = (share.value_of_holding * 100) / portfolio.total_invested
                actual_percentages[share] = actual
            portfolio.actual_percentages = actual_percentages

        def update_percentage_diffs(portfolio):
            """Updates how close the percentage of a particular share
            in the portfolio is to its aim percentage.
            """
            percentage_diffs = {}
            for share in portfolio.actual_percentages:
                diff = ((portfolio.actual_percentages[share] * 100) / share.aim_percentage) - 100
                percentage_diffs[share] = diff
            portfolio.percentage_diffs = percentage_diffs

        update_total_investment(self)
        update_actual_percentages(self)
        update_percentage_diffs(self)
