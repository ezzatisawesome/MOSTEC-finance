import pandas
import csv

price_data_url = 'data/us-shareprices-daily.csv'
price_data = pandas.read_csv(price_data_url, sep=';', header=0, usecols=[0,2,6,7], index_col=[0])

price_data2 = pandas.DataFrame()

company_list_url = 'data/constituents.csv'
company_list = pandas.read_csv(company_list_url, sep=',', header=0)

for company in company_list.iterrows():
    ticker = company[1][0]
    print(ticker)
    try:
        dataaa = price_data.loc[ticker]
        print(dataaa.head())
        price_data2 = price_data2.append(dataaa)
    except KeyError:
        pass
price_data2.to_csv('sp500-shareprices-daily.csv', sep=';', header=False, index=True, index_label=False, mode='w')
