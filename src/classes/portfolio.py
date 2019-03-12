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

    def load_from_file(self, filename):
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

    def save_to_file(self):
        """Saves the state of a portfolio to a json file."""
        portfolio_data = self.get_json()
        with open('./data/portfolio_save.json', 'w') as outfile:
            json.dump(portfolio_data, outfile)

    # Printing

    def get_data(self):
        """Outputs the portfolio information to the console."""
        return_string = ""
        for share in self.shares:
            return_string += '---\n'
            return_string += f'Stock: {share.get_ticker()}\n'
            return_string += f'Owned: {share.get_number_owned()}\n'
            return_string += f'Price: £{round(share.get_price(), 2)}\n'
            return_string += f'Aim of portfolio: {round(share.get_aim_percentage(), 2)}%\n'
            return_string += f'Actual of portfolio: {round(self.actual_percentages[share], 2)}%\n'
            return_string += f'Ratio diff: {round(self.percentage_diffs[share], 2)}%\n'
        return_string += '----\n'
        return_string += f'Total invested: £{round(self.total_invested, 2)}'
        return return_string
    
    def json_print(self):
        """Prints all current data in json format."""
        print(self.get_json())

    def get_json(self):
        """Returns all current data in json format."""
        portfolio_data = {}
        for share in self.shares:
            share_info = {}
            share_info["Owned"] = share.get_number_owned()
            share_info["Percentage"] = share.get_aim_percentage()
            share_info["MorningstarID"] = share.get_morningstar_id()
            share_info["Price"] = (share.get_price(), share.get_price_date().__str__())
            portfolio_data[share.get_ticker()] = share_info
        return portfolio_data

    def display_share_info(self, input_ticker):
        """Outputs information for a particular share to the console."""
        for share in self.shares:
            if share.get_ticker() == input_ticker:
                share.pretty_print()
                print(f'Actual percentage: {round(self.actual_percentages[share], 2)}')
                print(f'Percentage away from aim: {round(self.percentage_diffs[share], 2)}')
                return
        print("Share not owned")
        return

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
        assert number_of_shares <= share.get_number_owned(), "Not enough shares to sell"
        share.sell(number_of_shares)
        self.update_meta_info()

    def allocate_funds(self, amount_to_invest):
        """Suggests what shares to buy to maintain the appropriate
        distribution of shares in the portfolio.
        """
        self.update_meta_info()
        left_to_sell = amount_to_invest
        shares_to_buy = {}
        while left_to_sell >= min(share.get_price() * 1.05 for share in self.shares):
            share_to_buy = min(self.percentage_diffs, key=self.percentage_diffs.get)
            self.buy_shares(share_to_buy.get_ticker(), 1)
            left_to_sell -= share_to_buy.get_price() * 1.05
            if share_to_buy not in shares_to_buy:
                shares_to_buy[share_to_buy] = 1
            else:
                shares_to_buy[share_to_buy] += 1
        for share in shares_to_buy:
            print(f'Buy {shares_to_buy[share]} shares of {share.get_ticker()}')

    # Updating info

    def update_meta_info(self):
        """Updates all the metadata for the portfolio."""
        self.update_total_investment()
        self.update_actual_percentages()
        self.update_percentage_diffs()

    def update_total_investment(self):
        """Updates the total amount invested in the portfolio."""
        total = 0
        for share in self.shares:
            total += share.get_value_of_holding()
        self.total_invested = total

    def update_actual_percentages(self):
        """Updates the actual percentages that specific shares are of the portfolio."""
        actual_percentages = {}
        for share in self.shares:
            actual = (share.get_value_of_holding() * 100) / self.total_invested
            actual_percentages[share] = actual
        self.actual_percentages = actual_percentages

    def update_percentage_diffs(self):
        """Updates how close the percentage of a particular share
        in the portfolio is to its aim percentage.
        """
        percentage_diffs = {}
        for share in self.actual_percentages:
            diff = ((self.actual_percentages[share] * 100) / share.get_aim_percentage()) - 100
            percentage_diffs[share] = diff
        self.percentage_diffs = percentage_diffs
