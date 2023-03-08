from app.database import Users
from app.utils.translator import _
from app.bot import events
from .types import Page
from .permissions import IsNotBanned


class MainPage(Page):
    path = 'main'
    default = True
    permission_classes = (
        IsNotBanned,
    )

    def __init__(self, *args, **kwargs):
        super(MainPage, self).__init__(*args, **kwargs)
        _('test')
