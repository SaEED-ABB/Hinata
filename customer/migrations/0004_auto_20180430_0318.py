# Generated by Django 2.0.4 on 2018-04-29 22:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0003_auto_20180429_2300'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='basket',
            options={'ordering': ('-created_at',)},
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ('-created_at',)},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ('-created_at',), 'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
    ]