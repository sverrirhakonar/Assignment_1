# Data Ingestion & Immutable Types

# Read market_data.csv (columns: timestamp, symbol, price) using the built-in csv module.

# Define a frozen dataclass MarketDataPoint with attributes timestamp (datetime), symbol (str), and price (float).

# Parse each row into a MarketDataPoint and collect them in a list.

import csv
from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class MarketDataPoint:
    timestamp: str
    symbol: str
    price: float

def read_csv_to_immutable_list(csv_file_name):
    with open('market_data.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        price_history = []
        for point in reader:
            market_data_point = MarketDataPoint(
                timestamp = datetime.fromisoformat(point["timestamp"]), 
                symbol = point['symbol'], 
                price = float(point['price']))
            price_history.append(market_data_point)
    return price_history
