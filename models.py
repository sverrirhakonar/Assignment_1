from datetime import datetime
from dataclasses import dataclass

@dataclass(frozen=True)
class MarketDataPoint:
    timestamp: datetime
    symbol: str
    price: float

class Order:
    def __init__(self,symbol, quantity, price, status = 'NEW'):
        self.symbol = symbol
        self.quantity = quantity
        self.price = price
        self.status = status

class OrderError(Exception):
    pass

class ExecutionError(Exception):
    pass

    