# Generated by Django 2.0.3 on 2018-04-13 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_auto_20180412_1940'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='colors',
            field=models.ManyToManyField(related_name='colors', to='store.Color'),
        ),
    ]
