# Generated by Django 2.0.3 on 2018-04-13 06:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_auto_20180413_0638'),
        ('customer', '0002_useraddress'),
    ]

    operations = [
        migrations.CreateModel(
            name='Basket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('code', models.CharField(default='HINATA-lxIaiL', max_length=200, unique=True)),
                ('phone_number', models.CharField(blank=True, max_length=200, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('status', models.CharField(blank=True, choices=[('in_progress', 'In Progress'), ('in_way', 'In Way'), ('deliverd', 'Deliverd')], default='in_progress', max_length=200, null=True)),
                ('payment_type', models.CharField(blank=True, choices=[('paid_with_cashe', 'Paid With Cashe'), ('paid_with_epay', 'Paid With EPay')], max_length=200, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SelectedProdect',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('price', models.CharField(blank=True, max_length=200, null=True)),
                ('basket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.Basket')),
                ('color', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='store.Color')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='store.Product')),
                ('size', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='store.Size')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
