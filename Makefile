.PHONY: run
run:
	poetry run python src


.PHONY: extract-translations
extract-translations:
	poetry run python -m src.utils.i18n "src/__main__.py" "resources/i18n/PC-Alarm.po"


.PHONY: test
test:
	poetry run python -m pytest tests/