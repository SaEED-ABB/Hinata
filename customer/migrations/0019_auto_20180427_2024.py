# Generated by Django 2.0.4 on 2018-04-27 20:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0018_auto_20180427_2023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basket',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='baskets', to=settings.AUTH_USER_MODEL),
        ),
    ]
