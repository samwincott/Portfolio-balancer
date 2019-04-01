import unittest
from datetime import datetime
from app.classes.portfolio import Portfolio
from app.classes.share import Share

class TestPortfolio(unittest.TestCase):

    def setup(self):
        timestamp=datetime.utcnow().timestamp()

        share1_price_data = [25.00, timestamp]
        share2_price_data = [49.00, timestamp]

        share1_data_object = {"Owned": 2, "Percentage": 50, "MorningstarID": "0P0000YWPH", "Price": share1_price_data, "Holding": 50.00}
        share2_data_object = {"Owned": 1, "Percentage": 50, "MorningstarID": "0P0000YWPH", "Price": share2_price_data, "Holding": 49.00}

        self.test_share1 = Share("ABC", share1_data_object)
        self.test_share2 = Share("XYZ", share2_data_object)

        self.test_portfolio = Portfolio([self.test_share1, self.test_share2])
    
    def test_empty_setup(self):
        self.test_portfolio = Portfolio()

        self.assertEqual(self.test_portfolio.shares, [], "There should be no shares")
        self.assertEqual(self.test_portfolio.actual_percentages, {}, "There should be no metadata")
        self.assertEqual(self.test_portfolio.percentage_diffs, {}, "There should be no metadata")
        self.assertEqual(self.test_portfolio.total_invested, 0, "Total invested should be 0")

    def test_total_invested(self):
        self.setup()

        self.assertEqual(self.test_portfolio.total_invested, 99, "Total invested calculated incorrectly")

    def test_actual_percentages(self):
        self.setup()

        expected = [50.51, 49.49]

        for index, share in enumerate(self.test_portfolio.shares):
            self.assertEqual(expected[index], self.test_portfolio.actual_percentages[share])

    def test_percentage_diffs(self):
        self.setup()

        expected = [1.02, -1.02]

        for index, share in enumerate(self.test_portfolio.shares):
            self.assertEqual(expected[index], self.test_portfolio.percentage_diffs[share])

    def test_load(self):
        self.test_portfolio = Portfolio()
        self.test_portfolio.load("/Users/Sam/repos/lazy-balancer/data/test_portfolio.json")

        share1 = {"Ticker": "ABC", "Owned": 8, "Percentage": 30, "MorningstarID": "0P0000YWPH"}
        share2 = {"Ticker": "MNO", "Owned": 8, "Percentage": 30, "MorningstarID": "0P0000WAHF"}
        share3 = {"Ticker": "XYZ", "Owned": 12, "Percentage": 40, "MorningstarID": "0P0000WAHG"}

        self.test_shares = [share1, share2, share3]

        self.assertEqual(len(self.test_portfolio.shares), 3, "Incorrect number of shares after load")

        for index, share in enumerate(self.test_portfolio.shares):
            test_share = self.test_shares[index]

            self.assertEqual(test_share["Ticker"], share.ticker, "Tickers incorrect")
            self.assertEqual(test_share["Owned"], share.number_owned, "Number owned incorrect")
            self.assertEqual(test_share["Percentage"], share.aim_percentage, "Aim percentage incorrect")
            self.assertEqual(test_share["MorningstarID"], share.morningstar_id, "Morningstar ID incorrect")

if __name__ == '__main__':
    unittest.main()
