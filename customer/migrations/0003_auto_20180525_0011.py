# Generated by Django 2.0.4 on 2018-05-24 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_auto_20180525_0005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='session_id',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
