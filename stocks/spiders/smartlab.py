"""Scrapy spider that can parse smart-lab.ru website."""
import json

import scrapy.linkextractors
import scrapy.spiders

from stocks import items, processors


class SmartlabSpider(scrapy.spiders.CrawlSpider):
    """Main spider."""

    name = 'smartlab'
    allowed_domains = ('smart-lab.ru', 'iss.moex.com',)
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

    moex_details = 'https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities/{ticker}.jsonp'  # noqa

    def parse_start_url(self, response):
        """Extract stocks from the list page."""
        names = response.xpath('//td[3]/a/text()').getall()
        tickers = response.xpath('//td[4]/text()').getall()

        for name, ticker in zip(names, tickers):
            ticker = ticker.upper()
            item = items.StockItem(name=name, code=ticker)

            yield scrapy.Request(
                self.moex_details.format(ticker=ticker),
                meta={'item': item}, callback=self.parse_moex)

    def parse_moex(self, response):
        """Parse lot size from moex api."""
        item = response.meta['item']

        try:
            structured = json.loads(response.text)
        except Exception as e:
            return item

        try:
            item['lot'] = structured['securities']['data'][0][4]
        except Exception as e:
            pass

        return item

    def parse_payment(self, response):
        """Extract ticker, payment date and payment size from page."""
        xpath = "(//table[contains(@class, 'dividends')])/tr[@class='header_row']/following-sibling::tr"  # noqa

        for ticker, date, amount in zip(
            response.xpath(f'{xpath}/td[1]/text()').getall(),
            response.xpath(f'{xpath}/td[3]/text()').getall(),
            response.xpath(f'{xpath}/td[6]/strong/text()').getall(),
        ):
            yield items.PaymentItem(
                ticker=ticker.upper(),
                date=processors.extract_date(date),
                amount=processors.extract_amount(amount),
                is_forecast=(
                    processors.is_forecast(amount) or
                    processors.is_forecast(date)),
            )
