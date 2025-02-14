from pathlib import Path


def absolute_path(relative_path: str = '') -> Path:
    current_file_path = Path(__file__).resolve()
    package_path = current_file_path.parent
    target_path = package_path / relative_path
    return target_path