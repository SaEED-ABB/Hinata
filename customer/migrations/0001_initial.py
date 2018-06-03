# Generated by Django 2.0.4 on 2018-06-02 12:22

import customer.managers
import customer.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import store.helpers.validators
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
        ('store', '0003_productimage_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('phone_number', models.CharField(max_length=200, unique=True)),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('is_active', models.BooleanField(default=True)),
                ('account_type', models.CharField(blank=True, choices=[('user', 'Normal User'), ('admin', 'Admin User'), ('superuser', 'Super User')], default='user', max_length=200, null=True)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to=customer.models.generate_picture_path, validators=[store.helpers.validators.file_size])),
                ('favorites', models.ManyToManyField(blank=True, related_name='lovers', to='store.Product')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'ordering': ('-created_at',),
            },
            managers=[
                ('objects', customer.managers.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Basket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('code', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('phone_number', models.CharField(blank=True, max_length=200, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('status', models.CharField(blank=True, choices=[('closed_canceled', 'Closed -> Canceled'), ('closed_returned', 'Closed -> Returned'), ('closed_delivered', 'Closed -> Delivered'), ('open_checking', 'Open -> Checking'), ('open_preparing', 'Open -> Preparing'), ('open_sending', 'Open -> Sending'), ('open_delivering', 'Open -> Delivering')], default='open_checking', max_length=200, null=True)),
                ('payment_type', models.CharField(blank=True, choices=[('paid_with_cash', 'Paid With Cash'), ('paid_with_e-pay', 'Paid With E-Pay')], max_length=200, null=True)),
                ('total_price', models.IntegerField(default=0)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='baskets', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('comment', models.TextField()),
                ('session_id', models.CharField(blank=True, max_length=200, null=True)),
                ('session_name', models.CharField(blank=True, max_length=200, null=True)),
                ('is_approved', models.NullBooleanField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_comments', to='store.Product')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='ProductRate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('rate', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('session_id', models.CharField(blank=True, max_length=200, null=True)),
                ('session_name', models.CharField(blank=True, max_length=200, null=True)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rates', to='store.Product')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='related_rates', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SelectedProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('count', models.IntegerField(default=0)),
                ('price', models.IntegerField(default=0)),
                ('basket', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='selected_products', to='customer.Basket')),
                ('color', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='store.Color')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='store.Product')),
                ('size', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='store.Size')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('address', models.TextField()),
                ('phone_number', models.CharField(blank=True, max_length=200, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'user addresses',
            },
        ),
    ]
