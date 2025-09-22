from data_loader import read_market_data
from strategies import MomentumStrategy
from strategies import MovingAverageCrossOver
from models import Order, OrderError, ExecutionError
from engine import TradingEngine
from reporting import calculate_total_return
import random

filename = 'sverrir/market_data.csv'
CASH = 100000

def generate_orders(tick, strategies):
    orders_per_tick = []
    for strategy in strategies:
        orders = strategy.generate_signals(tick)
        orders_per_tick.extend(orders)
    return orders_per_tick


if __name__ == '__main__':
    market_data_ticks = read_market_data(filename)
    portfolio = {}

    momentum = MomentumStrategy(window = 15)
    crossover = MovingAverageCrossOver(short_window=10, long_window=30)
    strategies = [momentum, crossover]

    trade_engine = TradingEngine(strategies, portfolio, CASH)
    trade_engine.run(market_data_ticks)

    print(calculate_total_return(trade_engine.equity_curve))


            




















