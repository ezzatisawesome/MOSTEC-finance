from dateutil.relativedelta import relativedelta
from finance import monthly_data2, get_data
from datetime import datetime, timedelta
import pandas

price_data_url = 'data/us-shareprices-daily.csv'
price_data = pandas.read_csv(price_data_url, sep=';', header=0, index_col=[0])
spy_df = get_data('spy', price_data, "2000-01-01", "2020-01-02")
goog_df_monthly = monthly_data2(goog_df, datetime.fromisoformat("2014-12-31"), datetime.fromisoformat("2019-12-31"))
goog_df = get_data('goog', price_data, "2000-01-01", "2020-01-01")
goog_df_monthly = monthly_data2(goog_df, datetime.fromisoformat("2014-12-31"), datetime.fromisoformat("2019-12-31"))

print(goog_df_monthly)
