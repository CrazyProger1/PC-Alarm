.PHONY: run
run:
	poetry run python -m src


.PHONY: extract-translations
extract-translations:
	poetry run python -m src.utils.i18n "src/__main__.py" "resources/i18n/PC-Alarm.po"


.PHONY: test
test:
	poetry run python -m pytest tests/



.PHONY: build
build:
	poetry run pyinstaller -F -w --name PC-Alarm --icon "resources/imgs/icons/base.ico" --add-data="resources;." src/__main__.py

