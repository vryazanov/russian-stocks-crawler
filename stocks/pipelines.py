"""A set of pipelines."""
import collections
import typing
import urllib.parse

import requests
import scrapy.exceptions

import stocks.items


ItemsType = typing.Dict[str, typing.List[stocks.items.BaseItem]]


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

    def __init__(self, base_url: str):
        """Primary constructor."""
        self._base_url = base_url
        self._items: ItemsType = collections.defaultdict(list)

    @classmethod
    def from_settings(cls, settings):
        """Secondary constructor."""
        return cls(settings['BASE_API_URL'])

    def close_spider(self, spider):
        """Send crawled items to API."""
        for collection, items in self._items.items():
            url = urllib.parse.urljoin(self._base_url, collection)
            r = requests.post(
                url, json={'items': [dict(item) for item in items]})
            print(r.content)

    def process_item(self, item, spider):
        """Add crawled item to buffer."""
        self._items[item.collection].append(item)
        return item
