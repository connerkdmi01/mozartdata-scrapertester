

setup:
	@echo "Setting up"
	/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
	brew install pyenv pyenv-virtualenv 2> /dev/null || true
	brew upgrade pyenv pyenv-virtualenv 2> /dev/null || true
	pyenv rehash
	pyenv install -s 3.9.7
	pyenv virtualenv 3.9.7 scraper
	pyenv local scraper
	pyenv activate scraper
	pip install -r requirements.txt


.PHONY: setup

