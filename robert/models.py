class OrderError(Exception): pass
class ExecutionError(Exception): pass

class Order:
    def __init__(self, action, symbol, quantity, price, status):
        self.action = action
        self.symbol = symbol
        self.quantity = quantity
        self.price = price
        self.status = status

    def check_OrderError(self):
        if self.action not in (-1, 0, 1):
            raise OrderError("Invalid action. Use -1 for SELL , 0 for HOLD, and 1 for BUY.")

        if self.action == 0:
            if self.quantity != 0:
                raise OrderError("HOLD orders must have quantity == 0.")
            return

        if self.quantity <= 0:
            raise OrderError("Invalid quantity, must be positive for BUY or SELL.")
        if self.price <= 0:
            raise OrderError("Invalid price, must be positive for BUY or SELL.")



    
    

    