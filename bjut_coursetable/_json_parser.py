from typing import LiteralString, Self, TextIO
import logging
import traceback
from types import ModuleType
from typing import Optional

_json_modules = ["orjson", "ujson", "json"]


class JSONParser:

    module: ModuleType
    parser: str

    def __init__(self, module: ModuleType):
        self.module = module
        self.parser = module.__name__

    def __new__(cls, module: ModuleType):
        if cls is not JSONParser:
            return object.__new__(cls)

        match module.__name__:
            case "orjson":
                return OrJSON(module)
            case "ujson":
                return UJSON(module)
            case "json":
                return JSON(module)
            case _:
                raise ValueError(f"Unknown JSON parser: {module.__name__}")

    def __repr__(self) -> str:
        return f"JSONParser({self.parser})"

    def parse_file(self, file: TextIO) -> dict:
        raise NotImplementedError

    def parse_str(self, data: str) -> dict:
        raise NotImplementedError


parser: Optional[JSONParser] = None


class OrJSON(JSONParser):

    def parse_file(self, file: TextIO) -> dict:
        return self.module.loads(file.read())

    def parse_str(self, data: str) -> dict:
        return self.module.loads(data)


class UJSON(JSONParser):

    def parse_file(self, file: TextIO) -> dict:
        return self.module.load(file)

    def parse_str(self, data: str) -> dict:
        return self.module.loads(data)


class JSON(JSONParser):

    def parse_file(self, file: TextIO) -> dict:
        return self.module.load(file)

    def parse_str(self, data: str) -> dict:
        return self.module.loads(data)


def get_json_parser() -> JSONParser:
    global parser
    if parser:
        return parser

    for module_name in _json_modules:
        try:
            module: ModuleType = __import__(module_name)
            parser = JSONParser(module)
            return parser

        except ModuleNotFoundError:
            logging.info(f"{module_name} not found")

        except Exception:
            logging.error(traceback.format_exc())

    raise ModuleNotFoundError("Could not found an available JSON parser")
