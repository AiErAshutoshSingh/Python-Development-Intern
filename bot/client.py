from binance.client import Client
from .config import settings
from .exceptions import ConfigurationError, APIError
from .logger import error_logger

_client_instance = None

def get_client() -> Client:
    """Returns a singleton instance of the Binance Client."""
    global _client_instance
    
    if _client_instance is not None:
        return _client_instance

    api_key = settings.api_key.get_secret_value()
    api_secret = settings.api_secret.get_secret_value()

    if not api_key or not api_secret:
        error_logger.error("API keys are missing in the configuration.")
        raise ConfigurationError("BINANCE_API_KEY and BINANCE_API_SECRET must be set.")

    try:
        # testnet=True handles both spot testnet and futures testnet implicitly
        # when calling client.futures_* endpoints.
        _client_instance = Client(api_key, api_secret, testnet=settings.testnet)
        return _client_instance
    except Exception as e:
        error_logger.error(f"Failed to initialize Binance Client: {e}")
        raise APIError(f"Failed to initialize Binance Client: {e}")
