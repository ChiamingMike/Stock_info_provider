import pandas as pd

from infocenter.logger.Log import log


class Calculator(object):

    def __init__(self) -> None:
        pass

    def cal_roe(self,
                net_income: pd.Series,
                equity: pd.Series) -> pd.Series:
        df = pd.DataFrame([net_income, equity]).astype("float")
        df.loc["ROE"] = round(
            (df.loc["Net Income"] / df.loc["Total Equity"]) * 100, 1)

        return df.loc["ROE"]

    def cal_roa(self,
                net_income: pd.Series,
                total_assets: pd.Series) -> pd.Series:
        df = pd.DataFrame([net_income, total_assets]).astype("float")
        df.loc["ROA"] = round(
            (df.loc["Net Income"] / df.loc["Total Assets"]) * 100, 1)

        return df.loc["ROA"]

    def cal_avg_data(self,
                     span: str,
                     df: pd.DataFrame) -> pd.Series:
        rs = pd.DataFrame(index=[span])
        for col in df.columns:
            s = df[col].dropna()
            rs[col] = round(sum(s) / len(s), 1)
            log.i(f"{span} {str(col)} : {rs.iat[0,-1]} = {sum(s)} / {len(s)}")

        return rs


if __name__ == "__main__":
    pass
