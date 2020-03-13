from django.apps import AppConfig
# from django.db.models.signals import pre_save
# from api.signals import modified_food_order
# from api.models import FoodOrder


class ApiConfig(AppConfig):
    name = 'api'

    def ready(self):
        # pre_save.connect(modified_food_order, sender=FoodOrder,
        #                   dispatch_uid='modified_food_order')
        import api.signals
