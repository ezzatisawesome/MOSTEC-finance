import pandas
import csv

def select_prices():
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


#eps - net income / shares basic
#p/e - share price/ net income
#p/b - market price per share / ((total assets - total liability) / shares outstanding)
#p/s - (market price per share * shares outstanding) / marketprice sales

def select_fundamentals():
    company_list_url = 'companies/sp500.csv'
    price_data_url = 'data/sp500-shareprices-daily.csv'
    company_list = pandas.read_csv(company_list_url, sep=',', header=0)
    price_data = pandas.read_csv(price_data_url, sep=';', header=0, usecols=[0,1,2,3], index_col=[0,1])
    balance = pandas.read_csv('data/us-balance-annual.csv', sep=';', header=0, index_col=[0,3])
    income = pandas.read_csv('data/us-income-annual.csv', sep=';', header=0, index_col=[0,3])

    company_list = pandas.read_csv(company_list_url, sep=',', header=0)

    output_file =  open('sp500-debt_ratio-3year.csv', mode='w')
    output_file_writer = csv.writer(output_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
    output_file_writer.writerow(['debt_ratio', 'year_return'])

    for year in range(2010, 2020):
        for company in company_list.iterrows():
            ticker = company[1][0]
            try:
                year_return = round((price_data.loc[ticker, '{}-12-31'.format(year)]['Adj. Close'] / price_data.loc[ticker, '{}-12-31'.format(year-3)]['Adj. Close']) - 1, 3)
            except:
                year_return = None
                print('{}: PRICE ERROR'.format(ticker))
            """
            try:
                eps1 = round(income.loc[ticker, year]['Net Income'] / balance.loc[ticker, year]['Shares (Basic)'], 3)
                eps2 = round(income.loc[ticker, year-11]['Net Income'] / balance.loc[ticker, year-1]['Shares (Basic)'], 3)
                eps3 = round(income.loc[ticker, year-2]['Net Income'] / balance.loc[ticker, year-2]['Shares (Basic)'], 3)
                eps = sum([eps1, eps2, eps3])
            except:
                eps = None
                print('{}: EPS ERROR'.format(ticker))
            
            
            try:
                debt_to_equity1 = round(balance.loc[ticker, year]['Total Liabilities'] / (balance.loc[ticker, year]['Total Assets'] - balance.loc[ticker, year]['Total Liabilities']), 3)
                debt_to_equity2 = round(balance.loc[ticker, year-1]['Total Liabilities'] / (balance.loc[ticker, year-1]['Total Assets'] - balance.loc[ticker, year-1]['Total Liabilities']), 3)
                debt_to_equity3 = round(balance.loc[ticker, year-2]['Total Liabilities'] / (balance.loc[ticker, year-2]['Total Assets'] - balance.loc[ticker, year-2]['Total Liabilities']), 3)
                debt_to_equity = sum([debt_to_equity1, debt_to_equity2, debt_to_equity3])
            except:
                debt_to_equity = None
                print('{}: D/E ERROR'.format(ticker))
            
            try:
                roe1 = round(income.loc[ticker, year]['Net Income'] / (balance.loc[ticker, year]['Total Assets'] - balance.loc[ticker, year]['Total Liabilities']), 3)
                roe2 = round(income.loc[ticker, year-1]['Net Income'] / (balance.loc[ticker, year-1]['Total Assets'] - balance.loc[ticker, year-1]['Total Liabilities']), 3)
                roe3 = round(income.loc[ticker, year-2]['Net Income'] / (balance.loc[ticker, year-2]['Total Assets'] - balance.loc[ticker, year-2]['Total Liabilities']), 3)
                roe = sum([roe1, roe2, roe3])
            except:
                roe = None
                print('{}: ROE ERROR'.format(ticker))
            
            try:
                roa1 = round(income.loc[ticker, year]['Net Income'] / balance.loc[ticker, year]['Total Assets'], 3)
                roa2 = round(income.loc[ticker, year-1]['Net Income'] / balance.loc[ticker, year-1]['Total Assets'], 3)
                roa3 = round(income.loc[ticker, year-2]['Net Income'] / balance.loc[ticker, year-2]['Total Assets'], 3)
                roa = sum([roa1, roa2, roa3])
            except:
                roa = None
                print('{}: ROA ERROR'.format(ticker))
            
            try:
                current_ratio1 = round(balance.loc[ticker, year]['Total Current Assets'] / balance.loc[ticker, year]['Total Current Liabilities'], 3)
                current_ratio2 = round(balance.loc[ticker, year-1]['Total Current Assets'] / balance.loc[ticker, year-1]['Total Current Liabilities'], 3)
                current_ratio3 = round(balance.loc[ticker, year-2]['Total Current Assets'] / balance.loc[ticker, year-2]['Total Current Liabilities'], 3)
                current_ratio = sum([current_ratio1, current_ratio2, current_ratio3])
            except:
                current_ratio = None
                print('{}: CURRENT RATIO ERROR'.format(ticker))
            """

            try:
                debt_ratio1 = round(balance.loc[ticker, year]['Total Liabilities'] / balance.loc[ticker, year]['Total Assets'], 3)
                debt_ratio2 = round(balance.loc[ticker, year-1]['Total Liabilities'] / balance.loc[ticker, year-1]['Total Assets'], 3)
                debt_ratio3 = round(balance.loc[ticker, year-2]['Total Liabilities'] / balance.loc[ticker, year-2]['Total Assets'], 3)
                debt_ratio = sum([debt_ratio1, debt_ratio2, debt_ratio3])
            except:
                debt_ratio = None
                print('{}: DEBT RATIO ERROR'.format(ticker))
            
            if (debt_ratio is not None and year_return is not None):
                output_file_writer.writerow([debt_ratio, year_return])


if (__name__ == "__main__"):
    select_fundamentals()
