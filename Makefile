.PHONY: help clean dev docs package test

help:
	@echo "This project assumes that an active Python virtualenv is present."
	@echo "The following make targets are available:"
	@echo "	 dev 	install all deps for dev env"
	@echo "  docs	create pydocs for all relveant modules"
	@echo "	 test	run all tests with coverage"

clean:
	rm -rf dist/* build/*

dev:
	pip install twine
	pip install -e .[testing]

docs:
	$(MAKE) -C docs html

package:
	python setup.py sdist bdist_wheel
