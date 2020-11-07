import yaml
import os
from infocenter.logger.Log import log


class Property(object):

    def __init__(self, cls_name: str) -> None:
        self.__url_fmt = str()
        self.cls_name = cls_name
        self.__load_property()

        return None

    def __load_property(self) -> None:
        fp = str()
        file_list = list()

        for curDir, _, files in os.walk(os.path.dirname(__file__)):
            file_list = list(filter(lambda x: x.endswith(".yaml"), files))

            if len(file_list) == 1:
                fp = curDir + "\\" + file_list[0]
                break

            else:
                log.e("More than one yaml file is found.")
                return None

        with open(fp) as file:
            self.__url_fmt = yaml.safe_load(file.read())

        return None

    @property
    def url_fmt(self) -> dict:
        return self.__url_fmt[self.cls_name]


if __name__ == "__main__":
    pass
