# Generated by Django 2.0.3 on 2018-04-13 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_productimage'),
        ('customer', '0010_auto_20180413_0959'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SelectedProdect',
            new_name='SelectedProduct',
        ),
        migrations.AlterField(
            model_name='basket',
            name='code',
            field=models.CharField(default='HINATA-DWP6UU', max_length=200, unique=True),
        ),
    ]