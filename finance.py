from numpy.core.defchararray import startswith
import pandas
import numpy
from sklearn.linear_model import LinearRegression

companies = pandas.read_csv('data/us-companies.csv', sep=';', header=0)
#balance = pandas.read_csv('data/us-balance-annual.csv', sep=';', header=0, index_col=[0,3])
#cashflows = pandas.read_csv('data/us-cashflow-annual.csv', sep=';', header=0, index_col=[0,3])
#income = pandas.read_csv('data/us-income-annual.csv', sep=';', header=0, index_col=[0])
prices = pandas.read_csv('data/us-shareprices-daily.csv', sep=';', header=0, index_col=[0])

def get_data(ticker, start, end):
    mask = (prices['Date'] > start) & (prices['Date'] <= end)
    price_df = prices.loc[mask].loc[ticker.upper()]
    price_df.set_index(['Date'], inplace=True, drop=True)
    return price_df

def beta_slope(price_data1:pandas.DataFrame, price_data2:pandas.DataFrame):
    price_data1 = price_data1.pct_change()
    price_data2 = price_data2.pct_change()  
    price_data1.drop(price_data1.index[:1], inplace=True)
    price_data2.drop(price_data2.index[:1], inplace=True)
    x = numpy.array(price_data1['Close']).reshape((-1,1))
    y = numpy.array(price_data2['Close'])
    model = LinearRegression().fit(x, y)
    return model.coef_

def beta_cov(price_data1:pandas.DataFrame, price_data2:pandas.DataFrame):
    price_data1 = price_data1.pct_change()
    price_data2 = price_data2.pct_change()  
    price_data1.drop(price_data1.index[:1], inplace=True)
    price_data2.drop(price_data2.index[:1], inplace=True)
    x = numpy.array(price_data1['Close'])
    y = numpy.array(price_data2['Close'])
    d = []
    d.append(x)
    d.append(y)
    covariance = numpy.cov(d)[0, 1]
    variance = numpy.var(x)
    return covariance/variance


start = "2019-01-01"
end = "2020-01-01"
spy = get_data("SPY", "2019-01-01", "2020-01-01")
for company in companies.iterrows():
    ticker = company[1][0]
    try:
        company_data = get_data(ticker, start, end)
        beta = beta_cov(company_data, spy)
        print("{}: {}".format(ticker, beta))
    except KeyError:
        print("{} not found.".format(ticker))