from app.utils.config import JSONConfig, ENVConfig

json_conf = JSONConfig.load('config/config.json')

APP_NAME = 'PC-Alarm'

LOGGING = {
    'FILE': json_conf.logging.file,
    'FILEMODE': json_conf.logging.filemode,
    'LEVEL': json_conf.logging.level,
    'FORMAT': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'PRINT_LOG': True
}
