import pandas as pd

from infocenter.logger.Log import log
from infocenter.provider.BasicInfoProvider import BasicInfoProvider
from infocenter.provider.FinancialReportsProvider import FinancialReportsProvider
from infocenter.provider.FundamentalInfoProvider import FundamentalInfoProvider
from infocenter.provider.AverageDataProvider import AverageDataProvider
from infocenter.provider.Provider import Provider

from infocenter.errors.Errors import BasicInfoError
from infocenter.errors.Errors import FinancialReportsError
from infocenter.errors.Errors import FundamentalInfoError
from infocenter.errors.Errors import AverageDataError


class StockInfoCenter(object):

    def __init__(self, symbol) -> None:
        Provider.symbol = symbol
        self.is_info_extracted = self.__ask_info()

        # try:
        #     if self.__can_pickup(symbol):
        #         log.i(f"Picked up {symbol}")
        # except Exception:
        #     log.e("Failed to pick up")

        return None

    def tell_me(self) -> dict:
        if not self.is_info_extracted:
            return dict()

        msg = {
            "profile": self.basic_info.symbol_profile,
            "Recent five years": pd.concat([self.fundamental_info.net_income,
                                            self.fundamental_info.ROE,
                                            self.fundamental_info.ROA],
                                           axis=1),
            "Average price": pd.concat([self.average_data.daily_avg_price,
                                        self.average_data.weekly_avg_price,
                                        self.average_data.monthly_avg_price],
                                       axis=0)
        }

        return msg

    def __ask_info(self) -> bool:
        try:
            self.basic_info = BasicInfoProvider()
            self.financial_info = FinancialReportsProvider()
            self.fundamental_info = FundamentalInfoProvider()
            self.average_data = AverageDataProvider()
        except BasicInfoError as e:
            log.e(e)
            return False
        except FinancialReportsError as e:
            log.e(e)
            return False
        except FundamentalInfoError as e:
            log.e(e)
            return False
        except AverageDataError as e:
            log.e(e)
            return False
        except Exception as e:
            log.e(e)
            log.e("Unexcepted error occurred.")
            return False

        return True

    def __can_pickup(self, symbol) -> bool:
        roa_avg = round(self.fundamental_info.ROA.mean(), 2)
        roe_avg = round(self.fundamental_info.ROE.mean(), 2)
        with open("./output.txt", mode="a", encoding="utf-8") as f:
            line = f"{symbol}\t{roa_avg}\t{roe_avg}"
            f.write(line)
            f.write("\n")

        if roa_avg > 5 and roe_avg > 15:
            return True

        return False


if __name__ == '__main__':
    pass
