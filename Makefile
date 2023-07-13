init:
	@pip install . .[lint] .[test] .[package]

lint:
	@pip install .[lint]
	@pflake8 ./langchain_plantuml

fmt:
	@isort ./langchain_plantuml

release:
	python -m build
	twine check dist/*