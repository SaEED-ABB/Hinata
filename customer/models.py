import os

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.crypto import get_random_string


def get_path(instance, filename):
    name = get_random_string(length=24) + "." + filename.split('.')[-1]
    return "images/" + name


class BaseData(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        abstract = True


class User(AbstractUser):
    AC_TYPE = (
        ('user', 'Normal User'),
        ('admin', 'Admin User')
    )
    national_code = models.CharField(max_length=200, blank=True, null=True)
    phone_number = models.CharField(max_length=200, blank=True, null=True)
    account_type = models.CharField(max_length=200, blank=True, null=True, choices=AC_TYPE)

    def __str__(self):
        return str(self.national_code)


class UserAddress(BaseData):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.TextField()
    phone_number = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return "{} - {}".format(self.user.username, self.address)


class Basket(BaseData):
    STATUS = (
        ('in_progress', 'In Progress'),
        ('in_way', 'In Way'),
        ('deliverd', 'Deliverd')
    )

    PAYMENT_TYPE = (
        ('paid_with_cashe', 'Paid With Cashe'),
        ('paid_with_epay', 'Paid With EPay')
    )

    code = models.CharField(max_length=200, unique=True, default=("HINATA-{}".format(get_random_string(6))).upper())
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.DO_NOTHING)
    phone_number = models.CharField(max_length=200, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    status = models.CharField(choices=STATUS, default='in_progress', max_length=200, blank=True, null=True)
    payment_type = models.CharField(choices=PAYMENT_TYPE, max_length=200, blank=True, null=True)

    def __str__(self):
        return self.user.get_full_name()


class SelectedProduct(BaseData):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE)
    product = models.ForeignKey('store.product', on_delete=models.DO_NOTHING)
    size = models.ForeignKey('store.size', on_delete=models.DO_NOTHING)
    color = models.ForeignKey('store.color', on_delete=models.DO_NOTHING)
    count = models.IntegerField(blank=True, null=True, default=1)
    price = models.CharField(max_length=200, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.price = self.count * int(self.product.price)
        return super(SelectedProduct, self).save(*args, **kwargs)
    
    def update(self, *args, **kwargs):
        self.price = self.count * int(self.price)
        return super(SelectedProduct, self).update(*args, **kwargs)

    def __str__(self):
        return self.basket.code


class Comment(BaseData):
    product = models.ForeignKey('store.product', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    is_approved = models.NullBooleanField()

    def __str__(self):
        return "{}-{}".format(self.product.name, self.user.username)


class Image(BaseData):
    image = models.ImageField(upload_to=get_path)

    def delete(self, *args, **kwargs):
        os.remove(self.image.path)
        return super(Image, self).delete(*args, **kwargs)

    def __str__(self):
        return self.image.name


class Favorite(BaseData):
    product = models.ForeignKey('store.product', on_delete=models.CASCADE)
    user = models.ForeignKey('customer.user', on_delete=models.CASCADE)

    def __str__(self):
        return "{} - {}".format(self.user.username, self.product.name)
