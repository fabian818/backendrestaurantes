from django.db.models.signals import pre_save
from django.dispatch import receiver
from api.models import FoodOrder


@receiver(pre_save, sender=FoodOrder, dispatch_uid='modified_food_order')
def modified_food_order(sender, instance, **kwargs):
    food = instance.food
    instance.price = food.price
    instance.total = food.price * instance.quantity
