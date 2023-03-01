class Router:
    def __init__(self, bot):
        self._bot = bot

    def get_page(self, user):
        pass

    async def route_callback(self, callback, user):
        pass

    async def route_message(self, message, user):
        pass

    async def route_command(self, message, user):
        pass

    async def route_media(self, message, user):
        pass

    async def set_page(self, path: str):
        pass
