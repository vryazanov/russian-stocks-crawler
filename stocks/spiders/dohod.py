"""Scrapy spider that can parse dohod.ru website."""
import scrapy.linkextractors
import scrapy.spiders

from stocks import items, processors


class DohodSpider(scrapy.spiders.CrawlSpider):
    """Main spider."""

    name = 'dohod'
    allowed_domains = ('dohod.ru',)
    start_urls = ('https://www.dohod.ru/ik/analytics/dividend',)
    rules = (
        scrapy.spiders.Rule(
            scrapy.linkextractors.LinkExtractor(
                allow=('/ik/analytics/dividend/[0-9a-zA-Z]+$',),
            ),
            callback='parse_payments',
        ),
    )

    def parse_payments(self, response):
        """Extract ticker, payment date and payment size from page."""
        xpath = '//table[3]/tr'
        ticker = response.url.split('/')[-1].upper()

        for date, amount in zip(
            response.xpath(f'{xpath}/td[1]/text()').getall(),
            response.xpath(f'{xpath}/td[3]/text()').getall(),
        ):
            yield items.PaymentItem(
                ticker=ticker.upper(),
                declaration_date=processors.extract_date(date),
                amount=processors.extract_amount(amount),
                is_forecast=(
                    processors.is_forecast(amount) or
                    processors.is_forecast(date)),
            )
