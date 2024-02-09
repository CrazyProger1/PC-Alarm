import os.path


class SettingsError(Exception):
    pass


class LoaderNotFoundError(SettingsError):
    def __init__(self, file: str):
        self.file = file
        self.filetype = os.path.splitext(file)[1]
        super().__init__(f'Loader for {self.filetype} not found')


class FileFormatError(SettingsError):
    def __init__(self, file: str, msg: str):
        self.file = file
        super().__init__(msg)
