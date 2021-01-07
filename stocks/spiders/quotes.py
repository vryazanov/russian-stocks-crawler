"""Scrapy spider that can parse historical quotes."""
import datetime
import typing
import urllib
import urllib.parse

import scrapy.linkextractors
import scrapy.spiders

from stocks import items


def build_qs_dict(
    finam_id: str, market_id: str, date_from: str, date_to: str,
) -> typing.Dict[str, typing.Union[str, int]]:
    """Build a dict that can be used to generate query string to export api."""
    df, mf, yf = list(map(int, date_from.split('.')))
    dt, mt, yt = list(map(int, date_to.split('.')))

    return {
        'market': market_id,
        'em': finam_id,
        'mstime': 'on',
        'mstimever': '1',
        'MSOR': '1',
        'tmf': '1',
        'dtf': '1',
        'apply': '0',
        'df': df,
        'dt': dt,
        'yf': yf,
        'yt': yt,
        'mt': mt - 1,  # months starts from 0
        'mf': mf - 1,
        'p': '8',
        'f': 'report',
        'e': '.txt',
        'sep': '1',
        'sep2': '1',
        'datf': '5',  # report type
        'at': '0',  # no headers
    }


class StockQuotesSpider(scrapy.spiders.CrawlSpider):
    """Main spider to crawl stock quotes.

    It uses finam.ru functionality to export quotes.
    """

    custom_settings = {
        'CONCURRENT_REQUESTS_PER_DOMAIN': 5,
        'DOWNLOAD_DELAY': 1,
    }

    name = 'quotes'
    allowed_domains = ('finam.ru',)
    start_urls = ('https://www.finam.ru/quotes/stocks/russia/',)

    base_export_url = 'http://export.finam.ru/export9.out'

    rules = (
        scrapy.spiders.Rule(
            scrapy.linkextractors.LinkExtractor(
                allow=('\\?pageNumber=[0-9]+$',),
            ),
        ),
        scrapy.spiders.Rule(
            scrapy.linkextractors.LinkExtractor(
                allow=('/profile/moex-akcii/[0-9a-zA-Z-]+/$',),
            ),
        ),
        scrapy.spiders.Rule(
            scrapy.linkextractors.LinkExtractor(
                allow=('/profile/moex-akcii/[0-9a-zA-Z-]+/export',),
            ),
            callback='parse_export',
        ),
    )

    def __init__(self, date_from: str, date_to: str):
        """Primary constructor."""
        super().__init__()
        self.date_from = datetime.datetime.strptime(date_from, '%Y-%m-%d')
        self.date_to = datetime.datetime.strptime(date_to, '%Y-%m-%d')

    def parse_export(self, response):
        """Extract meta data about ticker in order to run export."""
        ticker = response.xpath('//input[@name="code"]/@value').get()
        finam_id = response.xpath('//input[@name="em"]/@value').get()
        market_id = response.xpath('//input[@name="market"]/@value').get()

        querystring = urllib.parse.urlencode(
            build_qs_dict(
                finam_id,
                market_id,
                self.date_from.strftime('%d.%m.%Y'),
                self.date_to.strftime('%d.%m.%Y'),
            ),
        )

        yield scrapy.Request(
            url=f'{self.base_export_url}?{querystring}',
            callback=self.parse_quotes,
            meta={'ticker': ticker.upper()},
        )

    def parse_quotes(self, response):
        """Extract stock quotes for date range for specific ticker."""
        for line in response.body.decode().strip().split('\r\n'):
            if not line:
                continue

            raw_date, _, open_price, _, _, close_price, _ = line.split(',')

            date = datetime.datetime.strptime(raw_date, '%Y%m%d').date()

            yield items.StockQuoteItem(
                ticker=response.meta['ticker'],
                date=date.isoformat(),
                open_price=open_price,
                close_price=close_price,
            )
