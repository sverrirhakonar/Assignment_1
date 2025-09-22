import unittest
from data_loader import MarketDataPoint
from models import Order
from dataclasses import FrozenInstanceError

class TestMutable(unittest.TestCase):
    """ Unit test that tests if Order.status can be changed
    and if MarketDataPoint.price can not be changed.
    """

    def test_order_status_mutable(self):
        order = Order('META', 100, 175.82, 'Routed')
        order.status = "Pending"
        self.assertEqual(order.status, "Pending", 'Error, the order status is not mutable')
    
    def test_order_status(self):
        data_point = MarketDataPoint('2025-09-18 12:31:55.737366','WM', 216.78 )
        with self.assertRaises(FrozenInstanceError, msg = 'Error, expected FrozenInstanceError when modifying price'):
            data_point.price = 200

if __name__ == '__main__':
    unittest.main()
