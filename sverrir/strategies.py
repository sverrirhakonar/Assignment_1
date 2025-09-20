from abc import ABC, abstractmethod
from models import MarketDataPoint

class Strategy(ABC):
    @abstractmethod
    def generate_signals(self, tick: MarketDataPoint) -> list:
        pass

class MomemtumStrategy(Strategy):
    def __init__(self, window = 5):
        self._window = window
        self._prices = []
    
    def generate_signals(self, tick:MarketDataPoint ) -> list: 
        signals = []
        self._prices.append(tick.price)
        if len(self._prices) > self._window:
            self._prices.pop(0)
        
        if len(self._prices) == self._window:
            current_price = tick.price
            past_price = self._prices[0]

            if current_price > past_price:
                signal = ('BUY', tick.symbol, 1, tick.price)
                signals.append(signal)
            elif current_price < past_price:
                signal = ('SELL', tick.symbol, 1, tick.price)
                signals.append(signal)
        return signals

class MovingAverageCrossOver(Strategy):
    
    def __init__(self, short_window = 10, long_window = 20):
        self._short_window = short_window
        self._long_window = long_window
        self._prices = []

    def generate_signals(self, tick: MarketDataPoint) -> list:
        signals = []
        self._prices.append(tick.price)
        if len(self._prices) > self._long_window:
            self._prices.pop(0)
        
        if len(self._prices) == self._long_window:
            slow_average = sum(self._prices) / self._long_window
            fast_average = sum(self._prices[-self._short_window:]) / self._short_window

            if fast_average > slow_average:
                signal = ('BUY', tick.symbol, 1, tick.price)
                signals.append(signal)
            elif fast_average < slow_average:
                signal = ('SELL', tick.symbol, 1, tick.price)
                signals.append(signal)
        return signals



        




        
