import logging
from typing import Callable, Optional
from numpy import isin
import yaml
from os import path

mapper_path = __path__[0] # type: ignore
version = ""

class Mapper:

    map: dict[str, str]

    def __init__(self):
        filename = f"default_{version}.yml" if version else "default.yml"

        with open(path.join(mapper_path, filename), 'r', encoding='utf-8') as f:
            result = yaml.load(f, Loader=yaml.SafeLoader)
        if not isinstance(result, dict):
            raise ValueError(f"Invalid mapping file {filename}")
        self.map = result

    def get_internal_string(self, key):
        try:
            return self.map[key]
        except KeyError:
            logging.warning(f"'{key}' not found in mapping file")
            return None

    def get_external_string(self, value):
        for key, val in self.map.items():
            if val == value:
                return key
        logging.warning(f"'{value}' not found in mapping file")
        return None

mapper = Mapper()

get: Callable[[str], Optional[str]] = mapper.get_internal_string
find: Callable[[str], Optional[str]] = mapper.get_external_string