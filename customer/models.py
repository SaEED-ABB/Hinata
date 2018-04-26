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
    phone_number = models.CharField(max_length=200, blank=True, null=True)
    account_type = models.CharField(max_length=200, blank=True, null=True, choices=AC_TYPE)
    favorites = models.ManyToManyField('store.Product', related_name='lovers')

    def __str__(self):
        return '{}({})'.format(self.username, self.get_full_name())


class UserAddress(BaseData):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
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
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.DO_NOTHING, related_name='baskets')
    phone_number = models.CharField(max_length=200, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    status = models.CharField(choices=STATUS, default='in_progress', max_length=200, blank=True, null=True)
    payment_type = models.CharField(choices=PAYMENT_TYPE, max_length=200, blank=True, null=True)

    def __str__(self):
        return "{}'s basket({})".format(self.user.username, self.code)


class SelectedProduct(BaseData):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name='selected_products')
    product = models.ForeignKey('store.Product', on_delete=models.DO_NOTHING)
    size = models.ForeignKey('store.Size', on_delete=models.DO_NOTHING, blank=True, null=True)
    color = models.ForeignKey('store.Color', on_delete=models.DO_NOTHING, blank=True, null=True)
    count = models.IntegerField(blank=True, null=True, default=1)
    price = models.CharField(max_length=200, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.price = self.count * int(self.product.price)
        return super(SelectedProduct, self).save(*args, **kwargs)
    
    def update(self, *args, **kwargs):
        self.price = self.count * int(self.price)
        return super(SelectedProduct, self).update(*args, **kwargs)

    def __str__(self):
        return '{} in {}'.format(self.product.name, self.basket)


class Comment(BaseData):
    product = models.ForeignKey('store.Product', on_delete=models.CASCADE, related_name='related_comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    is_approved = models.NullBooleanField()

    def __str__(self):
        return "by {} for {}".format(self.user.username, self.product.name)


class Image(BaseData):
    image = models.ImageField(upload_to=get_path)

    def delete(self, *args, **kwargs):
        os.remove(self.image.path)
        return super(Image, self).delete(*args, **kwargs)

    def __str__(self):
        return self.image.name


# class Favorite(BaseData):
#     product = models.ForeignKey('store.Product', on_delete=models.CASCADE)
#     user = models.ForeignKey('customer.User', on_delete=models.CASCADE, related_name='favorite_products')
#
#     def __str__(self):
#         return "{} likes {}".format(self.user.username, self.product.name)
