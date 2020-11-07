import datetime
import pandas as pd
import io
import requests

from dateutil.relativedelta import relativedelta

from infocenter.calculator.Calculator import Calculator
from infocenter.container.DataContainer import DataContainer
from infocenter.errors.Errors import AverageDataError
from infocenter.logger.Log import log
from infocenter.provider.Provider import Provider
from infocenter.resorce.Property import Property


class AverageDataProvider(Provider):

    def __init__(self) -> None:
        super().__init__()
        self.daily = "daily_data"
        self.weekly = "weekly_data"
        self.monthly = "monthly_data"
        self.__daily_avg = pd.DataFrame()
        self.__weekly_avg = pd.DataFrame()
        self.__monthly_avg = pd.DataFrame()
        self.__prices = dict()

        try:
            log.i("Preparing fundamental average data...")
            self.url_fmt = Property(self.__class__.__name__).url_fmt
            self.data_container = DataContainer()
            self.calculator = Calculator()
            self.load_url()

        except Exception as e:
            log.e(e)
            raise AverageDataError(
                "Error occurred when loading average data.")

        try:
            self.__daily_avg = self.get_daily_avg_price()
            self.__weekly_avg = self.get_weekly_avg_price()
            self.__monthly_avg = self.get_monthly_avg_price()
            log.i("Finished.")
        except Exception as e:
            log.e(e)
            raise AverageDataError(
                "Failed to calculate average data.")

        return None

    def load_url(self) -> None:
        for key in [self.daily, self.weekly, self.monthly]:
            if not self._get_basic_url(key):
                log.e("URL format was not found.")
                log.e(f"Please check yaml file for {self.__class__.__name__}")
                break

            super().load_url(self._get_basic_url(key))
            binary = requests.get(self.__set_time(self.url)).content
            rs = pd.read_csv(io.StringIO(binary.decode('utf-8')),
                             index_col=0,
                             header=0,
                             na_values=0,
                             encoding="utf-8")
            self.__prices[key] = rs

        self.data_container.register(self.__class__.__name__,
                                     self.__prices)
        return None

    def get_daily_avg_price(self) -> pd.Series:
        return self.calculator.cal_avg_data(self.daily,
                                            self.__prices[self.daily])

    def get_weekly_avg_price(self) -> pd.Series:
        return self.calculator.cal_avg_data(self.weekly,
                                            self.__prices[self.weekly])

    def get_monthly_avg_price(self) -> pd.Series:
        return self.calculator.cal_avg_data(self.monthly,
                                            self.__prices[self.monthly])

    def __set_time(self, url: str) -> str:
        st = datetime.datetime.now()
        et = st + relativedelta(years=-5)
        start_time_unix = str(et.timestamp()).split('.')[0]
        end_time_unix = str(st.timestamp()).split('.')[0]

        url = url.format(START_TIME_UNIX=start_time_unix,
                         END_TIME_UNIX=end_time_unix)
        return url

    @property
    def daily_avg_price(self) -> pd.Series:
        return self.__daily_avg

    @property
    def weekly_avg_price(self) -> pd.Series:
        return self.__weekly_avg

    @property
    def monthly_avg_price(self) -> pd.Series:
        return self.__monthly_avg


if __name__ == '__main__':
    pass
