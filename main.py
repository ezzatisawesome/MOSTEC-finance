from datetime import datetime
from backtest import portfolio
from finance import get_data, monthly_data, beta_cov
import pandas
import matplotlib.pyplot
import numpy

company_list_url = 'data/test1.csv'
company_list = pandas.read_csv(company_list_url, sep=',', header=0)
price_data = pandas.read_csv('data/us-shareprices-daily.csv', sep=';', header=0, index_col=[0])
start_date = datetime.fromisoformat('2010-01-04')
low_vol_port = portfolio(100000, 'portfolios/portfolio.csv', start_date, price_data)

start = "2000-01-01"
end = "2020-01-01"
start_date_beta = datetime.fromisoformat('2007-01-01')
end_date_beta = datetime.fromisoformat('2010-01-01')
spy_data = get_data("SPY", price_data, start, end)
spy_monthly_data = monthly_data(spy_data, start_date_beta, end_date_beta)

"""
beta_data = {}

for company in company_list.iterrows():
    ticker = company[1][0]
    try:
        company_data = get_data(ticker, price_data, start, end)
    except:
        print("{} not found.".format(ticker))
    try:
        company_monthly_data = monthly_data(company_data, start_date_beta, end_date_beta)
        beta = beta_cov(spy_monthly_data, company_monthly_data)
        beta_data[ticker] = beta
        print("{}: {}".format(ticker, beta))
    except (ValueError, KeyError):
        print("{} values not found.".format(ticker))

sorted_beta_values = sorted(beta_data.values()) # Sort the values
sorted_beta_data = {}

for i in sorted_beta_values:
    for k in beta_data.keys():
        if beta_data[k] == i:
            sorted_beta_data[k] = beta_data[k]
            break

print(sorted_beta_data)
"""
test_hello = {'ABT': 0.4449378671376737, 'ACN': 0.7322539352754748, 'ATVI': 0.7794778666942336, 'ADM': 0.7932822233625583, 'MMM': 0.8040232419762925, 'ADBE': 1.0681818947675954, 'AOS': 1.1070175677209382, 'ABMD': 1.1816852081738856}

for ticker in test_hello:
    low_vol_port.buy(ticker, shares=100)
test_val = []
test_val2 = []
for i in range(1000):
    low_vol_port.new_day()
    test_val.append(low_vol_port.value)
    test_val2.append(low_vol_port.cur_day)
    print(low_vol_port.cur_day)
    print(low_vol_port.value)

x = numpy.array(test_val2)
y = numpy.array(test_val)
print(y)
matplotlib.pyplot.plot(x,y)
matplotlib.pyplot.show()

