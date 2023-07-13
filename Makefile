init:
	@pip install . .[lint] .[test] .[package]

lint:
	@isort -rc ./langchain_plantuml
	@pflake8 ./langchain_plantuml