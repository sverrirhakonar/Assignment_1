# Part one
import csv
from datetime import datetime
from models import MarketDataPoint

# timestamp, symbol, price
#sverrir
def read_market_data(filename):
    data_points = []
    with open(filename, mode='r', newline = '') as file:
        reader = csv.DictReader(file)
        for row in reader:
            date = datetime.fromisoformat(row['timestamp'])
            price = float(row['price'])
            data_points.append(MarketDataPoint(date, row['symbol'],price))
    return data_points




