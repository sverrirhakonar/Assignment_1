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



        
