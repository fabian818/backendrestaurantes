from django.apps import AppConfig


class ApiConfig(AppConfig):
    name = 'api'

    # def ready(self):
    #     pre_save.connect(modified_food_order, sender=FoodOrder,
    #                       dispatch_uid='modified_food_order')
