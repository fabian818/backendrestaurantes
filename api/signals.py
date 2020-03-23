from django.db.models.signals import pre_save
from django.dispatch import receiver
from api.models import FoodOrder, Sale
from api.meta_data import SaleStatusID, OrderStatusID


@receiver(pre_save, sender=FoodOrder, dispatch_uid='modified_food_order')
def modified_food_order(sender, instance, **kwargs):
    food = instance.food
    instance.price = food.price
    instance.total = food.price * instance.quantity

@receiver(pre_save, sender=Sale, dispatch_uid='modified_sale')
def modified_sale(sender, instance, **kwargs):
    if instance.sale_status_id == SaleStatusID.PAID:
        FoodOrder.objects.filter(sale_id=instance.id).update(order_status_id=OrderStatusID.PAID)
    instance.change = instance.payment - instance.total
