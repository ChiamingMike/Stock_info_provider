from infocenter.logger.Log import log


class Provider(object):

    symbol = str()

    def __init__(self) -> None:
        self.url = str()

    def load_url(self, raw_url: str) -> None:
        self.url = self.__create_url(raw_url)
        return None

    def __create_url(self, raw_url) -> str:
        return raw_url.replace('SYMBOL', Provider.symbol)

    def _get_basic_url(self, key: str) -> str:
        return self.url_fmt.get(key)


if __name__ == '__main__':
    pass
