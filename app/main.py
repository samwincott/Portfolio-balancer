"""Main file for project."""

from interface.main import run_interface
from classes.portfolio import Portfolio

def main():
    my_portfolio = Portfolio()
    run_interface(my_portfolio)

if __name__ == '__main__':
    main()

# help
# load portfolio
# save portfolio
# display share info
# add money
# add money with balancer
# sell shares
# sell shares with balancer
# display info
