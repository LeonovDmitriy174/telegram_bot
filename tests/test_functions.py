import datetime
from src.functions import get_currency_rate

datetime_now = datetime.datetime.now()


def test_get_currency_rate():
    assert get_currency_rate("USD") == 0
