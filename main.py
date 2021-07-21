from datetime import datetime
from backtest import portfolio
import strategies
import pandas
import matplotlib.pyplot
import numpy


def main(strategy, portfolio: portfolio):
    test_hello = {'ABT': 0.4449378671376737, 'ACN': 0.7322539352754748, 'ATVI': 0.7794778666942336, 'ADM': 0.7932822233625583, 'MMM': 0.8040232419762925, 'ADBE': 1.0681818947675954, 'AOS': 1.1070175677209382, 'ABMD': 1.1816852081738856}
    for ticker in test_hello:
        portfolio.buy(ticker, shares=100)
    test_val = []
    test_val2 = []
    for i in range(1000):
        portfolio.new_day()
        test_val.append(portfolio.value)
        test_val2.append(portfolio.cur_day)
        print(portfolio.cur_day)
        print(portfolio.value)

    x = numpy.array(test_val2)
    y = numpy.array(test_val)
    matplotlib.pyplot.plot(x,y)
    matplotlib.pyplot.show()

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
    start_date = datetime.fromisoformat('2010-01-04')
    low_vol_port = portfolio(starting_amount, trades_csv, weights_json, start_date, price_data)
    low_vol_strat = strategies.low_vol_1(company_list, price_data)
    main(low_vol_strat, low_vol_port)