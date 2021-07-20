from os import close
import pandas
from datetime import datetime, timedelta
import csv

class portfolio:
    def __init__(self, cash, file_name, start_date: datetime, prices_df: pandas.DataFrame):
        self.value = cash
        self.cash = cash
        self.portfolio = {}
        self.writer = csv.writer(open(file_name, 'w'), delimiter=',')
        self.cur_day = start_date
        self.prices_df = prices_df.set_index('Date', drop=True, append=True, inplace=False)
    
    # dollar amount takes precedence over shares
    def buy(self, ticker, shares=100, dollar_amount=None):
        if (ticker not in self.portfolio.keys()):
            self.portfolio[ticker] = 0
        try:
            cur_price = self.prices_df.loc[ticker, self.cur_day.strftime("%Y-%m-%d")]['Close']
        except:
            raise IndexError("Couldn't find closing price on when trying to buy {} on {}".format(ticker, self.cur_day.strftime("%Y-%m-%d")))

        if (dollar_amount != None):
            if (dollar_amount > self.cash):
                raise ValueError('You do not have enough cash to purchase ${} of {}'.format(dollar_amount, ticker))
            units = dollar_amount / cur_price
            self.portfolio[ticker] = self.portfolio[ticker] + units
            self.upload_trade(0, ticker, self.cur_day, units)
            self.cash -= dollar_amount

        else:
            if (shares * cur_price > self.cash):
                raise ValueError('You do not have enough cash to purchase {} shares of {}'.format(shares, ticker))
            self.portfolio[ticker] = self.portfolio[ticker] + shares
            self.upload_trade(0, ticker, self.cur_day, shares)
            self.cash -= shares * cur_price

        self.update_value()

    #dollar amount takes precedence over shares
    def sell(self, ticker, shares=100, dollar_amount=None):
        if (ticker not in self.portfolio.keys()):
            raise ValueError('You do not own shares of {} and cannot sell it'.format(ticker))

        try:
            cur_price = self.prices_df.loc[ticker, self.cur_day.strftime("%Y-%m-%d")]['Close']
        except:
            raise IndexError("Couldn't find closing price on when trying to sell {}".format(ticker))

        if (dollar_amount != None):
            if (self.portfolio[ticker] * cur_price < dollar_amount):
                raise ValueError('You do not have ${} of {} to sell'.format(dollar_amount, ticker))
            units = dollar_amount / cur_price
            self.portfolio[ticker] = self.portfolio[ticker] - units
            self.upload_trade(1, ticker, self.cur_day, units)
            self.cash += dollar_amount

        else:
            if (self.portfolio[ticker] < shares):
                raise ValueError("You do not have enough shares of {} to sell!".format(ticker))
            self.portfolio[ticker] = self.portfolio[ticker] - shares
            self.upload_trade(1, ticker, self.cur_day, shares)
            self.cash += shares * cur_price

        self.update_value()

    def upload_trade(self, trade, ticker, date, shares):
        trade_type = ['Buy', 'Sell']
        self.writer.writerow([ticker, trade_type[trade], date, shares])

    def update_value(self):
        new_value = self.cash
        for ticker, shares in self.portfolio.items():
            try:
                share_price = self.prices_df.loc[ticker, self.cur_day.strftime("%Y-%m-%d")]['Close']
                new_value = new_value + (share_price * shares)
            except (ValueError, KeyError):
                raise IndexError("Couldn't find the share price when calculating value of portfolio!")
        self.value = new_value
        return self.value

    def new_day(self, days=1):
        self.cur_day += timedelta(days)
        try:
            self.update_value()
        except:
            pass

    def get_portfolio(self):
        portfolio_instance = self.portfolio
        for position in portfolio_instance:
            if (portfolio_instance[position] == 0):
                portfolio_instance.pop(position)
        return portfolio_instance


