from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _

import uuid as uuid_lib

from .managers import UserManager
from frontview.models import TimeStampedModel


class User(AbstractBaseUser, TimeStampedModel):
    AC_TYPE = (
        ('user', 'Normal User'),
        ('admin', 'Admin User')
    )
    phone_number = models.CharField(max_length=200, unique=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    account_type = models.CharField(max_length=200, blank=True, null=True, choices=AC_TYPE, default='user')
    favorites = models.ManyToManyField('store.Product', related_name='lovers', blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.account_type == 'admin'

    def __str__(self):
        return '{}({})'.format(self.phone_number, self.get_full_name())


class UserAddress(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    address = models.TextField()
    phone_number = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return "{} - {}".format(self.user.get_full_name(), self.address)


class Basket(TimeStampedModel):
    OPEN_CHECKING = 'open_checking'

    STATUS = (
        ('closed_canceled', 'Closed -> Canceled'),
        ('closed_returned', 'Closed -> Returned'),
        ('closed_delivered', 'Closed -> Delivered'),

        (OPEN_CHECKING, 'Open -> Checking'),
        ('open_preparing', 'Open -> Preparing'),
        ('open_sending', 'Open -> Sending'),
        ('open_delivering', 'Open -> Delivering')
    )

    PAYMENT_TYPE = (
        ('paid_with_cash', 'Paid With Cash'),
        ('paid_with_e-pay', 'Paid With E-Pay')
    )

    code = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='baskets')
    phone_number = models.CharField(max_length=200, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    status = models.CharField(choices=STATUS, default='open_checking', max_length=200, blank=True, null=True)
    payment_type = models.CharField(choices=PAYMENT_TYPE, max_length=200, blank=True, null=True)
    total_price = models.IntegerField(null=True)

    def get_info(self, all_colors_and_sizes_per_product=False):

        context = {
            "total_price": self.total_price,
            "status": self.status,
            "products": [],
        }

        for sel_pro in self.selected_products.all():
            desired_color = sel_pro.color
            desired_size = sel_pro.size

            colors = []
            sizes = []

            if all_colors_and_sizes_per_product:
                for color in sel_pro.product.colors.all():
                    colors.append({
                        "name": color.name,
                        "code": color.color
                    })

                for size in sel_pro.product.sizes.all():
                    sizes.append({
                        "name": size.name
                    })

            context['products'].append({
                "image": sel_pro.product.images.last().image.url,
                "name": sel_pro.product.name,
                "id": sel_pro.product.pk,
                "desired_color": desired_color if desired_color else '',
                "desired_size": desired_size if desired_size else '',
                "count": sel_pro.count,
                "price": sel_pro.product.price,
                "colors": colors,
                "sizes": sizes
            })


        return context

    # def save(self, *args, **kwargs):
    #     for sel_pro in self.selected_products.all():
    #         self.total_price += sel_pro.price
    #     return super(Basket, self).save(*args, **kwargs)

    def __str__(self):
        return "{}'s basket({})".format(self.user.get_full_name(), self.code)


class SelectedProduct(TimeStampedModel):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name='selected_products', null=True)
    product = models.ForeignKey('store.Product', on_delete=models.DO_NOTHING)
    size = models.ForeignKey('store.Size', on_delete=models.DO_NOTHING, blank=True, null=True)
    color = models.ForeignKey('store.Color', on_delete=models.DO_NOTHING, blank=True, null=True)
    count = models.IntegerField(blank=True, null=True, default=1)
    price = models.IntegerField(null=True)

    # def save(self, *args, **kwargs):
    #     self.price = self.count * self.product.price
    #     return super(SelectedProduct, self).save(*args, **kwargs)

    def __str__(self):
        return "{} in {}'s basket".format(self.product.name, self.basket.user.get_full_name())


class Comment(TimeStampedModel):
    product = models.ForeignKey('store.Product', on_delete=models.CASCADE, related_name='related_comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    is_approved = models.NullBooleanField()

    def __str__(self):
        return "by {} for {}".format(self.user.get_full_name(), self.product.name)


# class Image(TimeStampedModel):
#     image = models.ImageField(upload_to=get_path)
#
#     def delete(self, *args, **kwargs):
#         os.remove(self.image.path)
#         return super(Image, self).delete(*args, **kwargs)
#
#     def __str__(self):
#         return self.image.name


# class Favorite(TimeStampedModel):
#     product = models.ForeignKey('store.Product', on_delete=models.CASCADE)
#     user = models.ForeignKey('customer.User', on_delete=models.CASCADE, related_name='favorite_products')
#
#     def __str__(self):
#         return "{} likes {}".format(self.user.username, self.product.name)
