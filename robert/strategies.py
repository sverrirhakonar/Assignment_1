from abc import ABC, abstractmethod
from statistics import mean
from data_loader import MarketDataPoint

class Strategy(ABC):
    @abstractmethod
    def generate_signals(self, tick: MarketDataPoint) -> list:
        pass

class MovingAverageStrategy(Strategy):
    """Long only moving average strategy, returns action 
    (0 = HOLD, 1 = BUY and -1 = SELL) at every timepoint.
    
    Strategy goes long if stock price crosses over rolling average
    of the stock price.
    """
    def __init__(self, window):
        self._window = window
        self._prices = []
        self._signals = []
        self._tick_buffer = [] 
    def generate_signals(self, tick: MarketDataPoint) -> list:
        self._tick_buffer.append(tick) # Add each tick to a buffer (que) so we process ticks in right order.
        first_tick_in_line = self._tick_buffer[0]
        if len(self._signals) == 0:
            last_signal = 0
        else:
            last_signal = self._signals[-1]
        if len(self._prices) < self._window:
            self._signals.append((0, first_tick_in_line.symbol, 
            50, first_tick_in_line.price, "ROUTE"))
        elif len(self._prices) == self._window:
                avg_price = mean(self._prices)
                if avg_price < first_tick_in_line.price:
                    if last_signal == 1:
                        self._signals.append((0, first_tick_in_line.symbol, 
                        50, first_tick_in_line.price, "ROUTE"))
                    else:
                        self._signals.append((1, first_tick_in_line.symbol, 
                        50, first_tick_in_line.price, "ROUTE"))

                elif avg_price > first_tick_in_line.price:
                    if last_signal == 1:
                        self._signals.append((-1, first_tick_in_line.symbol, 
                        50, first_tick_in_line.price, "ROUTE"))
                    else:
                        self._signals.append((0, first_tick_in_line.symbol, 
                        50, first_tick_in_line.price, "ROUTE"))
                else:
                    self._signals.append((0, first_tick_in_line.symbol, 
                    50, first_tick_in_line.price, "ROUTE"))

        self._prices.append(first_tick_in_line.price)
        self._tick_buffer.pop(0) # Remove the tick we used from the buffer.
        if len(self._prices) > self._window:
            self._prices.pop(0)
        return self._signals


class MovingAverageCrossoverStrategy(Strategy):
    """Long only moving average crossover strategy, returns action 
    (0 = HOLD, 1 = BUY and -1 = SELL) at every timepoint.
    
    Strategy goes long if short term rolling average crosses 
    over long term rolling average of the stock price.
    """
    def __init__(self, window_short, window_long):
        self._window_short = window_short
        self._window_long = window_long
        self._prices = []
        self._signals = []
        self._tick_buffer = []
        # If short < long: SELL
        # If short > long> Buy
    def generate_signals(self, tick: MarketDataPoint) -> list:
        self._tick_buffer.append(tick) # Add each tick to a buffer (que) so we process ticks in right order.
        first_tick_in_line = self._tick_buffer[0]
        
        if len(self._signals) == 0:
            last_signal = 0
        else:
            last_signal = self._signals[-1]

        if len(self._prices) < self._window_long:
            self._signals.append((0, first_tick_in_line.symbol, 
            50, first_tick_in_line.price, "ROUTE"))
        elif len(self._prices) == self._window_long:
                avg_price_short = mean(self._prices[:self._window_short])
                avg_price_long = mean(self._prices[:self._window_long])
                if avg_price_short > avg_price_long:
                    if last_signal == 1:
                        self._signals.append((0, first_tick_in_line.symbol, 
                        50, first_tick_in_line.price, "ROUTE"))
                    else:
                        self._signals.append((1, first_tick_in_line.symbol, 
                        50, first_tick_in_line.price, "ROUTE"))
                elif avg_price_short < avg_price_long:
                    if last_signal == 1:
                        self._signals.append((-1, first_tick_in_line.symbol, 
                        50, first_tick_in_line.price, "ROUTE"))
                    else:
                        self._signals.append((0, first_tick_in_line.symbol, 
                        50, first_tick_in_line.price, "ROUTE"))
                else:
                    self._signals.append((0, first_tick_in_line.symbol, 
                    50, first_tick_in_line.price, "ROUTE"))

        self._prices.append(first_tick_in_line.price)
        self._tick_buffer.pop(0)
        if len(self._prices) > self._window_long:
            self._prices.pop(0)
        return self._signals

        