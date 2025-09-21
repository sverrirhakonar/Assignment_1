from data_loader import read_market_data
from strategies import MomemtumStrategy
from strategies import MovingAverageCrossOver

filename = 'market_data.csv'

def generate_orders(tick, strategies):
    orders_per_tick = []
    for strategy in strategies:
        orders = strategy.generate_signals(tick)
        orders_per_tick.extend(orders)
    return orders_per_tick


if __name__ == '__main__':
    market_data_ticks = read_market_data(filename)
    portfolio = {}
    momentum = MomemtumStrategy(window = 15)
    crossover = MovingAverageCrossOver(short_window=10, long_window=30)
    strategies = [momentum, crossover]

    for tick in market_data_ticks:
        orders_per_tick = generate_orders(tick, strategies)
        print(orders_per_tick)


















