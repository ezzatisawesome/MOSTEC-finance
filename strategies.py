import pandas
from datetime import datetime, timedelta
from dateutil import relativedelta
from finance import get_data, monthly_data, beta_cov

class strategies:
    def __init__(self, company_list:pandas.DataFrame, price_data:pandas.DataFrame, start_date:datetime, end_date:datetime):
        self.company_list = company_list
        self.price_data = price_data
        self.start_date = start_date
        self.end_date = end_date
        self.date_array = []

    def set_monthly(self):
        date_array = []
        delta_time = relativedelta.relativedelta(months=1)
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
        start = "1990-01-01"
        end = "2020-01-01"
        end_date_beta = cur_date - relativedelta.relativedelta(years=3)
        try:
            spy_data = get_data("SPY", self.price_data, start, end)
            spy_monthly_data = monthly_data(spy_data, end_date_beta, cur_date)
        except:
            ValueError("STOPPP")
        beta_data = {}
        for company in self.company_list.iterrows():
            ticker = company[1][0]
            try:
                company_data = get_data(ticker, self.price_data, start, end)
            except:
                print("{} not found.".format(ticker))
            try:
                company_monthly_data = monthly_data(company_data, end_date_beta, cur_date)
                beta = beta_cov(spy_monthly_data, company_monthly_data)
                beta_data[ticker] = beta
                print("{}: {}".format(ticker, beta))
            except (ValueError, KeyError):
                print("{} values not found.".format(ticker))
        sorted_beta_values = sorted(beta_data.values()) # Sort the values
        sorted_beta_data = {}
        for i in sorted_beta_values[:round(len(sorted_beta_values)*.2)]:
            for k in beta_data.keys():
                if beta_data[k] == i:
                    sorted_beta_data[k] = beta_data[k]
                    break

        return sorted_beta_data