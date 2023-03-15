<p align="center">
  <img src="https://github.com/CrazyProger1/PC-Alarm/blob/dev/resources/icons/alarm.png" alt="Alarm logo" width="256" height="256"/>
</p>

# PC-Alarm

PC-Alarm is an application that will help you detect someone else presence on your computer while you are away. It based
on Telegram API.

## Installation

## Configuration

## Development

**Note:** _Before starting, make sure you have installed [Python 3.11](https://www.python.org/downloads/)._

Firstly, you need to clone this GIT repository:

```shell
git clone https://github.com/CrazyProger1/PC-Alarm
```

Then, install the requirements:

```shell
pip install -r requirements.txt
```

That's all, now you can start bot with the command:

```shell
python main.py
```

To start the configurator use the following command:

```shell
python main.py --configurator
```

## Building

**Note:** _Make sure you have installed [PyInstaller](https://pypi.org/project/pyinstaller/)._

To build, execute the following command from base folder:

```commandline
"scripts/build.bat"
```

On Windows.

```bash
sh ./scripts/build.sh
```

On Linux.

Now, you can find an executable file at [dist/main](dist/main).

## L18N

**Available languages:**

- [x] Ukrainian
- [x] English

### Translation-Guide

Firstly, you need to go to folder: [resources/languages/pot](resources/languages/pot). There you will
find [.pot](https://en.wikipedia.org/wiki/Gettext) files.

Each part of the application has its own [.pot](https://en.wikipedia.org/wiki/Gettext) template:

- Configurator - [configurator.pot](resources/languages/pot/configurator.pot)
- Bot - [bot.pot](resources/languages/pot/bot.pot)

[.pot](https://en.wikipedia.org/wiki/Gettext) template files can be open with applications such as
[Poedit](https://poedit.net/), [Localizely](https://localizely.com/), [Transifex](https://www.transifex.com/) and many
others.

Tutorials:

- [Poedit](resources/docs/POEDIT.MD)

## TO-DO

- [x] Alarm (Main Goal)
- [x] L18N
    - [x] English
    - [x] Ukrainian

- [x] Pages
    - [x] Main
    - [x] Settings
    - [x] Interactive Actions
    - [x] L18N Settings

- [x] Interactive Actions / Commands
    - [x] Shutdown PC
    - [x] Restart PC
    - [x] End Session
    - [x] Say
    - [x] Music
    - [x] Beep
    - [x] Photo
    - [x] Screenshot

- [x] Configurator
    - [x] TOKEN
    - [x] Admin Telegram-ID
    - [x] UI L18N

## License

PC-Alarm is released under the MIT License. See the bundled [LICENSE](LICENSE) file for details.
