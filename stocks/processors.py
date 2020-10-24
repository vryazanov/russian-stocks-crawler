"""Scrapy spider that can parse smart-lab.ru website."""
import datetime
import typing


def is_forecast(value: str) -> bool:
    """Check it is a forecast or not.

    All forecasts contain a special cyrillic symbol or word.
    >>> is_forecast('0,65 П')
    True
    >>> is_forecast('0,65')
    False
    >>> is_forecast('0.89 (прогноз)')
    True
    """
    value = value.lower()

    if 'прогноз' in value:
        return True

    return 'п' in value.split()


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


def extract_date(value: str) -> typing.Optional[datetime.date]:
    """Extract date from value, return None if there is no date.

    >>> extract_date('18.07.2020 П')
    datetime.date(2020, 7, 18)
    >>> extract_date('20.12.2020 (прогноз)')
    datetime.date(2020, 12, 20)
    """
    value = value.lower().strip()
    value = value.replace('п', '').replace('прогноз', '').replace(',', '.')

    for chunk in value.split():
        try:
            dt_value = datetime.datetime.strptime(chunk, '%d.%m.%Y')
        except ValueError:
            continue
        else:
            return dt_value.date()

    return None
