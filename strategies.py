from os import error
from numpy.core.fromnumeric import sort
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from finance import get_data, monthly_data2, beta_cov
import pandas


class strategies:
    def __init__(self, company_list:pandas.DataFrame, price_data:pandas.DataFrame, balance:pandas.DataFrame, income:pandas.DataFrame, start_date:datetime, end_date:datetime):
        self.company_list = company_list
        self.price_data = price_data
        self.start_date = start_date
        self.end_date = end_date
        self.date_array = []

        self.start_data_date = datetime.fromisoformat("2006-12-31")
        self.end_data_date = datetime.fromisoformat("2019-12-31")
        self.spy_data = get_data("SPY", self.price_data, self.start_data_date, self.end_data_date)
        self.income_data = income
        self.balance_data = balance

    def set_monthly(self):
        date_array = []
        delta_time = relativedelta(months=1)
        next_month = self.start_date.replace(day=28) + timedelta(days=4)
        iter_date = next_month - timedelta(days=next_month.day)
        date_array.append(iter_date)
        while (iter_date + delta_time < self.end_date):
            iter_date = iter_date + delta_time
            next_month = iter_date.replace(day=28) + timedelta(days=4)
            iter_date = next_month - timedelta(days=next_month.day)
            date_array.append(iter_date)
        self.date_array = date_array

    # check if current day is end of month
    def check_date(self, cur_date):
        return cur_date not in self.date_array

    def low_vol_1(self, cur_date: datetime):
        end_date_beta = cur_date - relativedelta(years=3)
        try:
            spy_monthly_data = monthly_data2(self.spy_data, end_date_beta, cur_date)
        except:
            ValueError("SPY: MONTHLY DATA ERROR")
        beta_data = {}
        for company in self.company_list.iterrows():
            ticker = company[1][0]
            try:
                company_data = get_data(ticker, self.price_data, end_date_beta-relativedelta(months=1), cur_date+relativedelta(months=1))
            except (ValueError, KeyError, AttributeError):
                print("{}: COMPANY DATA ERROR".format(ticker))
                continue
            try:
                company_monthly_data = monthly_data2(company_data, end_date_beta, cur_date)
            except:
                print("{}: MONTHLY DATA ERROR".format(ticker))
                continue
            try:
                beta = beta_cov(spy_monthly_data, company_monthly_data)
                beta_data[ticker] = beta
                print("{}: {}".format(ticker, beta))
            except:
                print("{}: BETA ERROR".format(ticker))
        
        result = dict(filter(lambda x: x[1] >= 0.0, beta_data.items()))
        sorted_beta_data = sorted(result.items(), key=lambda x: x[1])[:round(len(result))]
        equal_weight = 1/len(sorted_beta_data) if len(sorted_beta_data) != 0 else  0
        weights = dict(zip([i[0] for i in sorted_beta_data], [equal_weight]*len(sorted_beta_data)))

        return weights

    def low_vol_2(self, cur_date: datetime):
        end_date_beta = cur_date - relativedelta(years=3)
        try:
            spy_monthly_data = monthly_data2(self.spy_data, end_date_beta, cur_date)
        except:
            ValueError("SPY: MONTHLY DATA ERROR")
        beta_data = {}
        for company in self.company_list.iterrows():
            ticker = company[1][0]
            try:
                company_data = get_data(ticker, self.price_data, end_date_beta-relativedelta(months=1), cur_date+relativedelta(months=1))
            except (ValueError, KeyError, AttributeError):
                print("{}: COMPANY DATA ERROR".format(ticker))
                continue
            try:
                company_monthly_data = monthly_data2(company_data, end_date_beta, cur_date)
            except:
                print("{}: MONTHLY DATA ERROR".format(ticker))
                continue
            try:
                beta = beta_cov(spy_monthly_data, company_monthly_data)
                beta_data[ticker] = beta
                print("{}: {}".format(ticker, beta))
            except:
                print("{}: BETA ERROR".format(ticker))
                
        result = dict(filter(lambda x: x[1] >= 0.0, beta_data.items()))
        sorted_beta_data = sorted(result.items(), key=lambda x: x[1])[:round(len(result)*.2)]
        inv_betas = list(map(lambda x: 1/x[1], sorted_beta_data))
        sum_inv_betas = sum(inv_betas)
        weights_data = list(map(lambda x: x/sum_inv_betas, inv_betas))
        weights = dict(zip([i[0] for i in sorted_beta_data], weights_data))

        return weights

    def low_vol_3(self, cur_date: datetime):
        end_date_beta = cur_date - relativedelta(years=3)
        try:
            spy_monthly_data = monthly_data2(self.spy_data, end_date_beta, cur_date)
        except:
            ValueError("SPY: MONTHLY DATA ERROR")
        beta_data = {}
        for company in self.company_list.iterrows():
            ticker = company[1][0]
            try:
                company_data = get_data(ticker, self.price_data, end_date_beta-relativedelta(months=1), cur_date+relativedelta(months=1))
            except (ValueError, KeyError, AttributeError):
                print("{}: COMPANY DATA ERROR".format(ticker))
                continue
            try:
                company_monthly_data = monthly_data2(company_data, end_date_beta, cur_date)
            except:
                print("{}: MONTHLY DATA ERROR".format(ticker))
                continue
            try:
                year = cur_date.year
                roe1 = round(self.income_data.loc[ticker, year]['Net Income'] / (self.balance_data.loc[ticker, year]['Total Assets'] - self.balance_data.loc[ticker, year]['Total Liabilities']), 3)
                roe2 = round(self.income_data.loc[ticker, year-1]['Net Income'] / (self.balance_data.loc[ticker, year-1]['Total Assets'] - self.balance_data.loc[ticker, year-1]['Total Liabilities']), 3)
                roe3 = round(self.income_data.loc[ticker, year-2]['Net Income'] / (self.balance_data.loc[ticker, year-2]['Total Assets'] - self.balance_data.loc[ticker, year-2]['Total Liabilities']), 3)
                roe = sum([roe1, roe2, roe3])
                if (roe < 0):
                    continue
            except:
                print("{}: ROE DATA ERROR".format(ticker))
                continue
            try:
                eps1 = round(self.income_data.loc[ticker, year]['Net Income'] / self.balance_data.loc[ticker, year]['Shares (Basic)'], 3)
                eps2 = round(self.income_data.loc[ticker, year-1]['Net Income'] / self.balance_data.loc[ticker, year-1]['Shares (Basic)'], 3)
                eps3 = round(self.income_data.loc[ticker, year-2]['Net Income'] / self.balance_data.loc[ticker, year-2]['Shares (Basic)'], 3)
                eps = sum([eps1, eps2, eps3])
                if (eps < 0):
                    continue
            except:
                print('{}: EPS DATA ERROR'.format(ticker))
                continue
            try:
                beta = beta_cov(spy_monthly_data, company_monthly_data)
                beta_data[ticker] = beta
                print("{}: {}".format(ticker, beta))
            except:
                print("{}: BETA ERROR".format(ticker))
            

        result = dict(filter(lambda x: x[1] >= 0.0, beta_data.items()))
        sorted_beta_data = sorted(result.items(), key=lambda x: x[1])[:round(len(result))]
        equal_weight = 1/len(sorted_beta_data) if len(sorted_beta_data) != 0 else  0
        weights = dict(zip([i[0] for i in sorted_beta_data], [equal_weight]*len(sorted_beta_data)))

        return weights