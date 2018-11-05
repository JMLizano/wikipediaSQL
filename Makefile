
#################
#  Common vars	#
#################

export PIPENV_VENV_IN_PROJECT := true   ##=> Tell pipenv to create virtualenv inside current project ($(pwd)/.venv)
export PIPENV_IGNORE_VIRTUALENVS := 1   ##=> Tell pipenv to always create its own venv

BASE := $(shell /bin/pwd)

SERVICE = wikipediasql


target:
	$(info ${HELP_MESSAGE})
	@exit 0

clean: ##=> Deletes current build environment and latest build
	$(info [*] Who needs all that anyway? Destroying environment....)
	rm -rf ./${SERVICE}.zip
	find . -type d -name '*pycache*' -exec rm -rf {} +
	find . -name '*.pyc' -exec rm --force {} \;
	rm Pipfile.lock || exit 0
	@pipenv --rm || exit 0

all: clean install

install: 
	$(info [+] Installing '$(SERVICE)' dependencies...")
	pip install pipenv
	pipenv install --skip-lock -d

deploy:
	VIRTUAL_ENV=.venv/ pipenv run zappa deploy

update:
	VIRTUAL_ENV=.venv/ pipenv run zappa update

shell:
	@pipenv shell

run: ##=> Run Local Flask development server
	FLASK_APP=wikipediasql.app FLASK_ENV=development pipenv run flask run

test: ##=> Run tests for the project
	pipenv run python -m unittest discover -v -s tests

define HELP_MESSAGE
	Environment variables to be aware of or to hardcode depending on your use case:

	SERVICE
		Default: not_defined
		Info: Environment variable to declare where source code for lambda is

	Common usage:

	...::: Installs all required packages as defined in the pipfile :::...
	$ make install

	...::: Spawn a virtual environment shell :::...
	$ make shell

	...::: Cleans up the environment - Deletes Virtualenv, ZIP builds and Dev env :::...
	$ make clean

	...::: Run local development Flask server :::...
	$ make run

	...::: Run unittests under tests/ :::...
	$ make test
endef

