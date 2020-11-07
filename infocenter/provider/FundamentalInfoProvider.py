import pandas as pd

from infocenter.calculator.Calculator import Calculator
from infocenter.container.DataContainer import DataContainer
from infocenter.errors.Errors import FundamentalInfoError
from infocenter.logger.Log import log
from infocenter.provider.Provider import Provider


class FundamentalInfoProvider(Provider):

    def __init__(self) -> None:
        try:
            log.i("Preparing fundamental info...")
            self.data_container = DataContainer()
            self.calculator = Calculator()
            self.financial_statements = self.data_container.get(
                "FinancialReportsProvider")
            self.pl = self.financial_statements["income_statement_annual"]
            self.bs = self.financial_statements["balance_sheet_annual"]

            self.__roe = self.get_roe()
            self.__roa = self.get_roa()
            self.__net_income = self.get_net_income()
            log.i("Finished.")
        except Exception as e:
            log.e(e)
            raise FundamentalInfoError(
                "Error occurred when loading fundamental info.")

        return None

    def load_url(self) -> None:
        return None

    def get_net_income(self) -> pd.Series:
        return self.pl.loc["Net Income"]

    def get_roe(self) -> pd.Series:
        return self.calculator.cal_roe(self.pl.loc["Net Income"],
                                       self.bs.loc["Total Equity"])

    def get_roa(self) -> pd.Series:
        return self.calculator.cal_roa(self.pl.loc["Net Income"],
                                       self.bs.loc["Total Assets"])

    @property
    def net_income(self) -> pd.Series:
        return self.__net_income

    @property
    def ROE(self) -> pd.Series:
        return self.__roe

    @property
    def ROA(self) -> pd.Series:
        return self.__roa


if __name__ == "__main__":
    pass
