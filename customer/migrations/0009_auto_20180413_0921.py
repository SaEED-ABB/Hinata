# Generated by Django 2.0.3 on 2018-04-13 09:21

import customer.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0008_auto_20180413_0854'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('image', models.ImageField(upload_to=customer.models.get_path)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='basket',
            name='code',
            field=models.CharField(default='HINATA-OBCXBT', max_length=200, unique=True),
        ),
    ]