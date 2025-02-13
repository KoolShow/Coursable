from typing import Callable
from numpy import isin
import yaml
from os import path

lang_path = __path__[0] # type: ignore

class I18n:

    language: str
    i18n_map: dict[str, str]

    def __init__(self, language: str = 'zh-CN'):
        self.set_language(language)

    def set_language(self, language: str):
        with open(path.join(lang_path, f"{language}.yml"), 'r', encoding='utf-8') as f:
            result = yaml.load(f, Loader=yaml.SafeLoader)
        if not isinstance(result, dict):
            raise ValueError(f"Invalid i18n file {language}.yml")
        self.i18n_map = result

    def get_local_string(self, key):
        return self.i18n_map.get(key, key)

i18n = I18n()

_: Callable[[str], str] = i18n.get_local_string