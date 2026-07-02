import datetime

def format_datetime(timestamp_ms: int) -> str:
    """Format milliseconds timestamp to human readable string."""
    dt = datetime.datetime.fromtimestamp(timestamp_ms / 1000.0)
    return dt.strftime('%Y-%m-%d %H:%M:%S')
