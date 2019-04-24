import unittest
import os
from datetime import datetime
from app.classes.portfolio import Portfolio
from app.classes.share import Share


class TestPortfolio(unittest.TestCase):

    def setup(self):
        timestamp = datetime.utcnow().timestamp()

        share1_price_data = [25.00, timestamp]
        share2_price_data = [49.00, timestamp]

        share1_data_object = {"Ticker": "ABC", "Owned": 2, "Percentage": 50, "MorningstarID": "0P0000YWPH",
                              "Price": share1_price_data, "Holding": 50.00}
        share2_data_object = {"Ticker": "XYZ", "Owned": 1, "Percentage": 50, "MorningstarID": "0P0000YWPH",
                              "Price": share2_price_data, "Holding": 49.00}

        self.test_share1 = Share(share1_data_object)
        self.test_share2 = Share(share2_data_object)

        self.test_portfolio = Portfolio([self.test_share1, self.test_share2])

    def test_empty_setup(self):
        self.test_portfolio = Portfolio()

        self.assertEqual(self.test_portfolio.shares, [],
                         "There should be no shares")
        self.assertEqual(self.test_portfolio.actual_percentages,
                         {}, "There should be no metadata")
        self.assertEqual(self.test_portfolio.percentage_diffs,
                         {}, "There should be no metadata")
        self.assertEqual(self.test_portfolio.total_invested,
                         0, "Total invested should be 0")

    def test_total_invested(self):
        self.setup()

        self.assertEqual(self.test_portfolio.total_invested, 99,
                         "Total invested calculated incorrectly")

    def test_actual_percentages(self):
        self.setup()

        expected = [50.51, 49.49]

        for index, share in enumerate(self.test_portfolio.shares):
            self.assertEqual(
                expected[index], self.test_portfolio.actual_percentages[share])

    def test_percentage_diffs(self):
        self.setup()

        expected = [1.02, -1.02]

        for index, share in enumerate(self.test_portfolio.shares):
            self.assertEqual(
                expected[index], self.test_portfolio.percentage_diffs[share])

    def test_load(self):
        self.test_portfolio = Portfolio()
        portfolio_path = os.path.abspath("data/test_load_portfolio.json")
        self.test_portfolio.load(portfolio_path)

        share1 = {"Ticker": "ABC", "Owned": 8,
                  "Percentage": 30, "MorningstarID": "0P0000YWPH"}
        share2 = {"Ticker": "MNO", "Owned": 8,
                  "Percentage": 30, "MorningstarID": "0P0000WAHF"}
        share3 = {"Ticker": "XYZ", "Owned": 12,
                  "Percentage": 40, "MorningstarID": "0P0000WAHG"}

        self.test_shares = [share1, share2, share3]

        self.assertEqual(len(self.test_portfolio.shares), 3,
                         "Incorrect number of shares after load")

        for index, share in enumerate(self.test_portfolio.shares):
            test_share = self.test_shares[index]

            self.assertEqual(test_share["Ticker"],
                             share.ticker, "Tickers incorrect")
            self.assertEqual(
                test_share["Owned"], share.number_owned, "Number owned incorrect")
            self.assertEqual(test_share["Percentage"], share.aim_percentage,
                             "Aim percentage incorrect")
            self.assertEqual(test_share["MorningstarID"], share.morningstar_id,
                             "Morningstar ID incorrect")

    def test_save(self):
        self.setup()

        portfolio_path = os.path.abspath("data/test_save_portfolio")
        self.test_portfolio.save(portfolio_path)

    def test_str(self):
        self.setup()

        expected = ("----\n"
                    "Stock: ABC\n"
                    "Owned: 2\n"
                    "Price: £25.0\n"
                    "Aim of portfolio: 50%\n"
                    "Actual of portfolio: 50.51%\n"
                    "Ratio diff: 1.02%\n"
                    "----\n"
                    "Stock: XYZ\n"
                    "Owned: 1\n"
                    "Price: £49.0\n"
                    "Aim of portfolio: 50%\n"
                    "Actual of portfolio: 49.49%\n"
                    "Ratio diff: -1.02%\n"
                    "----\n"
                    "Total invested: £99.0")

        self.assertEqual(str(self.test_portfolio),
                         expected, "Printing wrong summary")

    def test_get_json(self):
        self.setup()

    def test_buy_shares(self):
        self.setup()

        self.test_portfolio.buy_shares("ABC", 100)

        test_share = self.test_portfolio.get_share("ABC")

        self.assertEqual(test_share.number_owned, 102,
                         "Incorrect number of shares after buying more")

    def test_sell_shares(self):
        self.setup()

        test_share = self.test_portfolio.get_share("ABC")

        self.test_portfolio.sell_shares("ABC", 1)
        self.assertEqual(test_share.number_owned, 1,
                         "Incorrect number of shares after buying more")

        self.assertFalse(self.test_portfolio.sell_shares("ABC", 100),
                         "Incorrect number of shares after buying more")

    def test_invest(self):
        self.setup()

        advice = self.test_portfolio.invest(500)

        self.assertEqual(advice["ABC"], 9, "Wrong number of shares to buy")
        self.assertEqual(advice["XYZ"], 5, "Wrong number of shares to buy")

    def test_get_share(self):
        self.setup()

        valid_share = self.test_portfolio.get_share("ABC")
        self.assertTrue(valid_share, "Shares not returned properly")

        invlaid_share = self.test_portfolio.get_share("1234")
        self.assertFalse(invlaid_share, "Invalid shares not handled properly")


if __name__ == '__main__':
    unittest.main()
