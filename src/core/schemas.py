from pydantic import BaseModel, Field

from src.settings import (
    DEFAULT_SETTINGS_FILE,
    DEFAULT_DATABASE_FILE
)
from src.core.enums import ApplicationWorkingMode


class Arguments(BaseModel):
    mode: ApplicationWorkingMode = Field(ApplicationWorkingMode.BOT, description='application working mode')
    settings_file: str = Field(DEFAULT_SETTINGS_FILE, description='settings file path', alias='settings')


class DatabaseSettings(BaseModel):
    file: str = Field(DEFAULT_DATABASE_FILE)


class ENVSettings(BaseModel):
    bot_token: str = Field(alias='BOT_TOKEN')
    admin_id: int = Field(alias='ADMIN_ID')


class BotSettings(BaseModel):
    pass


class ConfiguratorSettings(BaseModel):
    language: str = 'en'


class Settings(BaseModel):
    database: DatabaseSettings = DatabaseSettings()
    bot: BotSettings = BotSettings()
    configurator: ConfiguratorSettings = ConfiguratorSettings()
    env: ENVSettings | None = None
