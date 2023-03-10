class UserState:
    def __getattr__(self, item):
        return self.__dict__.get(item)

    def __getitem__(self, item):
        return self.__dict__.get(item)

    def __setattr__(self, key, value):
        self.__dict__[key] = value

    def __setitem__(self, key, value):
        self.__dict__[key] = value
