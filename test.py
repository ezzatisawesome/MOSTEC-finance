from finance import monthly_data2, get_data, beta_cov
from datetime import date, datetime, timedelta
from dateutil import relativedelta
import pandas

price_data_url = 'data/sp500-shareprices-daily.csv'
price_data = pandas.read_csv(price_data_url, sep=';', header=0, usecols=[0,1,2,3], index_col=[0])

end_date = datetime.fromisoformat("2012-05-30")
start_date = end_date - relativedelta.relativedelta(years=3)

#spy_df = get_data('spy', price_data, datetime.fromisoformat("2000-01-01"), datetime.fromisoformat("2020-01-02"))
#goog_df = get_data('abt', price_data, datetime.fromisoformat("2000-01-01"), datetime.fromisoformat("2020-01-02"))


spy_df = get_data('spy', price_data, start_date-relativedelta.relativedelta(months=1), end_date+relativedelta.relativedelta(months=1))
mmm_df = get_data('now', price_data, start_date-relativedelta.relativedelta(months=1), end_date+relativedelta.relativedelta(months=1))

#print(spy_df.tail())
print(mmm_df.tail())

spy_df_monthly = monthly_data2(spy_df, start_date, end_date)
goog_df_monthly = monthly_data2(mmm_df, start_date, end_date)
beta_cov(spy_df_monthly, goog_df_monthly)

print(beta_cov(spy_df_monthly, goog_df_monthly))
