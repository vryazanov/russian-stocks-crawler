"""Scrapy settings are stored in this file."""

BASE_API_URL = 'http://localhost:5000/tickers/'

BOT_NAME = 'stocks'

SPIDER_MODULES = ['stocks.spiders']

NEWSPIDER_MODULE = 'stocks.spiders'

ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
    'stocks.pipelines.VerifyPipeline': 300,
    'stocks.pipelines.APIPipeline': 300,
}
