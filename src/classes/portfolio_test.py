from classes.portfolio import Portfolio

def test_load():
    new_portfolio = Portfolio()
    new_portfolio.load('''/Users/Sam/my-repos/lazy_balancer
                                    /src/data/test_portfolio.json''')

def portfolio_tests():
    test_load()

portfolio_tests()
