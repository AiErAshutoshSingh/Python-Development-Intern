import pytest
from bot.validators import validate_symbol, validate_quantity, validate_side, validate_order_type, validate_price
from bot.exceptions import ValidationError

def test_validate_symbol():
    assert validate_symbol("BTCUSDT") == "BTCUSDT"
    with pytest.raises(ValidationError):
        validate_symbol("BTCUSD")
    with pytest.raises(ValidationError):
        validate_symbol("BTC")

def test_validate_quantity():
    assert validate_quantity("0.001") == 0.001
    assert validate_quantity(1.5) == 1.5
    with pytest.raises(ValidationError):
        validate_quantity("-1")
    with pytest.raises(ValidationError):
        validate_quantity("0")

def test_validate_side():
    assert validate_side("BUY") == "BUY"
    assert validate_side("sell") == "SELL"
    with pytest.raises(ValidationError):
        validate_side("HOLD")

def test_validate_order_type():
    assert validate_order_type("MARKET") == "MARKET"
    assert validate_order_type("limit") == "LIMIT"
    with pytest.raises(ValidationError):
        validate_order_type("INVALID")

def test_validate_price():
    assert validate_price(50000) == 50000.0
    with pytest.raises(ValidationError):
        validate_price(0)
    with pytest.raises(ValidationError):
        validate_price(-100)
