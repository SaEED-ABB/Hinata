# Generated by Django 2.0.4 on 2018-06-14 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0005_auto_20180615_0020'),
    ]

    operations = [
        migrations.AddField(
            model_name='basket',
            name='verify_return_request',
            field=models.NullBooleanField(),
        ),
    ]
