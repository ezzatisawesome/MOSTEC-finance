from os import close
import pandas
from datetime import datetime, timedelta
import csv
import json

class portfolio:

    #weights_url should be a json file while trades_url should be a csv file
    def __init__(self, cash, trades_url, weights_url, prices_df: pandas.DataFrame, start_date: datetime):
        if(trades_url.split('.')[1] != 'csv'):
            raise NameError('Trades url is not a csv file!')
        if(weights_url.split('.')[1] != 'json'):
            raise NameError('Weights url is not a json file!')

        self.value = cash
        self.weights = {}
        self.cash = cash
        self.portfolio = {}
        self.weights_file = weights_url
        self.traders_writer = csv.writer(open(trades_url, 'w'), delimiter=',')
        self.cur_day = start_date
        self.prices_df = prices_df.set_index('Date', drop=True, append=True, inplace=False)
    
    def rebalance(self, company_list: dict):
        pass

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
        self.traders_writer.writerow([ticker, trade_type[trade], date, shares])
    
    def update_weights(self):
        port_weight_dists = self.weights
        cur_port_weight_dist = {}
        cur_port_weight_dist['CASH'] = self.cash / self.value
        for ticker, shares in self.portfolio.items():
            try:
                share_price = self.prices_df.loc[ticker, self.cur_day.strftime("%Y-%m-%d")]['Close']
            except (ValueError, KeyError):
                raise IndexError("Couldn't find the share price when calculating weights of portfolio!")
            cur_port_weight_dist[ticker] = (share_price * shares) / self.value
        
        port_weight_dists[self.cur_day.strftime("%Y-%m-%d")] = cur_port_weight_dist
        with open(self.weights_file, "w") as outfile:   
            json.dump(port_weight_dists, outfile)
        return cur_port_weight_dist

    def update_value(self):     
        new_value = self.cash
        for ticker, shares in self.portfolio.items():
            try:
                share_price = self.prices_df.loc[ticker, self.cur_day.strftime("%Y-%m-%d")]['Close']
                new_value = new_value + (share_price * shares)
            except (ValueError, KeyError):
                raise IndexError("Couldn't find the share price when calculating value of portfolio!")
        self.value = new_value
        return new_value

    def new_day(self, days=1):
        self.cur_day += timedelta(days)
        try:
            self.update_value()
            self.update_weights()
        except:
            pass

    def get_portfolio(self):
        portfolio_instance = self.portfolio
        for position in portfolio_instance:
            if (portfolio_instance[position] == 0):
                portfolio_instance.pop(position)
        return portfolio_instance


