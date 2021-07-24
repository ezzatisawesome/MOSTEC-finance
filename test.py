from finance import monthly_data2, get_data, beta_cov
from datetime import date, datetime, timedelta
from dateutil import relativedelta
import pandas

print(datetime.now())

price_data_url = 'data/test.csv'
price_data = pandas.read_csv(price_data_url, sep=';', header=0, usecols=[0,2,6,7], index_col=[0])

print(datetime.now())

end_date = datetime.fromisoformat("2019-07-31")
start_date = end_date - relativedelta.relativedelta(years=3)

#spy_df = get_data('spy', price_data, datetime.fromisoformat("2000-01-01"), datetime.fromisoformat("2020-01-02"))
#goog_df = get_data('abt', price_data, datetime.fromisoformat("2000-01-01"), datetime.fromisoformat("2020-01-02"))

spy_df = get_data('spy', price_data, start_date-timedelta(days=1), end_date+timedelta(days=1))
goog_df = get_data('goog', price_data, start_date-timedelta(days=1), end_date+timedelta(days=1))

print(datetime.now())

spy_df_monthly = monthly_data2(spy_df, start_date, end_date)
goog_df_monthly = monthly_data2(goog_df, start_date, end_date)

print(datetime.now())

beta_cov(spy_df_monthly, goog_df_monthly)

print(datetime.now())

#print(beta_cov(spy_df_monthly, goog_df_monthly))
