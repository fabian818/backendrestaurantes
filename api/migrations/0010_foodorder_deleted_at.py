# Generated by Django 2.2.9 on 2020-02-07 23:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20200202_2349'),
    ]

    operations = [
        migrations.AddField(
            model_name='foodorder',
            name='deleted_at',
            field=models.DateTimeField(null=True),
        ),
    ]
