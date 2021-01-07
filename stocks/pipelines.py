"""A set of pipelines."""
import collections
import typing
import urllib.parse

import requests
import scrapy.exceptions

import stocks.items


ItemsType = typing.Dict[
    stocks.items.CollectionType, typing.List[stocks.items.BaseItem]]


class VerifyPipeline:
    """Pipeline that drops non-valid items."""

    def process_item(self, item, spider):
        """Drop items that have at least one empty field."""
        for value in item.values():
            if value is None:
                raise scrapy.exceptions.DropItem
        return item


class APIPipeline:
    """Pipline that persists crawled items with API."""

    def __init__(self, url: str, token: str):
        """Primary constructor."""
        self._url = url
        self._token = token
        self._items: ItemsType = collections.defaultdict(list)

    @classmethod
    def from_settings(cls, settings):
        """Secondary constructor."""
        return cls(settings['OPENAPI_URL'], settings['OPENAPI_TOKEN'])

    def close_spider(self, spider):
        """Send crawled items to API."""
        for collection, items in self._items.items():
            payload = [{**item, 'source': spider.name} for item in items]

            url = urllib.parse.urljoin(self._url, f'/crawler/{collection}')
            headers = {'Authorization': f'Bearer {self._token}'}

            requests.post(url, json=payload, headers=headers)

    def process_item(self, item, spider):
        """Add crawled item to buffer."""
        self._items[item.collection].append(item)
        return item
