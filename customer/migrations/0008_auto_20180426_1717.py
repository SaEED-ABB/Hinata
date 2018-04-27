# Generated by Django 2.0.4 on 2018-04-26 17:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0007_auto_20180426_1635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basket',
            name='code',
            field=models.CharField(default='HINATA-QA7E3M', max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='selectedproduct',
            name='basket',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='selected_products', to='customer.Basket'),
        ),
    ]
