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

## Data sources
Here is a list of websites we are using to crawl financial data:
* [x] https://smart-lab.ru/
* [x] https://www.dohod.ru/

## Format of crawled data

* Ticker
  * Name (string, example: `Lukoil`)
  * Ticker (string, example: `LKOH`)
* Dividend payments (historical data and forecasts)
  * Ticker (example: `LKOH`)
  * Declaration date (iso format, example: `2020-05-01`)
  * Amount (decimal, example `12.45`)
  * Is forecast flag  (boolean, true or false)