import pandas
from datetime import datetime, timedelta
from dateutil import relativedelta
from finance import get_data, monthly_data, beta_cov

def split_time(start_date:datetime, end_date:datetime, days:int=0, months:int=0, years:int=0):
        date_array = []
        delta_time = relativedelta.relativedelta(days=days, months=months, years=years)
        iter_date = start_date
        while (iter_date.weekday() != 4):
            iter_date = iter_date + timedelta(days=1)
        date_array.append(iter_date)
        while (iter_date + timedelta(days=7) < end_date):
            iter_date = iter_date + delta_time
            date_array.append(iter_date)
        return date_array

class strategies:
    def __init__(self, company_list:pandas.DataFrame, price_data:pandas.DataFrame, start_date:datetime, end_date:datetime):
        self.company_list = company_list
        self.price_data = price_data
        self.start_date = start_date
        self.end_date = end_date
        self.date_array = []

    def set_monthly(self):
        self.date_array = split_time(self.start_date, self.end_date, months=1)

    def set_yearly(self):
        self.date_array = split_time(self.start_date, self.end_date, years=1)

    def low_vol_1(self, cur_date: datetime):
        # check if current day is end of month
        if cur_date not in self.date_array:
            return None

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