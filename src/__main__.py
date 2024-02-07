import asyncio

from src.configurator import run_configurator


async def main():
    await run_configurator()


if __name__ == '__main__':
    asyncio.run(main())
