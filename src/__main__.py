import asyncio

from src.settings import FOR_BUILD
from src.configurator import run_configurator


async def main():
    await run_configurator()


if __name__ == '__main__':
    asyncio.run(main())
