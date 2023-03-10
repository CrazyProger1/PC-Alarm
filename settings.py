from aiogram import types
from app.utils.config import JSONConfig, ENVConfig

FILES = {
    'JSON_CONFIG_FILE': 'config/config.json',
    'ENV_CONFIG_FILE': 'env/local.env',

}

json_conf = JSONConfig.load(FILES['JSON_CONFIG_FILE'])
env_conf = ENVConfig.load(FILES['ENV_CONFIG_FILE'])

DEBUG = True

APP = {
    'NAME': 'PC-Alarm',
    'VERSION': '0.1'
}

LOGGING = {
    'FILE': json_conf.logging.file,
    'FILEMODE': json_conf.logging.filemode,
    'LEVEL': json_conf.logging.level,
    'FORMAT': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'PRINT_LOG': DEBUG
}

BOT = {
    'TOKEN': env_conf.TOKEN,
    'ADMIN': env_conf.ADMIN
}

DATABASE = {
    'ENGINE': env_conf.DB_ENGINE,
    'PARAMS': {
        'database': env_conf.DB_FILE
    },
    'AUTHENTICATOR_CLASS': 'custom.CustomAuthenticator'
}

L18N = {
    'UI_LANGUAGE': json_conf.ui_language,
    'LOCALE_FOLDER': 'resources/languages',
    'BOT_DOMAIN': 'bot',
    'CONFIGURATOR_DOMAIN': 'configurator'
}

SUPPORT = {
    'TELEGRAM': 'crazyproger1'
}

COMMAND = {
    'PREFIX': '/',
    'REGEXP': fr'^\/\w+',
    'PARSER_CLASS': 'app.bot.types.Parser'
}

MIDDLEWARES = [
    'app.bot.middlewares.ErrorCatchingMiddleware',
    'app.bot.middlewares.AuthMiddleware',
    'app.bot.middlewares.PermissionMiddleware',
]

CATEGORIES = {
    'FOLDER': 'resources/categories'
}

MESSAGES = {
    'PARSE_MODE': types.ParseMode.MARKDOWN_V2
}
