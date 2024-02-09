import os.path


class SettingsError(Exception):
    pass


class LoaderNotFoundError(SettingsError):
    def __init__(self, file: str):
        self.file = file

        super().__init__(f'Loader for {self.file} not found')


class FileFormatError(SettingsError):
    def __init__(self, file: str, msg: str):
        self.file = file
        super().__init__(msg)
