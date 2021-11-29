# MozartData-ScraperTester

## Dev Environment Setup

In a terminal:

```
xcode-select --install

cd ~
git clone https://github.com/connerkdmi01/mozartdata-scrapertester.git
cd mozartdata-scrapertester
```

## Setup and running the app use this repo's Makefile

The following command will install pyenv, create a pyenv-virtualenv, and install requirements.

```
make setup
```

## Running the script

```
pyenv activate scraper
python scraper.py
```
