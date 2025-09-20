from datetime import datetime
from dataclasses import dataclass

@dataclass(frozen=True)
class MarketDataPoint:
    timestamp: datetime
    symbol: str
    price: float

    