import logging

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

# Settings
DEFAULT_SETTINGS_FILE = 'settings.toml'

# Database
DEFAULT_DATABASE_FILE = 'db.sqlite3'
OWNER_GROUP = 'owner'
ADMIN_GROUP = 'admin'

# Logging
LOGGING_LEVEL = logging.DEBUG
