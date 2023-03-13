from app.database import Users
from app.utils.translator import _


class BotInteractionError(Exception):
    def __init__(self, user: Users, text: str):
        self.user = user
        self.text = text
        super(BotInteractionError, self).__init__(text)


class AccessError(BotInteractionError):
    pass


class MissingArgumentsError(BotInteractionError):
    def __init__(self, user: Users, missing_args):
        self.missing_args = missing_args
        super(MissingArgumentsError, self).__init__(
            user,
            _('Command arguments is missing: {args}',
              user=user).format(args=", ".join(missing_args))
        )


class TargetNotExistsError(BotInteractionError):
    def __init__(self, user: Users, target: str):
        self.target = target
        super(TargetNotExistsError, self).__init__(
            user,
            _('Target does not exists: {target}', user=user).format(target=target)
        )


class FileDoesNotExists(BotInteractionError):
    def __init__(self, user: Users, path: str):
        self.path = path
        super(FileDoesNotExists, self).__init__(
            user,
            _('File {path} does not exists!', user=user).format(path=path)
        )
