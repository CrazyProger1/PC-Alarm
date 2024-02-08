from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings

from src.settings import (
    DEFAULT_SETTINGS_FILE,
    DEFAULT_DATABASE_FILE
)
from src.core.enums import ApplicationWorkingMode


class Arguments(BaseModel):
    mode: ApplicationWorkingMode = Field(ApplicationWorkingMode.BOT, description='application working mode')
    settings_file: str = Field(DEFAULT_SETTINGS_FILE, description='settings file path', alias='settings')


class DatabaseSettings(BaseSettings):
    file: str = Field(DEFAULT_DATABASE_FILE)


class BotSettings(BaseSettings):
    bot_token: str = Field(env='BOT_TOKEN')
    admin_id: int = Field(env='ADMIN_ID')


class ConfiguratorSettings(BaseSettings):
    language: str = 'en'


class Settings(BaseSettings):
    database: DatabaseSettings = DatabaseSettings()
    bot: BotSettings = BotSettings()
    configurator: ConfiguratorSettings = ConfiguratorSettings()
