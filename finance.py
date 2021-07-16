import pandas
import datetime
import numpy
from sklearn.linear_model import LinearRegression

#balance = pandas.read_csv('data/us-balance-annual.csv', sep=';', header=0, index_col=[0,3])
#cashflows = pandas.read_csv('data/us-cashflow-annual.csv', sep=';', header=0, index_col=[0,3])
#income = pandas.read_csv('data/us-income-annual.csv', sep=';', header=0, index_col=[0])
prices = pandas.read_csv('data/test.csv', sep=';', header=0, index_col=[0, 2])

def get_prices(ticker, start, end):
    start_date = datetime.date.fromisoformat(start)
    end_date = datetime.date.fromisoformat(end)
    delta = datetime.timedelta(days=1)
    date_array = []
    price_array = []
    #previous_price = 0

    while start_date <= end_date:

        #print(start_date)
        start_date += delta
        try:
            price = prices.loc[ticker.upper(), start_date.isoformat()]["Close"]
            price_array.append(price)
            date_array.append(start_date)
            #previous_price = price
        except KeyError:
            print("Missing price value on", start_date.isoformat() + "!")
            #price_array.append(previous_price)

    return pandas.DataFrame({'Date': date_array, 'Price': price_array}).set_index('Date')

goog = get_prices("goog", "2019-01-01", "2020-01-01").pct_change()
spy = get_prices("SPY", "2019-01-01", "2020-01-01").pct_change()
goog = goog.drop(goog.index[0])
spy = spy.drop(spy.index[0])

x = numpy.array(goog['Price']).reshape((-1,1))
y = numpy.array(spy['Price'])
model = LinearRegression().fit(x, y)

# Prints the beta to the screen 
print('Beta: ', model.coef_)
