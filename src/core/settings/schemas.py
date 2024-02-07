from pydantic import Field
from pydantic_settings import BaseSettings


class BotSettings(BaseSettings):
    bot_token: str = Field(env='BOT_TOKEN')
    admin_id: int = Field(env='ADMIN_ID')


class Settings(BaseSettings):
    bot: BotSettings = BotSettings()
