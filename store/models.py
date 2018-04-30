import os
from django.db import models
from colorfield.fields import ColorField
from django.utils.text import slugify
from django.shortcuts import reverse

from frontview.models import TimeStampedModel
# from .helpers import get_path

from django.utils.crypto import get_random_string


def get_path(instance, filename):
    name = get_random_string(length=24) + "." + filename.split('.')[-1]
    return "images/" + name


class CategoryManager(models.Manager):
    def get_all_children(self):
        children = []
        print(self.model.children)
        for u in self.model.children:
            children.append(u.get_all_children())
        return children


class Category(TimeStampedModel):
    name = models.CharField(max_length=200, blank=True, null=True)
    parent = models.ForeignKey('self', related_name="children", on_delete=models.CASCADE, blank=True, null=True)

    objects = CategoryManager()

    def __str__(self):
        full_name = []
        cur_cat = self
        while cur_cat:
            full_name.append(cur_cat.name)
            cur_cat = cur_cat.parent
        full_name = ' -> '.join(reversed(full_name))
        return full_name


class Size(TimeStampedModel):
    name = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name


class Color(TimeStampedModel):
    name = models.CharField(max_length=200, blank=True, null=True)
    color = ColorField(default='ffffff')

    def __str__(self):
        return self.name


class ProductProperty(TimeStampedModel):
    property = models.CharField(max_length=500)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='properties', null=True)

    def __str__(self):
        return self.property


class ProductTags(TimeStampedModel):
    tag_name = models.CharField(max_length=200)

    def __str__(self):
        return self.tag_name


class Product(TimeStampedModel):
    name = models.CharField(max_length=200, blank=True, null=True)
    material = models.CharField(max_length=200, blank=True, null=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    # properties = models.ManyToManyField(ProductProperty, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, related_name='related_products')
    tags = models.ManyToManyField(ProductTags, related_name='filtered_products', blank=True)
    sizes = models.ManyToManyField(Size, related_name='sizes', blank=True)
    colors = models.ManyToManyField(Color, related_name='colors', blank=True)
    price = models.IntegerField()

    class Meta:
        ordering = ('-created_at', )

    def get_absolute_url(self):
        return reverse('frontview:product_detail', kwargs={'slug': self.slug})

    def _get_unique_slug(self):
        slug = slugify(self.name)
        counter = 1
        while Product.objects.filter(slug=slug).exists():
            slug = '{}-{}'.format(slug, counter)
            counter += 1
        return slug

    def save(self, *args, **kwargs):
        self.slug = self._get_unique_slug()
        super(Product, self).save()

    def __str__(self):
        return self.name


class ProductImage(TimeStampedModel):
    NAME_CHOICES = (
        ('front', 'front image'),
        ('back', 'back image'),
        ('other', 'other')
    )
    name = models.CharField(max_length=200, choices=NAME_CHOICES, default='other')
    image = models.ImageField(upload_to=get_path)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

    def delete(self, *args, **kwargs):
        os.remove(self.image.path)
        return super(ProductImage, self).delete(*args, **kwargs)

    def __str__(self):
        return "{}-{}".format(self.product.name, self.name)
