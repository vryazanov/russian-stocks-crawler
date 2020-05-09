"""Scrapy spider that can parse smart-lab.ru website."""
import datetime
import typing

import scrapy.linkextractors
import scrapy.spiders

from stocks import items


def extract_amount(value: str) -> typing.Optional[float]:
    """Extract amount from raw string.

    >>> extract_amount('0,65 П')
    0.65
    >>> extract_amount('213')
    213.0
    >>> extract_amount('some text')
    """
    value = value.replace('П', '').replace(',', '.').strip()

    try:
        return float(value)
    except Exception:
        return None


def extract_date(value: str) -> typing.Optional[str]:
    """Extract date from value, return None if there is no date.

    >>> extract_date('18.07.2020 П')
    '2020-07-18'
    """
    value = value.replace('П', '').replace(',', '.').strip()

    try:
        value = datetime.datetime.strptime(value, '%d.%m.%Y')
    except ValueError:
        return None

    return value.date().isoformat()


class SmartlabSpider(scrapy.spiders.CrawlSpider):
    """Main spider."""

    name = 'smartlab'
    allowed_domains = ('smart-lab.ru',)
    start_urls = ('https://smart-lab.ru/q/shares/',)
    rules = (
        scrapy.spiders.Rule(
            scrapy.linkextractors.LinkExtractor(
                allow=('/forum/[0-9a-zA-Z]+$',),
            ),
        ),
        scrapy.spiders.Rule(
            scrapy.linkextractors.LinkExtractor(
                allow=('/dividend/',),
            ),
            callback='parse_payment',
        ),
    )

    def parse_start_url(self, response):
        """Extract stocks from the list page."""
        names = response.xpath('//td[3]/a/text()').getall()
        tickers = response.xpath('//td[4]/text()').getall()

        for name, ticker in zip(names, tickers):
            yield items.StockItem(name=name, ticker=ticker)

    def parse_payment(self, response):
        """Extract ticker, payment date and payment size from page."""
        xpath = "//table[contains(@class, 'dividends')]/*"

        for ticker, date, amount in zip(
            response.xpath(f'{xpath}/td[1]/text()').getall(),
            response.xpath(f'{xpath}/td[3]/text()').getall(),
            response.xpath(f'{xpath}/td[6]/strong/text()').getall(),
        ):
            yield items.PaymentItem(
                ticker=ticker,
                declaration_date=extract_date(date),
                amount=extract_amount(amount),
                is_forecast=False,
            )
