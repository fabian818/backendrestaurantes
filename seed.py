from api.tests.factories.base import SaleFactory, FoodOrderFactory
from random import choice

SALE_STATUSES = [1, 2, 3]
ORDER_STATUSES = [1, 2, 3]

for _ in range(100):
    SaleFactory(sale_status_id=choice(SALE_STATUSES))
for _ in range(100):
    FoodOrderFactory(order_status_id=choice(ORDER_STATUSES))
