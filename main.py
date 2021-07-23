from datetime import datetime, timedelta
from backtest import portfolio
from strategies import strategies
import pandas
import matplotlib.pyplot
import numpy


def main(strategy: strategies, portfolio: portfolio, start_date:datetime, end_date:datetime):
    value_array = []
    day_array = []

    strategy.set_monthly()
    iter_date = portfolio.cur_day

    while iter_date <= end_date:
        if (strategy.check_date(iter_date)):
            portfolio.buy_queried() # any queried orders or rebalances should be executed
            
            print("{}: {}".format(iter_date, portfolio.value))
            portfolio.new_day()
            iter_date = portfolio.cur_day
            continue

        weights = strategy.low_vol_1(iter_date)
        portfolio.rebalance(weights)
        #value_array.append(portfolio.value)
        #day_array.append(portfolio.cur_day)
        print("STRAT:", weights)
        print("PORT: ", portfolio.portfolio)
        print("{}: {}".format(iter_date, portfolio.value))

        portfolio.new_day()
        iter_date = portfolio.cur_day

    #x = numpy.array(value_array)
    #y = numpy.array(day_array)
    #matplotlib.pyplot.plot(x,y)
    #matplotlib.pyplot.show()

if (__name__ == "__main__"):
    company_list_url = 'data/test1.csv'
    price_data_url = 'data/us-shareprices-daily.csv'
    company_list = pandas.read_csv(company_list_url, sep=',', header=0)
    price_data = pandas.read_csv(price_data_url, sep=';', header=0, index_col=[0])
    #balance = pandas.read_csv('data/us-balance-annual.csv', sep=';', header=0, index_col=[0,3])
    #cashflows = pandas.read_csv('data/us-cashflow-annual.csv', sep=';', header=0, index_col=[0,3])
    #income = pandas.read_csv('data/us-income-annual.csv', sep=';', header=0, index_col=[0])

    trades_csv = 'portfolios/portfolio.csv'
    weights_json = 'portfolios/portfolio.json'
    starting_amount = 100000
    start_date = datetime.fromisoformat('2009-12-31')
    end_date = datetime.fromisoformat('2019-12-31')
    low_vol_port = portfolio(starting_amount, trades_csv, weights_json, price_data, start_date)
    low_vol_strat = strategies(company_list, price_data, start_date, end_date)
    main(low_vol_strat, low_vol_port, start_date, end_date)