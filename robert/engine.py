from fsspec.caching import P
from data_loader import read_csv_to_immutable_list
from strategies import MovingAverageStrategy
from strategies import MovingAverageCrossoverStrategy
from models import Order
from models import OrderError
from models import ExecutionError
import pandas as pd



class ExecutionEngine:
    # 1. Bua til signal fyrir hvert tick
    # 2. Tekka hvort signal se i lagi i order, ef ja tha er that order
    # 3. ef order i lagi tha baeta vid portfolio
    # 4. halda uti hversu mikid equity er virdi i portfolio
    def __init__(self, cash, strat_names, price_history, windows):
        self._cash = cash
        self._strat_names = strat_names
        self._price_history = price_history
        self._windows = windows
        self._portfolio = {}
        self._last_price = {}
        self._equity_curve = []  

    
    def execute_strategies(self):
        # Check what strategies we want to run.
        if 'MovingAverageStrategy' in self._strat_names:
            bool_strat_1 = True
            strat_1 = MovingAverageStrategy(self._windows['MovingAverageStrategy'])
        else:
            bool_strat_1 = False
        if 'MovingAverageCrossoverStrategy' in self._strat_names:
            bool_strat_2 = True
            strat_2 = MovingAverageCrossoverStrategy(self._windows['MovingAverageCrossoverStrategy'][0],
            self._windows['MovingAverageCrossoverStrategy'][1] )
        else:
            bool_strat_2 = False

        # For each tick we get signal, instantiate and validate Order objects, 
        # execute orders by updating the portfolio dictionary and keep track of portfolio value.
        for tick in self._price_history:
            if bool_strat_1:
                signals_strat_1 = strat_1.generate_signals(tick)
                action, symbol, qty, price, status = signals_strat_1[-1]
                order = Order(action, symbol, qty, price, status)
                try:
                    order.check_OrderError()
                    self.execute_order(order)
                except OrderError:
                    order.status = 'REJECTED' # Use same language as BBG EMSX.
                except ExecutionError:
                    order.status = 'CANCEL'

            if bool_strat_2:
                signals_strat_2 = strat_2.generate_signals(tick)
                action, symbol, qty, price, status = signals_strat_2[-1]
                order = Order(action, symbol, qty, price, status)
                try:
                    order.check_OrderError()
                    self.execute_order(order)
                except OrderError:
                    order.status = 'REJECTED' # Use same language as BBG EMSX.
                except ExecutionError:
                    order.status = 'CANCEL'

            # Calculate equity value and append to equity curve
            self._last_price[tick.symbol] = tick.price
            portfolio_value = 0
            if self._portfolio:
                for symbol in self._portfolio.keys():
                    portfolio_value += self._portfolio[symbol]['quantity']*self._last_price[symbol]
            equity_value = self._cash + portfolio_value
            self._equity_curve.append((tick.timestamp, equity_value))

    def execute_order(self, order):

        if order.action == 0: # If hold then always OK.
            return 
        amount = order.quantity*order.price
        if order.action == 1: # is there enough cash?
            if amount > self._cash:
                raise ExecutionError("Cash balance will become negative.")
            else:
                self._cash += -amount
                if order.symbol in self._portfolio:
                    old_avg_price = self._portfolio[order.symbol]['avg_price']
                    old_quantity = self._portfolio[order.symbol]['quantity']
                    new_quantity = old_quantity + order.quantity
                    self._portfolio[order.symbol]['avg_price'] = (old_avg_price*old_quantity+amount)/new_quantity
                    self._portfolio[order.symbol]['quantity'] = new_quantity
                else:
                    self._portfolio[order.symbol] = {'quantity': order.quantity, 'avg_price': order.price}
        elif order.action == -1:
            if order.symbol not in self._portfolio or order.quantity > self._portfolio[order.symbol]['quantity']:
                raise ExecutionError("Position will become short.")
            else:
                self._cash += amount
                old_avg_price = self._portfolio[order.symbol]['avg_price']
                old_quantity = self._portfolio[order.symbol]['quantity']
                new_quantity = old_quantity - order.quantity
                self._portfolio[order.symbol]['quantity'] = new_quantity
                if new_quantity == 0:
                    self._portfolio[order.symbol]['avg_price'] = 0.0
                else:
                    self._portfolio[order.symbol]['avg_price'] = old_avg_price
        
