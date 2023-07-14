init:
	@pip install . .[lint] .[test] .[package]

lint:
	@pip install .[lint]
	@pflake8 ./langchain_plantuml

fmt:
	@black ./langchain_plantuml
	@isort ./langchain_plantuml

release:
	python -m build
	twine check dist/*