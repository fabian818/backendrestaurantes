#/bin/bash

python manage.py loaddata fixtures/fake_data/food.yaml
python manage.py loaddata fixtures/fake_data/food_table.yaml
python manage.py loaddata fixtures/fake_data/food_order.yaml
python manage.py shell < seed.py