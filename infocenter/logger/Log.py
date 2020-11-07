import logging


class Log(object):

    __instance = None
    __is_initialized = False

    def __new__(cls):
        """
        """
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)

        return cls.__instance

    def __init__(self):
        if self.__is_initialized is True:
            return None

        self.__is_initialized = True

        self.logger = logging.getLogger(__name__)

        log_fmt = "%(asctime)s %(levelname)s:        %(message)s"
        self.log_level = logging.INFO

        logging.basicConfig(level=self.log_level,
                            format=log_fmt,
                            datefmt="%Y-%m-%d %H:%M:%S")
        return None

    def c(self, msg) -> None:
        self.logger.log(logging.CRITICAL, str(msg))
        return None

    def e(self, msg) -> None:
        self.logger.log(logging.ERROR, str(msg))
        return None

    def w(self, msg) -> None:
        self.logger.log(logging.WARNING, str(msg))
        return None

    def i(self, msg) -> None:
        self.logger.log(logging.INFO, str(msg))
        return None


log = Log()
