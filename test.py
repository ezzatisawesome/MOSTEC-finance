from finance import monthly_data2, get_data
from datetime import datetime, timedelta
from dateutil import relativedelta
import pandas
import numpy

company_list_url = 'companies/sp500.csv'
price_data_url = 'data/sp500-shareprices-daily.csv'
company_list = pandas.read_csv(company_list_url, sep=',', header=0)
price_data = pandas.read_csv(price_data_url, sep=';', header=0, usecols=[0,1,2,3], index_col=[0])
balance = pandas.read_csv('data/us-balance-annual.csv', sep=';', header=0, index_col=[0,3])
cashflows = pandas.read_csv('data/us-cashflow-annual.csv', sep=';', header=0, index_col=[0,3])
income = pandas.read_csv('data/us-income-annual.csv', sep=';', header=0, index_col=[0,3])

year = 2015
ticker = 'MMM'


company_prices = get_data(ticker, price_data, datetime.fromisoformat('{}-12-31'.format(year-3))-timedelta(days=20), datetime.fromisoformat('{}-12-31'.format(year))+timedelta(days=20))
company_monthly_data = monthly_data2(company_prices, datetime.fromisoformat('{}-12-31'.format(year-3))-timedelta(days=20), datetime.fromisoformat('{}-12-31'.format(year))+timedelta(days=20))
#year_return = round((company_monthly_data.iloc[len(company_monthly_data)-1]['Adj. Close'] / company_monthly_data.iloc[0]['Adj. Close']))
returns = company_monthly_data.iloc[len(company_monthly_data)-1]['Adj. Close'] / company_monthly_data.iloc[0]['Adj. Close']
print(company_monthly_data)
print(returns)

