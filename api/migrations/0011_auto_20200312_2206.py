# Generated by Django 2.2.10 on 2020-03-12 22:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_foodorder_deleted_at'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='client',
            options={'ordering': ['created_at']},
        ),
        migrations.AlterModelOptions(
            name='food',
            options={'ordering': ['created_at']},
        ),
        migrations.AlterModelOptions(
            name='foodorder',
            options={'ordering': ['created_at']},
        ),
        migrations.AlterModelOptions(
            name='foodtable',
            options={'ordering': ['created_at']},
        ),
        migrations.AlterModelOptions(
            name='historicalprice',
            options={'ordering': ['created_at']},
        ),
        migrations.AlterModelOptions(
            name='sale',
            options={'ordering': ['-created_at']},
        ),
    ]
