from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import reverse
from django.utils.crypto import get_random_string

import uuid as uuid_lib

from .managers import UserManager
from frontview.models import TimeStampedModel
from store.models import Product, Color, Size
from store.helpers import validators


class User(AbstractBaseUser, TimeStampedModel):
    def generate_picture_path(self, filename):
        filename = get_random_string(length=24) + "." + filename.split('.')[-1]
        path = 'users/profile_pictures/{}'.format(filename)
        return path

    AC_TYPE = (
        ('user', 'Normal User'),
        ('admin', 'Admin User')
    )
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    phone_number = models.CharField(max_length=200, unique=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    account_type = models.CharField(max_length=200, blank=True, null=True, choices=AC_TYPE, default='user')
    favorites = models.ManyToManyField('store.Product', related_name='lovers', blank=True)
    profile_picture = models.ImageField(upload_to=generate_picture_path, validators=[validators.file_size], blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        ordering = ('-created_at', )
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def edit_yourself(self, phone_number=None, first_name=None, last_name=None):
        if phone_number:
            self.phone_number = phone_number
        if first_name:
            self.first_name = first_name
        if last_name:
            self.last_name = last_name
        self.save()
        status = 201

        return self.get_info(), status

    def add_address(self, address, phone_number):
        new_addr, created = self.addresses.get_or_create(address=address, phone_number=phone_number)
        if created:
            context, status = new_addr.get_info(), 201
        else:
            context, status = {"error": "This address already exists"}, 400
        return context, status

    def get_addresses(self):
        context = []
        for addr in self.addresses.all():
            context.append(addr.get_info())
        return context, 200

    def delete_address(self, address_id):
        try:
            addr = self.addresses.get(id=address_id)
            context, status = addr.get_info(), 204
            addr.delete()
        except UserAddress.DoesNotExist:
            context, status = {"error": "There is no such address for user {}".format(self.get_full_name())}, 400

        return context, status

    def get_favorites(self):
        context = []
        for favorite_product in self.favorites.all():
            images = []
            for image in favorite_product.images.all():
                images.append({
                    "url": image.image.url,
                })

            context.append({
                "product_name": favorite_product.name,
                "product_slug": favorite_product.slug,
                "images": images,
                "price": favorite_product.price,
            })
        return context

    def get_info(self):
        context = {
            "phone_number": self.phone_number,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "uuid": self.uuid,
            "profile_picture_url": self.profile_picture.url
        }
        return context

    def get_absolute_url(self):
        return reverse('customer:user_panel', kwargs={'slug': self.uuid})

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

    def get_info(self):
        context = {
            "id": self.id,
            "user": self.user.get_full_name(),
            "address": self.address,
            "phone_number": self.phone_number
        }
        return context

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
    total_price = models.IntegerField(default=0)

    class Meta:
        ordering = ('-created_at', )

    def get_info(self, all_colors_and_sizes_per_product=False):

        context = {
            "total_price": self.total_price,
            "status": self.status,
            "products": [],
        }

        for sel_pro in self.selected_products.all():
            desired_color = sel_pro.color
            desired_size = sel_pro.size
            last_image = sel_pro.product.images.last()

            colors = []
            sizes = []

            if all_colors_and_sizes_per_product:
                for color in sel_pro.product.colors.all():
                    colors.append({
                        "name": color.name,
                        "slug": color.slug,
                        "code": color.color
                    })

                for size in sel_pro.product.sizes.all():
                    sizes.append({
                        "name": size.name,
                        "slug": size.slug
                    })

            context['products'].append({
                "image": last_image.image.url if last_image else '',
                "name": sel_pro.product.name,
                "slug": sel_pro.product.slug,
                "desired_color": desired_color if desired_color else '',
                "desired_size": desired_size if desired_size else '',
                "count": sel_pro.count,
                "price": sel_pro.product.price,
                "colors": colors,
                "sizes": sizes
            })

        return context

    def add_product_to_yourself(self, product_slug, color_slug, size_slug, count):
        try:
            product = Product.objects.get(slug=product_slug)
            if color_slug and size_slug:
                color = Color.objects.get(slug=color_slug)
                size = Size.objects.get(slug=size_slug)
                sel_pro = self.selected_products.get_or_create(product=product, color=color, size=size)[0]
            elif color_slug:
                color = Color.objects.get(slug=color_slug)
                sel_pro = self.selected_products.get_or_create(product=product, color=color)[0]
            elif size_slug:
                size = Size.objects.get(slug=size_slug)
                sel_pro = self.selected_products.get_or_create(product=product, size=size)[0]
            else:
                sel_pro = self.selected_products.get_or_create(product=product)[0]

            sel_pro.count += count
            sel_pro.save()  # it does set sel_pro.price and sel_pro.basket.total_price automatically according to count and product.price

            context = {"success": "Such product successfully added to {}'s basket".format(self.user.get_full_name())}
            status = 201

        except Product.DoesNotExist:
            context = {"error": "no such product"}
            status = 404
        except Color.DoesNotExist:
            context = {"error": "no such color"}
            status = 404
        except Size.DoesNotExist:
            context = {"error": "no such size"}
            status = 404

        return context, status

    def remove_product_from_yourself(self, product_slug, count):
        try:
            sel_pro = self.selected_products.get(product__slug=product_slug)
            if count == 'all' or int(count) >= sel_pro.count:
                sel_pro.delete()
            else:
                sel_pro.count -= int(count)
                sel_pro.save()
            context = {
                "success": "Such product successfully removed from {}'s basket".format(self.user.get_full_name())
            }
            status = 201
        except SelectedProduct.DoesNotExist:
            context = {"error": "no such product"}
            status = 404

        return context, status

    def delete(self, *args, **kwargs):
        for sel_pro in self.selected_products.all():
            sel_pro.delete()
        return super(Basket, self).delete(*args, **kwargs)

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
    count = models.IntegerField(default=0)
    price = models.IntegerField(default=0)

    def delete(self, *args, **kwargs):
        self.basket.total_price -= self.price
        self.basket.save()
        return super(SelectedProduct, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        if not self.pk:
            last_price = 0
        else:
            last_price = self.price
        new_price = self.count * self.product.price
        if last_price != new_price:
            self.price = new_price
            self.basket.total_price += new_price - last_price
            self.basket.save()
        return super(SelectedProduct, self).save(*args, **kwargs)

    def __str__(self):
        return "{} in {}'s basket".format(self.product.name, self.basket.user.get_full_name())


class Comment(TimeStampedModel):
    product = models.ForeignKey('store.Product', on_delete=models.CASCADE, related_name='related_comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    is_approved = models.NullBooleanField()

    class Meta:
        ordering = ('-created_at', )

    def __str__(self):
        return "by {} for {}".format(self.user.get_full_name(), self.product.name)
