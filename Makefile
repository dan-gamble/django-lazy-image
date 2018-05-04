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
	pip install pip -U
	pip install twine
	pip install -e .[testing]

docs:
	$(MAKE) -C docs html

package:
	python setup.py sdist bdist_wheel

test:
	pylint django_lazy_image/ --load-plugins pylint_django,pylint_mccabe --ignore=migrations,tests -d missing-docstring,invalid-name,no-init,too-many-ancestors,no-member,line-too-long,attribute-defined-outside-init,too-few-public-methods,no-self-use,unused-argument,protected-access,locally-disabled,duplicate-code,ungrouped-imports,not-context-manager,fixme --reports=n
	isort --check-only --diff --quiet --skip-glob=venv
