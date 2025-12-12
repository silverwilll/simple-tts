.PHONY: run install venv

venv:
	python3 -m venv .venv

install: venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -r requirements.txt

run:
	@if [ -x .venv/bin/streamlit ]; then \
		.venv/bin/streamlit run app.py; \
	else \
		streamlit run app.py; \
	fi