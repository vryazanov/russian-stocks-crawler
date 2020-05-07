# Russian stocks crawler
A set of spiders to crawl data about stocks of Russian companies.

## Requirements
* python 3.8
* poetry (use `pip install poetry` if it's not installed yet)

## How to run locally?
* clone the repo from github
* run `poetry install` inside project's folder

## How to debug spider?
* execute `poetry run scrapy parse --spider smartlab -c parse https://smart-lab.ru/q/shares/`