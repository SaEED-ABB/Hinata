# Generated by Django 2.0.4 on 2018-04-26 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0009_auto_20180426_1809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basket',
            name='code',
            field=models.CharField(default='HINATA-YBJWV5', max_length=200, unique=True),
        ),
    ]
