from datetime import datetime
from backtest import portfolio
from strategies import strategies
from tempfile import TemporaryFile
import matplotlib.pyplot
import pandas
import numpy


def main(strategy: strategies, portfolio: portfolio, start_date:datetime, end_date:datetime):
    value_array_file = 'portfolios/value_array.npy'
    day_array_file = 'portfolios/day_array.npy'
    value_array = []
    day_array = []
    strategy.set_monthly()

    while portfolio.cur_day <= end_date:
        portfolio.new_day()
        value_array.append(portfolio.value)
        day_array.append(portfolio.cur_day)
        dd = portfolio.cur_day.strftime("%Y-%m-%d")
        print("{}: {}".format(dd, portfolio.value))
    
        if (strategy.check_date(portfolio.cur_day)):
            portfolio.buy_queried() # any queried orders or rebalances should be executed
            continue

        weights = strategy.low_vol_1(portfolio.cur_day)
        print("{}: CASH: {}".format(dd, portfolio.cash))
        portfolio.rebalance(weights)
        print("{}: PORT: {}".format(dd, portfolio.portfolio))

    x = numpy.array(value_array)
    y = numpy.array(day_array)
    numpy.save(value_array_file, x)
    numpy.save(day_array_file, y)
    matplotlib.pyplot.plot(y,x)
    matplotlib.pyplot.show()

if (__name__ == "__main__"):
    company_list_url = 'data/test1.csv'
    price_data_url = 'data/sp500-shareprices-daily.csv'
    company_list = pandas.read_csv(company_list_url, sep=',', header=0)
    price_data = pandas.read_csv(price_data_url, sep=';', header=0, usecols=[0,1,2,3], index_col=[0])
    #balance = pandas.read_csv('data/us-balance-annual.csv', sep=';', header=0, index_col=[0,3])
    #cashflows = pandas.read_csv('data/us-cashflow-annual.csv', sep=';', header=0, index_col=[0,3])
    #income = pandas.read_csv('data/us-income-annual.csv', sep=';', header=0, index_col=[0])

    trades_csv = 'portfolios/portfolio.csv'
    weights_json = 'portfolios/portfolio.json'
    starting_amount = 100000
    start_date = datetime.fromisoformat('2011-09-25')
    end_date = datetime.fromisoformat('2014-12-31')
    low_vol_port = portfolio(starting_amount, trades_csv, weights_json, price_data, start_date)
    low_vol_strat = strategies(company_list, price_data, start_date, end_date)
    main(low_vol_strat, low_vol_port, start_date, end_date)
