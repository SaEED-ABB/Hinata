# Generated by Django 2.0.4 on 2018-05-28 14:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productimage',
            name='slug',
        ),
    ]
