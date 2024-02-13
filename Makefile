.PHONY: run-bot
run-bot:
	poetry run python -m src -m bot

.PHONY: run-configurator
run-configurator:
	poetry run python -m src -m configurator


.PHONY: extract-translations
extract-translations:
	poetry run python -m i18n src "resources/languages/PC-Alarm.pot"


.PHONY: test
test:
	poetry run python -m pytest tests/



.PHONY: build
build:
	poetry run pyinstaller -F -w --name PC-Alarm --icon "resources/images/icons/base.ico" --add-data="resources;." src/__main__.py


.PHONY: build-debug
build-debug:
	poetry run pyinstaller -F --name PC-Alarm-Debug --icon "resources/imgs/icons/base.ico" --add-data="resources;." src/__main__.py

