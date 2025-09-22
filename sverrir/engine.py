import random
from strategies import MomemtumStrategy
from strategies import MovingAverageCrossOver
from models import Order, OrderError, ExecutionError

class TradingEngine:
    def __init__(self, strategies, portfolio = {}, cash = 10000):
        self.strategies = strategies
        self.portfolio = portfolio 
        self.cash = cash
        self.equity_curve = []
    
    def generate_orders(self, tick):
        orders_per_tick = []
        for strategy in self.strategies:
            orders = strategy.generate_signals(tick)
            orders_per_tick.extend(orders)
        return orders_per_tick
    

    def run(self, ticks):
        for tick in ticks:
            orders_per_tick = self.generate_orders(tick)
            for order in orders_per_tick:
                action = order[0]
                symbol = order[1]
                quantity = order[2]
                price = order[3]

                if quantity <= 0:
                    raise OrderError()
                
                try:
                    if random.random() < 0.05:
                        raise ExecutionError("some random failure")
                    

                    if action == 'BUY':
                        if symbol not in self.portfolio:
                            self.portfolio[symbol] = {'quantity' : quantity, 'avg_price' : price}
                        else:
                            if self.cash >= quantity * price:
                                prev_avg = self.portfolio[symbol]['avg_price']
                                prev_qty = self.portfolio[symbol]['quantity']
                                new_quantity = prev_qty + quantity
                                self.portfolio[symbol]['avg_price'] = (prev_avg * prev_qty + quantity * price) / (new_quantity)
                                self.portfolio[symbol]['quantity'] = new_quantity
                                self.cash -= quantity * price
                            else:
                                print(f"WARNING, don't have enough cash")
                    elif action == 'SELL':
                        
                        if symbol in self.portfolio:
                            quantity_owned = self.portfolio[symbol]['quantity']
                            
                            if quantity <= quantity_owned:
                                self.portfolio[symbol]['quantity'] -= quantity
                                self.cash += quantity * price
                                if self.portfolio[symbol]['quantity'] == 0:
                                    del self.portfolio[symbol]
                                else:
                                    print(f"WARNING: Tried to sell {quantity} {symbol} but only own {quantity_owned}.")
                            else:
                                print(f"WARNING: Tried to sell {symbol} but have no position.")        
                except ExecutionError as e:
                    print("Execution error")
            equity_value = 0
            for symbol, position in self.portfolio.items():
                equity_value += position['quantity'] * price
            total_value = self.cash + equity_value
            self.equity_curve.append(total_value)
