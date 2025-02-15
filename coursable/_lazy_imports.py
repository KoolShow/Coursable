from types import ModuleType


extra_table = {
    "main": ["yaml","pytz"],
    "url": ["requests"],
    "orjson": ["orjson"],
    "ujson": ["ujson"],
    "ics": ["icalendar"],
    "dev": ["coverage","mypy","pylint"]
}

def find_extra(module_name):
    for key, value in extra_table.items():
        if module_name in value:
            return key
    return None

def generate_exception_message(module_name):
    extra = find_extra(module_name)
    match extra:
        case "main":
            return f"Failed to import {module_name}. Please try to reinstall coursable."
        case None:
            return f"Failed to import {module_name}."
        case _ as e:
            return f"Failed to import {module_name}. Please try to install coursable with extras {e}."

def require(module_name) -> ModuleType:
    try:
        return __import__(module_name)
    except ImportError as e:
        raise ImportError(generate_exception_message(module_name)) from e
