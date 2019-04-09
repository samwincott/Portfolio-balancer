import unittest
from datetime import datetime
from app.classes.share import Share


class TestShare(unittest.TestCase):

    def setup(self, timestamp=datetime.utcnow().timestamp()):
        self.timestamp = timestamp
        price_data = [25.00, timestamp]
        data_object = {"Ticker": "VHYL", "Owned": 1, "Percentage": 20,
                       "MorningstarID": "0P0000YWPH", "Price": price_data, "Holding": 25.00}
        self.test_share = Share(data_object)

    def test_init(self):
        self.setup()

        self.assertEqual(self.test_share.ticker, "VHYL", "Should be VHYL")
        self.assertEqual(self.test_share.number_owned, 1, "Should be 1")
        self.assertEqual(self.test_share.aim_percentage, 20, "Should be 20%")
        self.assertEqual(self.test_share.morningstar_id,
                         "0P0000YWPH", "Should be 0P0000YWPH")
        self.assertEqual(self.test_share.price, 25.00, "Should be £25.00")
        self.assertEqual(self.test_share.price_date,
                         self.timestamp, f"Should be {self.timestamp}")
        self.assertEqual(self.test_share.value_of_holding,
                         25.00, "Should be £25.00")

    def test_price_update(self):
        hour_ago_timestamp = float(datetime.utcnow().timestamp()) - 86401
        self.setup(hour_ago_timestamp)

        self.assertTrue(self.test_share.price > 0,
                        "Price should not be uninstantiated")
        self.assertTrue(self.test_share.price_date > hour_ago_timestamp,
                        "Price date should be recent")
        self.assertTrue(self.test_share.value_of_holding == self.test_share.price * 1,
                        "Value of holding incorrect")

    def test_buy(self):
        self.setup()

        self.test_share.buy(100)

        self.assertTrue(self.test_share.number_owned == 101,
                        "Buying shares doesn't work")

    def test_sell(self):
        self.setup()

        self.test_share.sell(1)

        self.assertTrue(self.test_share.number_owned == 0, "Selling shares doesn't work")

    def test_sell_too_many(self):
        self.setup()

        # The share is instantiated with 1 share, this should return false
        result = self.test_share.sell(100)

        self.assertFalse(result, "Selling shares doesn't work")

    def test_str(self):
        self.setup()

        expected_string = """Share name: VHYL\nNumber owned: 1\nCurrent price: £25.0\nAim percentage: 20%"""
        result_string = str(self.test_share)

        self.assertEqual(expected_string, result_string)


if __name__ == '__main__':
    unittest.main()
