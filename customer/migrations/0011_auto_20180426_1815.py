# Generated by Django 2.0.4 on 2018-04-26 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0010_auto_20180426_1809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basket',
            name='code',
            field=models.CharField(default='HINATA-S7MACC', max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='account_type',
            field=models.CharField(blank=True, choices=[('user', 'Normal User'), ('admin', 'Admin User')], max_length=200, null=True),
        ),
    ]