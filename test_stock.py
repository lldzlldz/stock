import unittest
from stock import stock


class TestStock(unittest.TestCase):
    def setUp(self):
        self.d05 = stock("d05.si")
        self.aapl = stock("aapl")
        self.fb = stock("fb")

    def tearDown(self):
        pass

    def test_price(self):
        d05_price = self.d05.price()
        aapl_price = self.aapl.price()
        print(aapl_price)

        self.assertTrue(isinstance(d05_price, float))
        self.assertTrue(isinstance(aapl_price, float))

        self.assertGreater(float(d05_price), 0)
        self.assertGreater(float(aapl_price), 0)

        print(self.d05.price())
        print(self.aapl.price())

    def test_currency(self):
        self.assertEqual(self.d05.currency(), "SGD")
        self.assertEqual(self.aapl.currency(), "USD")

    # needs to be tested on a stock with consistent dividends
    def test_date(self):
        self.assertRegex(self.d05.ex_dividend_date(), r"20\d{2}-\d{2}-\d{2}")
        self.assertRegex(self.aapl.ex_dividend_date(), r"20\d{2}-\d{2}-\d{2}")

        # since fb does not declare dividends
        with self.assertRaises(KeyError):
            self.fb.ex_dividend_date()


if __name__ == "__main__":
    unittest.main()
