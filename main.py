from datetime import datetime
from backtest import portfolio
from finance import get_data, monthly_data, beta_cov
import pandas
import csv

company_list_url = 'data/constituents.csv'
company_list = pandas.read_csv(company_list_url, sep=',', header=0)
price_data = pandas.read_csv('data/us-shareprices-daily.csv', sep=';', header=0, index_col=[0])
start_date = datetime.fromisoformat('2010-01-01')
low_vol_port = portfolio(100000, 'portfolios/portfolio.csv', start_date, price_data)

start = "2000-01-01"
end = "2020-01-01"
start_date_beta = datetime.fromisoformat('2007-01-01')
end_date_beta = datetime.fromisoformat('2010-01-01')
spy_data = get_data("SPY", price_data, start, end)
spy_monthly_data = monthly_data(spy_data, start_date_beta, end_date_beta)

for company in company_list.iterrows():
    ticker = company[1][0]
    try:
        company_data = get_data(ticker, price_data, start, end)
    except:
        print("{} not found.".format(ticker))
    try:
        company_monthly_data = monthly_data(company_data, start_date_beta, end_date_beta)
        beta = beta_cov(spy_monthly_data, company_monthly_data)
        print("{}: {}".format(ticker, beta))
    except (ValueError, KeyError):
        print("{} values not found.".format(ticker))