# Generated by Django 2.2.9 on 2020-02-02 23:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_sale_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='sale_status',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='api.SaleStatus'),
        ),
    ]
