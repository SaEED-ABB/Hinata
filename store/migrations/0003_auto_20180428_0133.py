# Generated by Django 2.0.4 on 2018-04-27 21:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_auto_20180426_1635'),
    ]

    operations = [
        migrations.RenameField(
            model_name='producttags',
            old_name='tag',
            new_name='tag_name',
        ),
    ]
