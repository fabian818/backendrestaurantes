from django.db import models


class DateTable(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True


class MetaDataTable(DateTable):
    name = models.CharField(max_length=25)
    display_name = models.CharField(max_length=25)
    description = models.CharField(max_length=200)

    class Meta:
        abstract = True


class FoodStatus(MetaDataTable):
    pass


class FoodCategory(MetaDataTable):
    pass


class TableStatus(MetaDataTable):
    pass


class OrderStatus(MetaDataTable):
    pass


class SaleStatus(MetaDataTable):
    pass


class Food(DateTable):
    food_status = models.ForeignKey(FoodStatus, on_delete=models.DO_NOTHING, null=False)
    food_category = models.ForeignKey(FoodCategory, on_delete=models.DO_NOTHING, null=False)
    name = models.CharField(max_length=100, null=False)
    price = models.DecimalField(max_digits=5, decimal_places=2, null=False)
    image_pic = models.ImageField(default="/static/img/ajidegallina.jpg")


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
    sale_status = models.ForeignKey(SaleStatus, on_delete=models.DO_NOTHING, null=False)
    code = models.CharField(max_length=20, null=False)
    total = models.DecimalField(max_digits=8, decimal_places=2, null=False)
    payment = models.DecimalField(max_digits=8, decimal_places=2, null=False)
    change = models.DecimalField(max_digits=8, decimal_places=2, null=False)


class FoodOrder(DateTable):
    order_status = models.ForeignKey(OrderStatus, on_delete=models.DO_NOTHING, null=False)
    food = models.ForeignKey(Food, on_delete=models.DO_NOTHING, null=False)
    food_table = models.ForeignKey(FoodTable, on_delete=models.DO_NOTHING, null=False, related_name='food_orders')
    sale = models.ForeignKey(Sale, on_delete=models.DO_NOTHING, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=False, default=0)
    total = models.DecimalField(max_digits=8, decimal_places=2, null=False, default=0)
    quantity = models.IntegerField(null=False, default=1)
