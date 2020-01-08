#/bin/bash

python manage.py loaddata fixtures/food_status.yaml
python manage.py loaddata fixtures/food_category.yaml
python manage.py loaddata fixtures/order_status.yaml
python manage.py loaddata fixtures/sale_status.yaml
python manage.py loaddata fixtures/table_status.yaml