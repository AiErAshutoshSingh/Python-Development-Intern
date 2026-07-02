from .exceptions import ValidationError

def validate_symbol(symbol: str) -> str:
    """Validate and sanitize trading symbol."""
    if not symbol:
        raise ValidationError("Symbol cannot be empty.")
    symbol = symbol.strip().upper()
    if not symbol.endswith("USDT"):
        raise ValidationError("Only USDT-M Futures are supported. Symbol must end with USDT.")
    if len(symbol) < 5:
        raise ValidationError(f"Invalid symbol length: {symbol}")
    return symbol

def validate_quantity(quantity: float) -> float:
    """Validate order quantity."""
    try:
        qty = float(quantity)
    except ValueError:
        raise ValidationError("Quantity must be a number.")
        
    if qty <= 0:
        raise ValidationError("Quantity must be strictly positive (greater than zero).")
    return qty

def validate_side(side: str) -> str:
    """Validate order side."""
    if not side:
        raise ValidationError("Side cannot be empty.")
    side = side.strip().upper()
    if side not in ["BUY", "SELL"]:
        raise ValidationError(f"Invalid side '{side}'. Must be 'BUY' or 'SELL'.")
    return side

def validate_order_type(order_type: str) -> str:
    """Validate order type."""
    if not order_type:
        raise ValidationError("Order type cannot be empty.")
    order_type = order_type.strip().upper()
    valid_types = ["MARKET", "LIMIT", "STOP", "STOP_MARKET", "TAKE_PROFIT", "TAKE_PROFIT_MARKET"]
    if order_type not in valid_types:
        raise ValidationError(f"Invalid order type '{order_type}'. Must be one of {valid_types}.")
    return order_type

def validate_price(price: float) -> float:
    """Validate limit price."""
    try:
        prc = float(price)
    except ValueError:
        raise ValidationError("Price must be a number.")
        
    if prc <= 0:
        raise ValidationError("Price must be strictly positive (greater than zero).")
    return prc
