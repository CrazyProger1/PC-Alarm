from app.database import Users
from .types import Page
from .permissions import IsNotBanned


class MainPage(Page):
    path = 'main'
    default = True
    permission_classes = (
        IsNotBanned,
    )

