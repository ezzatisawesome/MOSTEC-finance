from datetime import datetime, timedelta
import pandas

prices = pandas.read_csv('data/us-shareprices-daily.csv', sep=';', header=0, index_col=[0])

def get_data(ticker, start, end):
    mask = (prices['Date'] > start) & (prices['Date'] <= end)
    price_df = prices.loc[mask].loc[ticker.upper()]
    price_df.set_index(['Date'], inplace=True, drop=True)
    return price_df


def monthly_returns(price_df: pandas.DataFrame, start_date: datetime, end_date: datetime):
    price_df.index = pandas.to_datetime(price_df.index)
    price_df = price_df.pct_change()
    price_df.drop(price_df.index[:1], inplace=True)
    date_array = []
    price_array = []
    iter_date = start_date
    while (iter_date.weekday() != 4):
        iter_date = iter_date + timedelta(days=1)
    date_array.append(iter_date)
    while (iter_date + timedelta(days=7) < end_date):
        iter_date = iter_date + timedelta(days=7)
        date_array.append(iter_date)
    for date in date_array:
        try:
            price_array.append(round(price_df.loc[date], 3))
        except:
            price_array.append(round(price_df.loc[date-timedelta(days=1)], 3))
    return price_array


start = "2007-01-01"
end = "2020-01-01"
#spy = get_data("SPY", start, end)
aapl = get_data("aapl", start, end)

start_date = datetime.fromisoformat('2007-01-01')
end_date = datetime.fromisoformat('2010-01-01')

print(monthly_returns(aapl, start_date, end_date))