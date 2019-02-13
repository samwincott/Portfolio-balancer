from classes.portfolio import Portfolio
from classes.share import Share

share1 = Share('VHYL', 9, 25)
share2 = Share('VFEM', 5, 15)
my_shares = [share1, share2]

my_portfolio = Portfolio(my_shares)

my_portfolio.pretty_print()