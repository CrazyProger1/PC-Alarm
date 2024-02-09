from src.settings import (
    APP,
    DESCRIPTION,
    ENV_FILE
)
from src.utils.arguments import SchemedArgumentParser
from src.core.utils import (
    load_settings,
    save_settings,
    parse_arguments
)
from src.core.schemas import (
    Settings,
    Arguments,
    ENVSettings
)

from src.types import (
    BaseApplicationFactory
)


async def run(factory: type[BaseApplicationFactory]):
    arguments = parse_arguments(
        parser=SchemedArgumentParser(
            schema=Arguments,
            prog=APP,
            description=DESCRIPTION
        )
    )

    settings = load_settings(
        file=arguments.settings_file,
        schema=Settings
    )
    settings.env = load_settings(
        file=ENV_FILE,
        schema=ENVSettings
    )

    app = factory.create(
        arguments=arguments,
        settings=settings
    )

    await app.run()

    save_settings(
        file=arguments.settings_file,
        instance=settings,
        exclude=('env',)
    )
    save_settings(
        file=ENV_FILE,
        instance=settings.env,
    )
