from finance import monthly_data2, get_data, beta_cov
from datetime import datetime
import pandas

price_data_url = 'data/us-shareprices-daily.csv'
price_data = pandas.read_csv(price_data_url, sep=';', header=0, index_col=[0])
spy_df = get_data('spy', price_data, datetime.fromisoformat("2000-01-01"), datetime.fromisoformat("2020-01-02"))
spy_df_monthly = monthly_data2(spy_df, datetime.fromisoformat("2007-01-31"), datetime.fromisoformat("2010-01-31"))
goog_df = get_data('abbv', price_data, datetime.fromisoformat("2000-01-01"), datetime.fromisoformat("2020-01-02"))
goog_df_monthly = monthly_data2(goog_df, datetime.fromisoformat("2007-01-31"), datetime.fromisoformat("2010-01-31"))
print(spy_df_monthly)
print(goog_df_monthly)

print(beta_cov(spy_df_monthly, goog_df_monthly))
