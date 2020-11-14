import pandas as pd

from infocenter.container.DataContainer import DataContainer
from infocenter.errors.Errors import BasicInfoError
from infocenter.logger.Log import log
from infocenter.provider.Provider import Provider
from infocenter.resorce.Property import Property


class BasicInfoProvider(Provider):

    def __init__(self) -> None:
        super().__init__()
        self.profile = "profile"
        self.__symbol_profile = dict()

        try:
            log.i("Preparing symbol profile...")
            self.url_fmt = Property(self.__class__.__name__).url_fmt
            self.data_container = DataContainer()
            self.load_url()
            log.i("Finished.")
        except Exception as e:
            log.e(e)
            raise BasicInfoError(
                "Error occurred when loading symbol profile.")

        return None

    def load_url(self) -> None:
        for key in [self.profile]:
            if not self._get_basic_url(key):
                log.e("URL format was not found.")
                log.e(f"Please check yaml file for {self.__class__.__name__}")
                break

            super().load_url(self._get_basic_url(key))
            rs = pd.read_html(self.url,
                              header=None,
                              index_col=0,
                              encoding="utf-8")
            df = pd.concat([rs[0], rs[1]], axis=0)
            item = df.index.values.tolist()
            val = df.iloc[:, 0].values.tolist()
            self.__symbol_profile[key] = pd.DataFrame({"Item": item,
                                                       "Value": val})

        self.data_container.register(self.__class__.__name__,
                                     self.__symbol_profile)
        return None

    @property
    def symbol_profile(self) -> pd.DataFrame:
        return self.__symbol_profile[self.profile]


if __name__ == "__main__":
    pass
