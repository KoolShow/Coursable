import logging
from typing import Callable, Optional
import yaml

from ..utils import absolute_path

mapper_path = absolute_path('mapping')
version = ""

class Mapper:

    map: dict[str, str]

    def __init__(self):
        filename = f"default_{version}.yml" if version else "default.yml"

        with open(mapper_path / filename, 'r', encoding='utf-8') as f:
            result = yaml.load(f, Loader=yaml.SafeLoader)
        if not isinstance(result, dict):
            raise ValueError(f"Invalid mapping file {filename}")
        self.map = result

    def to_internal(self, key):
        try:
            return self.map[key]
        except KeyError:
            logging.warning(f"'{key}' not found in mapping file")
            return None

    def to_external(self, value):
        for key, val in self.map.items():
            if val == value:
                return key
        logging.warning(f"'{value}' not found in mapping file")
        return None

mapper = Mapper()

to_internal: Callable[[str], Optional[str]] = mapper.to_internal
to_external: Callable[[str], Optional[str]] = mapper.to_external