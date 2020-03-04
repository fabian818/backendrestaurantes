from api.tests.factories.base import SaleFactory
from random import choice

SALE_STATUSES = [1, 2, 3]

for _ in range(200):
    SaleFactory(sale_status_id=choice(SALE_STATUSES))
