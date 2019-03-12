from classes.portfolio import Portfolio

def test_load_from_file():
    new_portfolio = Portfolio()
    new_portfolio.load_from_file('''/Users/Sam/my-repos/lazy_balancer
                                    /src/data/test_portfolio.json''')

def portfolio_tests():
    test_load_from_file()

portfolio_tests()
