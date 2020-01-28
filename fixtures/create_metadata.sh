#/bin/bash

python manage.py loaddata fixtures/meta_data/food_status.yaml
python manage.py loaddata fixtures/meta_data/food_category.yaml
python manage.py loaddata fixtures/meta_data/order_status.yaml
python manage.py loaddata fixtures/meta_data/sale_status.yaml
python manage.py loaddata fixtures/meta_data/sale_type.yaml
python manage.py loaddata fixtures/meta_data/table_status.yaml