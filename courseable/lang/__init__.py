from typing import Callable
import yaml
from ..utils import absolute_path

lang_path = absolute_path("lang")

class I18n:

    language: str
    i18n_map: dict[str, str]

    def __init__(self, language: str = 'zh-CN'):
        self.set_language(language)

    def set_language(self, language: str):
        with open(lang_path / f"{language}.yml", 'r', encoding='utf-8') as f:
            result = yaml.load(f, Loader=yaml.SafeLoader)
        if not isinstance(result, dict):
            raise ValueError(f"Invalid i18n file {language}.yml")
        self.i18n_map = result

    def localize(self, key):
        return self.i18n_map.get(key, key)

i18n = I18n()

_: Callable[[str], str] = i18n.localize