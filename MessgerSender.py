import argparse
import pandas as pd
import time

from infocenter.logger.Log import log
from infocenter.StockInfoCenter import StockInfoCenter


class MessengerSender(object):

    def __init__(self) -> None:
        self.first_symbol = pd.DataFrame()
        return None

    def get_first_section_symbol(self) -> list:
        self.__extract_first_section_symbol()
        local_code = self.first_symbol["Local Code"]
        return local_code.tolist()

    def __extract_first_section_symbol(self) -> None:
        df = pd.read_csv("./data_e.csv")
        first_section = "First Section (Domestic)"
        self.first_symbol = df[df["Section/Products"].isin([first_section])]

        return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Request investment info")
    parser.add_argument(
        "symbol", help="Enter the stock stmbol to get investment info. ie: 8766.T")
    args = parser.parse_args()
    info_center = StockInfoCenter(args.symbol)
    for i in [args.symbol]:
        info = info_center.tell_me()
        if info == dict():
            log.e("Error occurred!")
        else:
            for _, v in info.items():
                print("*"*30)
                print(v)
                print("*"*30)
