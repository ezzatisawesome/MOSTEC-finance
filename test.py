from strategies import strategies
from datetime import datetime, timedelta
import pandas

company_list_url = 'data/constituents.csv'
price_data_url = 'data/us-shareprices-daily.csv'
company_list = pandas.read_csv(company_list_url, sep=',', header=0)
price_data = pandas.read_csv(price_data_url, sep=';', header=0, index_col=[0])

test_strat = strategies(company_list, price_data, datetime.fromisoformat('2010-01-01'), datetime.fromisoformat('2020-01-01'))
test_strat.set_monthly()
print(test_strat.low_vol_1(datetime.fromisoformat('2010-01-01')))