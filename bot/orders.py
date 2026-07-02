import time
from typing import Optional, Dict, Any
from binance.exceptions import BinanceAPIException, BinanceRequestException
from .client import get_client
from .validators import validate_symbol, validate_side, validate_quantity, validate_order_type, validate_price
from .logger import market_logger, limit_logger, error_logger
from .exceptions import APIError, OrderExecutionError

def place_order(
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: Optional[float] = None,
    stop_price: Optional[float] = None
) -> Dict[str, Any]:
    """
    Places a futures order on Binance.
    """
    symbol = validate_symbol(symbol)
    side = validate_side(side)
    order_type = validate_order_type(order_type)
    quantity = validate_quantity(quantity)
    
    if order_type in ["LIMIT", "STOP", "TAKE_PROFIT"]:
        if price is None:
            raise OrderExecutionError(f"Price is required for {order_type} orders.")
        price = validate_price(price)

    if order_type in ["STOP", "TAKE_PROFIT", "STOP_MARKET", "TAKE_PROFIT_MARKET"]:
        if stop_price is None:
            raise OrderExecutionError(f"Stop price is required for {order_type} orders.")
        stop_price = validate_price(stop_price)

    client = get_client()

    params = {
        'symbol': symbol,
        'side': side,
        'type': order_type,
        'quantity': quantity,
    }

    if price is not None:
        params['price'] = price
        params['timeInForce'] = 'GTC'

    if stop_price is not None:
        params['stopPrice'] = stop_price

    start_time = time.time()
    try:
        response = client.futures_create_order(**params)
        execution_time = time.time() - start_time
        
        log_data = {
            'request': params,
            'response': response,
            'execution_time': f"{execution_time:.3f}s",
            'status': response.get('status', 'UNKNOWN')
        }
        
        if order_type == 'MARKET':
            market_logger.info(f"Order Success: {log_data}")
        else:
            limit_logger.info(f"Order Success: {log_data}")
            
        return response

    except BinanceAPIException as e:
        error_logger.error(f"Binance API Error: {e.status_code} - {e.message} | Request: {params}")
        raise APIError(f"Binance API Error: {e.message}")
    except BinanceRequestException as e:
        error_logger.error(f"Binance Request Error: {e} | Request: {params}")
        raise APIError(f"Binance Request Error: {e}")
    except Exception as e:
        error_logger.error(f"Unexpected Error: {e} | Request: {params}")
        raise OrderExecutionError(f"Unexpected Error: {e}")
