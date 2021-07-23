from datetime import datetime, timedelta
from operator import truediv
from dateutil import relativedelta
from sklearn.linear_model import LinearRegression
import pandas
import numpy

def get_data(ticker, prices_df: pandas.DataFrame, start, end):
    mask = (prices_df['Date'] > start) & (prices_df['Date'] <= end)
    price_df = prices_df.loc[mask].loc[ticker.upper()]
    price_df.set_index(['Date'], inplace=True, drop=True)
    return price_df

def monthly_data(price_df: pandas.DataFrame, start_date: datetime, end_date: datetime):
    price_df.index = pandas.to_datetime(price_df.index)
    date_array = []
    returns_df = pandas.DataFrame()
    iter_date = start_date
    while (iter_date.weekday() != 4):
        iter_date = iter_date + timedelta(days=1)
    date_array.append(iter_date)
    while (iter_date + relativedelta.relativedelta(months=1) < end_date):
        iter_date = iter_date + relativedelta.relativedelta(months=1)
        date_array.append(iter_date)
    for date in date_array:
        try:
            returns_df = returns_df.append(price_df.loc[date])
        except:
            returns_df = returns_df.append(price_df.loc[date-timedelta(days=1)])
    return returns_df

def monthly_data2(price_df:pandas.DataFrame, start_date: datetime, end_date:datetime):
    price_df.set_index('Close', drop=True, append=False)
    #print(price_df)
    returns_df = pandas.DataFrame()
    delta_time = relativedelta.relativedelta(months=1)
    next_month = start_date.replace(day=28) + timedelta(days=4)
    iter_date = next_month - timedelta(days=next_month.day)
    while (iter_date + delta_time < end_date):
        iter_date = iter_date + delta_time
        next_month = iter_date.replace(day=28) + timedelta(days=4)
        iter_date = next_month - timedelta(days=next_month.day)
        
        if (iter_date.weekday() == 5):
            try:
                returns_df = returns_df.append(price_df.loc[(iter_date-timedelta(days=1)).strftime("%Y-%m-%d")])
            except:
                returns_df = returns_df.append(price_df.loc[(iter_date-timedelta(days=2)).strftime("%Y-%m-%d")])
        elif (iter_date.weekday() == 6):
            try:
                returns_df = returns_df.append(price_df.loc[(iter_date+timedelta(days=1)).strftime("%Y-%m-%d")])
            except:
                returns_df = returns_df.append(price_df.loc[(iter_date+timedelta(days=2)).strftime("%Y-%m-%d")])
        else:
            try:
                returns_df = returns_df.append(price_df.loc[iter_date.strftime("%Y-%m-%d")])
            except:
                pass
    
    return returns_df

#price_data1 should be an indice
def beta_slope(price_data1:pandas.DataFrame, price_data2:pandas.DataFrame):
    price_data1 = price_data1.pct_change()
    price_data2 = price_data2.pct_change()  
    price_data1.drop(price_data1.index[:1], inplace=True)
    price_data2.drop(price_data2.index[:1], inplace=True)
    x = numpy.array(price_data1['Adj. Close']).reshape((-1,1))
    y = numpy.array(price_data2['Adj. Close'])
    model = LinearRegression().fit(x, y)
    return model.coef_

#price_data1 should be an indice
def beta_cov(price_data1:pandas.DataFrame, price_data2:pandas.DataFrame):
    try:
        price_data1 = price_data1.pct_change()
        price_data2 = price_data2.pct_change()
        price_data1.drop(price_data1.index[:1], inplace=True)
        price_data2.drop(price_data2.index[:1], inplace=True)
        x = numpy.array(price_data1['Adj. Close'])
        y = numpy.array(price_data2['Adj. Close'])
        d = []
        d.append(x)
        d.append(y)
        covariance = numpy.cov(d)[0, 1]
        variance = numpy.var(x)
        return covariance/variance
    except ValueError:
        return "ValueError"


