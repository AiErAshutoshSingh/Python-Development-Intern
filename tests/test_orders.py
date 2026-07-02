import pytest
from unittest.mock import patch, MagicMock
from bot.orders import place_order
from bot.exceptions import OrderExecutionError

@patch('bot.orders.get_client')
def test_place_order_market(mock_get_client):
    mock_client = MagicMock()
    mock_client.futures_create_order.return_value = {"orderId": 12345, "status": "NEW"}
    mock_get_client.return_value = mock_client
    
    response = place_order(
        symbol="BTCUSDT",
        side="BUY",
        order_type="MARKET",
        quantity=0.001
    )
    
    assert response["orderId"] == 12345
    mock_client.futures_create_order.assert_called_once_with(
        symbol="BTCUSDT",
        side="BUY",
        type="MARKET",
        quantity=0.001
    )

def test_place_order_limit_missing_price():
    with pytest.raises(OrderExecutionError):
        place_order(
            symbol="BTCUSDT",
            side="BUY",
            order_type="LIMIT",
            quantity=0.001
        )
