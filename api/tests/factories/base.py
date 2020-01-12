import factory
import random
from faker import Faker
from api.models import Food, FoodTable, FoodOrder, Sale, Client


fake = Faker()


class FoodFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Food

    food_status_id = 1
    food_category_id = 1
    name = factory.Faker('credit_card_provider')
    price = random.randint(100, 200)


class FoodTableFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FoodTable

    table_status_id = 1
    identifier = 'mesa x'
    display_name = factory.Faker('credit_card_provider')
    description = factory.Faker('credit_card_number')


class ClientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Client

    identifier = str(random.randint(11111111, 99999999))
    name = factory.Faker('credit_card_provider')
    last_name = factory.Faker('credit_card_provider')


class SaleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Sale

    client = factory.SubFactory(ClientFactory)
    sale_status_id = 1
    code = str(random.randint(100, 200))
    total = random.randint(100, 200)
    payment = random.randint(100, 200)
    change = random.randint(100, 200)


class FoodOrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FoodOrder

    order_status_id = 1
    food = factory.SubFactory(FoodFactory)
    food_table = factory.SubFactory(FoodTableFactory)
    sale_id = factory.SubFactory(SaleFactory)
    price = random.randint(100, 200)
    total = random.randint(100, 200)
    quantity = random.randint(100, 200)