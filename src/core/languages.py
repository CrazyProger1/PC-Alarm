import os

from src.settings import LOCALE_DIR


def get_available_languages(localedir: str = LOCALE_DIR) -> list[str]:
    languages = []

    for file in os.listdir(localedir):
        file = os.path.join(localedir, file)
        if os.path.isdir(file):
            languages.append(
                os.path.split(file)[1][:2]
            )
    return languages
