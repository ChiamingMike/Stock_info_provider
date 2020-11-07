import pandas as pd

from infocenter.container.DataContainer import DataContainer
from infocenter.errors.Errors import FinancialReportsError
from infocenter.logger.Log import log
from infocenter.provider.Provider import Provider
from infocenter.resorce.Property import Property


class FinancialReportsProvider(Provider):

    def __init__(self) -> None:
        super().__init__()
        self.bs = "balance_sheet_annual"
        self.pl = "income_statement_annual"
        self.cf = "cash_flow_annual"
        self.__financial_reports = dict()

        try:
            log.i("Preparing financial reports...")
            self.url_fmt = Property(self.__class__.__name__).url_fmt
            self.data_container = DataContainer()
            self.load_url()
            log.i("Finished.")
        except Exception as e:
            log.e(e)
            raise FinancialReportsError(
                "Error occurred when loading financial statements.")

        return None

    def load_url(self) -> None:
        for key in [self.bs, self.pl, self.cf]:
            if not self._get_basic_url(key):
                log.e("URL format was not found.")
                log.e(f"Please check yaml file for {self.__class__.__name__}")
                break

            super().load_url(self._get_basic_url(key))
            rs = pd.read_html(self.url,
                              header=None,
                              index_col=0,
                              encoding="utf-8")

            # drop last column of DataFrame named Trend
            rs[0].drop(rs[0].columns[[-1]], axis=1, inplace=True)
            rs[0].columns = ["past 1 year",
                             "past 2 year",
                             "past 3 year",
                             "past 4 year",
                             "past 5 year"]
            self.__financial_reports[key] = rs[0]

        self.data_container.register(self.__class__.__name__,
                                     self.__financial_reports)
        return None

    @property
    def balance_sheet_annual(self) -> pd.DataFrame:
        return self.__financial_reports[self.bs]

    @property
    def income_statement_annual(self) -> pd.DataFrame:
        return self.__financial_reports[self.pl]

    @property
    def cash_flow_annual(self) -> pd.DataFrame:
        return self.__financial_reports[self.cf]


if __name__ == "__main__":
    pass
