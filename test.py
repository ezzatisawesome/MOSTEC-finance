import pandas
import datetime

prices = pandas.read_csv('data/test.csv', sep=';', header=0, index_col=[0])
#prices['Date'] = pandas.to_datetime(prices['Date'])
#prices.set_index(['Ticker', 'Date'], inplace=True, drop=True)

def get_prices(ticker, start, end):
    mask = (prices['Date'] > start) & (prices['Date'] <= end)
    price_df = prices.loc[mask].loc[ticker]['Close']
    return price_df