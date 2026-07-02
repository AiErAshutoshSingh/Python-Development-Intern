class TradingBotException(Exception):
    """Base exception for the trading bot."""
    pass

class ConfigurationError(TradingBotException):
    """Raised when configuration is missing or invalid."""
    pass

class ValidationError(TradingBotException):
    """Raised when user input fails validation."""
    pass

class APIError(TradingBotException):
    """Raised when Binance API returns an error."""
    pass

class OrderExecutionError(TradingBotException):
    """Raised when an order fails to execute."""
    pass
