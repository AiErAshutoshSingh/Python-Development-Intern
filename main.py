from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from bot.orders import place_order
from bot.exceptions import TradingBotException
from bot.client import get_client

app = FastAPI(
    title="Binance Futures Trading Bot API",
    description="API for the 3D React Dashboard",
    version="1.0.0"
)

# Enable CORS for the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class OrderRequest(BaseModel):
    symbol: str
    side: str
    order_type: str
    quantity: float
    price: Optional[float] = None
    stop_price: Optional[float] = None

@app.get("/health")
def health_check():
    """Simple health check endpoint."""
    return {"status": "ok", "message": "API is running"}

@app.get("/status")
def connection_status():
    """Check connection to Binance Testnet."""
    try:
        client = get_client()
        client.ping()
        return {"status": "connected", "message": "Successfully connected to Binance Testnet"}
    except Exception as e:
        return {"status": "disconnected", "message": str(e)}

@app.post("/place-order")
def api_place_order(order: OrderRequest):
    """Place a new order."""
    try:
        response = place_order(
            symbol=order.symbol,
            side=order.side,
            order_type=order.order_type,
            quantity=order.quantity,
            price=order.price,
            stop_price=order.stop_price
        )
        return {"success": True, "data": response}
    except TradingBotException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
