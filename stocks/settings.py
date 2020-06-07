"""Scrapy settings are stored in this file."""
import os


OPENAPI_URL = os.environ['OPENAPI_URL']

OPENAPI_TOKEN = os.environ['OPENAPI_TOKEN']

BOT_NAME = 'stocks'

SPIDER_MODULES = ['stocks.spiders']

NEWSPIDER_MODULE = 'stocks.spiders'

ROBOTSTXT_OBEY = False

ITEM_PIPELINES = {
    'stocks.pipelines.VerifyPipeline': 300,
    'stocks.pipelines.APIPipeline': 300,
}
