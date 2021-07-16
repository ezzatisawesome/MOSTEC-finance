import pandas

balance = pandas.read_csv('data/us-balance-annual.csv', sep=';', header=0, index_col=[0,3])
cashflows = pandas.read_csv('data/us-cashflow-annual.csv', sep=';', header=0, index_col=[0,3])
income = pandas.read_csv('data/us-income-annual.csv', sep=';', header=0, index_col=[0,3])

def get_revenue(ticker, time_period):
    revenue = {}
    for i in range(time_period[0],time_period[1]+1):
        revenue[i] = income.loc[ticker.upper(), i]["Revenue"]
    return revenue

print(get_revenue('a', (2010, 2019)))
