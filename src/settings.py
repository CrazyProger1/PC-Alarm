from dotenv import load_dotenv

load_dotenv()

# System
DEBUG = True
FOR_BUILD = True

if FOR_BUILD:
    import typeguard

    typeguard.typechecked = lambda func: func

# App info
APP = 'PC-Alarm'
VERSION = '0.0.2'

# Configurator
WINDOW_SIZE = (600, 400)
TITLE = f'{APP} - v{VERSION}'

# Core
SETTINGS_DEFAULT_FILE = 'settings.toml'
