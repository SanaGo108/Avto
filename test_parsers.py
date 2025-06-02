import pytest
from parsers.avito_parser import parse_avito
from parsers.auto_ru_parser import parse_auto_ru
from parsers.drom_parser import parse_drom

def test_parse_avito():
    make = "BMW"
    model = "X5"
    prices = parse_avito(make, model)
    assert isinstance(prices, list)
    assert all(isinstance(price, int) for price in prices)

def test_parse_auto_ru():
    make = "BMW"
    model = "X5"
    prices = parse_auto_ru(make, model)
    assert isinstance(prices, list)
    assert all(isinstance(price, int) for price in prices)

def test_parse_drom():
    make = "BMW"
    model = "X5"
    prices = parse_drom(make, model)
    assert isinstance(prices, list)
    assert all(isinstance(price, int) for price in prices)
