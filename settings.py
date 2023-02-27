from app.utils.config import JSONConfig, ENVConfig

JSON_CONFIG_FILE = 'config/config.json'
ENV_CONFIG_FILE = 'env/local.env'

json_conf = JSONConfig.load(JSON_CONFIG_FILE)
env_conf = ENVConfig.load(ENV_CONFIG_FILE)

DEBUG = True

APP = {
    'NAME': 'PC-Alarm',
    'VERSION': '0.0'
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

LANGUAGE = {
    'UI_LANGUAGE': json_conf.ui_language,
    'FILE_EXTENSIONS': ('.json', '.lang'),
    'PACKS_FOLDER': 'resources/languages'
}

SUPPORT = {
    'TELEGRAM': 'crazyproger1'
}

COMMAND = {
    'PREFIX': '/',
    'REGEXP': fr'^\/\w+'
}

MIDDLEWARES = [
    'app.bot.middlewares.ErrorCatchingMiddleware',
    'app.bot.middlewares.AuthMiddleware',
    'app.bot.middlewares.PermissionMiddleware',
]
