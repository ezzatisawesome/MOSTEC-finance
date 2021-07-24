from os import error
from numpy.core.fromnumeric import sort
import pandas
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from finance import get_data, monthly_data2, beta_cov

class strategies:
    def __init__(self, company_list:pandas.DataFrame, price_data:pandas.DataFrame, start_date:datetime, end_date:datetime):
        self.company_list = company_list
        self.price_data = price_data
        self.start_date = start_date
        self.end_date = end_date
        self.date_array = []

        self.start_data_date = datetime.fromisoformat("2006-12-31")
        self.end_data_date = datetime.fromisoformat("2019-12-31")
        self.spy_data = get_data("SPY", self.price_data, self.start_data_date, self.end_data_date)

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
            except KeyError:
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
        sorted_beta_data = sorted(beta_data.items(), key=lambda x: x[1])[:round(len(beta_data)*.2)]
        if (len(sorted_beta_data) != 0):
            equal_weight = 1 / len(sorted_beta_data)
        else:
            equal_weight = 0
        weights = {}
        for i in sorted_beta_data:
            weights[i[0]] = equal_weight
        return weights