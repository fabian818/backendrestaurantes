from django.db import models
from api.meta_data import OrderStatusID, SaleTypeID, SaleStatusID, FoodStatusID
from django.db.models import Max
from django.db.models.functions import Coalesce
from django.utils import timezone
from slugify import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver


class DateTable(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True
        ordering = ['created_at']


class MetaDataTable(DateTable):
    name = models.CharField(max_length=25)
    display_name = models.CharField(max_length=25)
    description = models.CharField(max_length=200)

    class Meta:
        abstract = True


class FoodStatus(MetaDataTable):
    pass


class FoodCategory(MetaDataTable):
    def save(self, *args, **kwargs):
        self.name = slugify(self.display_name)
        super().save(*args, **kwargs)


class TableStatus(MetaDataTable):
    pass


class OrderStatus(MetaDataTable):
    pass


class SaleStatus(MetaDataTable):
    pass


class SaleType(MetaDataTable):
    pass


class Food(DateTable):
    food_status = models.ForeignKey(FoodStatus,
                                    on_delete=models.DO_NOTHING,
                                    null=False)
    food_category = models.ForeignKey(FoodCategory,
                                      on_delete=models.DO_NOTHING,
                                      null=False)
    name = models.CharField(max_length=100, null=False)
    price = models.DecimalField(max_digits=5, decimal_places=2, null=False)
    image_pic = models.ImageField(default="/static/img/ajidegallina.jpg")
    deleted_at = models.DateTimeField(null=True)

    def delete(self,
               force_insert=False,
               force_update=False,
               using=None,
               update_fields=None):
        self.deleted_at = timezone.now()
        self.food_status_id = FoodStatusID.DELETED
        self.save()


@receiver(post_save,
        sender=Food,
        dispatch_uid="update_historical_price")
def update_historical_price(sender, instance, **kwargs):
    HistoricalPrice.objects.create(price=instance.price, food_id=instance.id)


class HistoricalPrice(DateTable):
    food = models.ForeignKey(Food, on_delete=models.DO_NOTHING, null=False)
    price = models.DecimalField(max_digits=5, decimal_places=2, null=False)


class FoodTable(DateTable):
    table_status = models.ForeignKey(TableStatus, on_delete=models.DO_NOTHING, null=False)
    identifier = models.CharField(max_length=100, null=False)
    display_name = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=200, null=True)


class Client(DateTable):
    identifier = models.CharField(max_length=10, null=False)
    name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)


class Sale(DateTable):
    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING, null=False)
    sale_status = models.ForeignKey(
        SaleStatus, on_delete=models.DO_NOTHING, null=False, default=1)
    sale_type = models.ForeignKey(
        SaleType, on_delete=models.DO_NOTHING, null=False, default=1)
    number = models.IntegerField(null=False, default=1)
    code = models.CharField(max_length=20, null=False)
    total = models.DecimalField(max_digits=8, decimal_places=2, null=False)
    payment = models.DecimalField(max_digits=8, decimal_places=2, null=False)
    change = models.DecimalField(max_digits=8, decimal_places=2, null=False)
    deleted_at = models.DateTimeField(null=True)

    def delete(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.deleted_at = timezone.now()
        self.sale_status_id = SaleStatusID.DELETED
        FoodOrder.objects.filter(sale_id=self.id).update(order_status_id=OrderStatusID.CREATED)
        self.save()

    def save(self,
             force_insert=False,
             force_update=False,
             using=None,
             update_fields=None):
        if self.pk is None:
            sale_types_values = {SaleTypeID.BOLETA: 'B', SaleTypeID.FACTURA: 'F'}
            letter = sale_types_values.get(self.sale_type_id)
            last_number = Sale.objects.all().aggregate(max_number=Coalesce(Max('number'), 0))['max_number']
            self.number = int(last_number) + 1
            number_str = str(self.number).rjust(8, '0')
            self.code = "{}001-{}".format(letter, number_str)
            self.change = self.payment - self.total
        return super(Sale, self).save(force_insert=False,
                                      force_update=False,
                                      using=None,
                                      update_fields=None)

    class Meta:
        ordering = ['-created_at']


class FoodOrder(DateTable):
    order_status = models.ForeignKey(OrderStatus, on_delete=models.DO_NOTHING, null=False, default=OrderStatusID.CREATED)
    food = models.ForeignKey(Food, on_delete=models.DO_NOTHING, null=False)
    food_table = models.ForeignKey(FoodTable, on_delete=models.DO_NOTHING, null=False, related_name='food_orders')
    sale = models.ForeignKey(Sale, on_delete=models.DO_NOTHING, null=True, related_name='food_orders')
    price = models.DecimalField(max_digits=8, decimal_places=2, null=False, default=0)
    total = models.DecimalField(max_digits=8, decimal_places=2, null=False, default=0)
    quantity = models.IntegerField(null=False, default=1)
    deleted_at = models.DateTimeField(null=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.total = self.quantity * self.price
        return super(FoodOrder, self).save(force_insert=False, force_update=False, using=None,
                                        update_fields=None)

    def delete(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.deleted_at = timezone.now()
        self.order_status_id = OrderStatusID.DELETED
        self.save()
