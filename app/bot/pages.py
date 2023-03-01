from app.database import Users
from .types import Page
from .permissions import IsNotBanned
from .router import Router


class MainPage(Page):
    path = 'main'
    default = True
    permission_classes = (
        IsNotBanned,
    )

    async def on_initialize(self, user: Users):
        pass
