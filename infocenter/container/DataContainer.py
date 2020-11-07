from infocenter.logger.Log import log


class DataContainer(object):

    __instance = None
    __is_initialized = False

    def __new__(cls):
        """
        """
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)

        return cls.__instance

    def __init__(self) -> None:
        if self.__is_initialized is True:
            return None

        self.__is_initialized = True

        self.data_map = dict()
        return None

    def get(self, provider: str) -> dict:
        log.i(f"Get info of {provider}")
        return self.data_map[provider]

    def register(self, provider: str, rs: dict) -> None:
        self.data_map[provider] = rs
        log.i(f"Register info of {provider}")
        return None


if __name__ == "__main__":
    pass
