from pydantic import BaseModel, Field

from src.settings import SETTINGS_DEFAULT_FILE
from src.core.enums import ApplicationWorkingMode


class Arguments(BaseModel):
    mode: ApplicationWorkingMode = Field(ApplicationWorkingMode.BOT)
    settings_file: str = Field(SETTINGS_DEFAULT_FILE)
