from finance import monthly_data2, get_data, beta_cov
from datetime import date, datetime, timedelta
from dateutil import relativedelta
import pandas
import numpy

company_list_url = 'companies/sp500.csv'
price_data_url = 'data/sp500-shareprices-daily.csv'
company_list = pandas.read_csv(company_list_url, sep=',', header=0)
price_data = pandas.read_csv(price_data_url, sep=';', header=0, usecols=[0,1,2,3], index_col=[0,1])
balance = pandas.read_csv('data/us-balance-annual.csv', sep=';', header=0, index_col=[0,3])
cashflows = pandas.read_csv('data/us-cashflow-annual.csv', sep=';', header=0, index_col=[0,3])
income = pandas.read_csv('data/us-income-annual.csv', sep=';', header=0, index_col=[0,3])

year = 2010
ticker = 'MMM'

year_return = (price_data.loc[ticker, '{}-12-31'.format(year)]['Close'] / price_data.loc[ticker, '{}-12-31'.format(year-1)]['Close']) - 1

print(year_return)
