import pandas
import datetime
from finance import get_data, monthly_data, beta_cov

class low_vol_1:
    def __init__(self, company_list: pandas.DataFrame, price_data: pandas.DataFrame):
        self.company_list = company_list
        self.price_data = price_data

    def execute(self, cur_date):
        start = "2000-01-01"
        end = "2020-01-01"
        start_date_beta = datetime.fromisoformat('2007-01-01')
        end_date_beta = datetime.fromisoformat('2010-01-01')
        spy_data = get_data("SPY", self.price_data, start, end)
        spy_monthly_data = monthly_data(spy_data, start_date_beta, end_date_beta)

        beta_data = {}

        for company in self.company_list.iterrows():
            ticker = company[1][0]
            try:
                company_data = get_data(ticker, self.price_data, start, end)
            except:
                print("{} not found.".format(ticker))
            try:
                company_monthly_data = monthly_data(company_data, start_date_beta, end_date_beta)
                beta = beta_cov(spy_monthly_data, company_monthly_data)
                beta_data[ticker] = beta
                print("{}: {}".format(ticker, beta))
            except (ValueError, KeyError):
                print("{} values not found.".format(ticker))

        sorted_beta_values = sorted(beta_data.values()) # Sort the values
        sorted_beta_data = {}

        for i in sorted_beta_values:
            for k in beta_data.keys():
                if beta_data[k] == i:
                    sorted_beta_data[k] = beta_data[k]
                    break

        return sorted_beta_data