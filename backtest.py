from os import close
from numpy.lib.arraysetops import isin
import pandas
from datetime import datetime, timedelta
import csv
import json


class queried_buy:
    def __init__(self, ticker, attempted_purchase_date, shares=100, dollar_amount=None):
        self.ticker = ticker
        self.shares = shares
        self.dollar_amount = dollar_amount
        self.apd = attempted_purchase_date

class queried_sell:
    def __init__(self, ticker, attempted_sell_date, shares=100, dollar_amount=None):
        self.ticker = ticker
        self.shares = shares
        self.dollar_amount = dollar_amount
        self.asd = attempted_sell_date

class queried_rebalance:
    def __init__(self, company_list: dict):
        self.company_list = company_list

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
        self.cur_day = start_date - timedelta(days=1)
        self.prices_df = prices_df.set_index('Date', drop=True, append=True, inplace=False)

        self.query = []

    def rebalance(self, company_list: dict):
        if (len(company_list) == 0):
            print("{}: REBALANCE LIST EMPTY".format(self.cur_day))
            return
        try:
            self.prices_df.loc[company_list[0], self.cur_day.strftime("%Y-%m-%d")]['Close']
        except KeyError:
            new_query = queried_rebalance(company_list)
            self.query.append(new_query)
            print("{}: QUERYING REBALANCE".format(self.cur_day))
            return
        
        for ticker in self.portfolio.keys():
            if (ticker not in self.portfolio.keys()):
                # sell all of it
                self.sell(ticker, shares=self.portfolio[ticker])
        
        buy_list = {}
        sell_list = {}

        for ticker in company_list.keys():
            if (ticker not in self.portfolio.keys()):
                self.portfolio[ticker] = 0
            value_relative_to_port = company_list[ticker] * self.value, 6
            share_price = self.prices_df.loc[ticker, self.cur_day.strftime("%Y-%m-%d")]['Close']
            market_value = share_price * self.portfolio[ticker], 6
            if (round(value_relative_to_port) > round(market_value)):
                buy_list[ticker] = round(value_relative_to_port-market_value) - 1
            elif (round(value_relative_to_port) < round(market_value)):
                sell_list[ticker] = round(market_value-value_relative_to_port) - 1
            else:
                pass
        self.clean_portfolio()
        
        for i in sell_list.keys():
            self.sell(i, dollar_amount=sell_list[i])
        for i in buy_list.keys():
            self.buy(i, dollar_amount=buy_list[i])
    
    def rebalance2(self, company_list: dict):
        for ticker in self.portfolio.keys():
            if (ticker not in company_list.keys()):
                # sell all of it
                self.sell(ticker, shares=self.portfolio[ticker])

        buy_list = {}
        sell_list = {}

        for ticker in company_list.keys():
            if (ticker not in self.portfolio.keys()):
                self.portfolio[ticker] = 0
            value_relative_to_port = company_list[ticker] * self.value
            share_price = self.prices_df.loc[ticker, self.cur_day.strftime("%Y-%m-%d")]['Close']
            market_value = share_price * self.portfolio[ticker]
            if (round(value_relative_to_port) > round(market_value)):
                buy_list[ticker] = round(value_relative_to_port - market_value) - 1
            elif (round(value_relative_to_port) < round(market_value)):
                sell_list[ticker] = round(market_value - value_relative_to_port) - 1
            else:
                pass
        
        self.clean_portfolio()

        for i in sell_list.keys():
            self.sell(i, dollar_amount=sell_list[i])
        for i in buy_list.keys():
            self.buy(i, dollar_amount=buy_list[i])

    def buy_queried(self):
        for item in self.query:
            if isinstance(item, queried_rebalance):
                try:
                    self.rebalance2(item.company_list)
                    self.query.remove(item)
                    print("{}: REBALANCE QUERY COMPLETE".format(self.cur_day))
                except (KeyError, IndexError):
                    print("{}: REBALANCE STILL IN QUEUE".format(self.cur_day))
            elif isinstance(item, queried_buy):
                try:
                    self.buy(item.ticker, item.shares, item.dollar_amount)
                except KeyError:
                    self.buy(item.ticker, item.shares, item.dollar_amount)
            elif isinstance(item, queried_sell):
                try:
                    self.sell(item.ticker, item.shares, item.dollar_amount)
                except KeyError:
                    self.sell(item.ticker, item.shares, item.dollar_amount)
            
    # dollar amount takes precedence over shares
    def buy(self, ticker, shares=100, dollar_amount=None):
        if (ticker not in self.portfolio.keys()):
            self.portfolio[ticker] = 0
        try:
            cur_price = self.prices_df.loc[ticker, self.cur_day.strftime("%Y-%m-%d")]['Close']
        except:
            raise IndexError("{}: Couldn't find closing price on when trying to buy {} on {}".format(self.cur_day, ticker, self.cur_day.strftime("%Y-%m-%d")))

        if (dollar_amount != None):
            if (dollar_amount > self.cash):
                raise ValueError('{}: You do not have enough cash to purchase ${} of {}'.format(self.cur_day, dollar_amount, ticker, self.cash))
            units = dollar_amount / cur_price
            self.portfolio[ticker] = self.portfolio[ticker] + units
            self.upload_trade(0, ticker, self.cur_day, units)
            self.cash -= dollar_amount

        else:
            if (shares * cur_price > self.cash):
                raise ValueError('{}: You do not have enough cash to purchase {} shares of {}'.format(self.cur_day, shares, ticker))
            self.portfolio[ticker] = self.portfolio[ticker] + shares
            self.upload_trade(0, ticker, self.cur_day, shares)
            self.cash -= shares * cur_price

        self.update_value()

    #dollar amount takes precedence over shares
    def sell(self, ticker, shares=100, dollar_amount=None):
        if (ticker not in self.portfolio.keys()):
            raise ValueError('{}: You do not own shares of {} and cannot sell it'.format(self.cur_day, ticker))

        try:
            cur_price = self.prices_df.loc[ticker, self.cur_day.strftime("%Y-%m-%d")]['Close']
        except:
            raise IndexError("{}: Couldn't find closing price on when trying to sell {}".format(self.cur_day, ticker))

        if (dollar_amount != None):
            if (self.portfolio[ticker] * cur_price < dollar_amount):
                raise ValueError('{}: You do not have ${} of {} to sell'.format(self.cur_day, dollar_amount, ticker))
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
    
    def clean_portfolio(self):
        {x:y for x,y in self.portfolio.items() if y!=0}
    
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

