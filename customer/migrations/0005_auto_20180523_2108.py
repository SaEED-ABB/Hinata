# Generated by Django 2.0.4 on 2018-05-23 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0004_auto_20180430_0318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basket',
            name='total_price',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='selectedproduct',
            name='count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='selectedproduct',
            name='price',
            field=models.IntegerField(default=0),
        ),
    ]
