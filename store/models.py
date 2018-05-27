import os
from unidecode import unidecode

from django.db import models
from colorfield.fields import ColorField
from django.utils.text import slugify
from django.shortcuts import reverse
from django.template import defaultfilters
from django.utils.crypto import get_random_string
from django.db.models import Avg

from .helpers import validators
from frontview.models import TimeStampedModel


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
    slug = models.SlugField(unique=True, blank=True, null=True)

    objects = CategoryManager()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = defaultfilters.slugify(unidecode(self.name))
        return super(Category, self).save(*args, **kwargs)

    def __str__(self):
        full_name = []
        cur_cat = self
        while cur_cat:
            full_name.append(cur_cat.name)
            cur_cat = cur_cat.parent
        full_name = ' -> '.join(reversed(full_name))
        return full_name

    class Meta:
        verbose_name_plural = 'categories'


class Size(TimeStampedModel):
    name = models.CharField(max_length=200, blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = defaultfilters.slugify(unidecode(self.name))
        return super(Size, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Color(TimeStampedModel):
    name = models.CharField(max_length=200, blank=True, null=True)
    color = ColorField(default='ffffff')
    slug = models.SlugField(unique=True, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = defaultfilters.slugify(unidecode(self.name) + ' ' + self.color)
        return super(Color, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProductProperty(TimeStampedModel):
    property = models.CharField(max_length=500)
    related_product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='properties', null=True)

    def __str__(self):
        return self.property

    class Meta:
        verbose_name_plural = 'product properties'


class ProductTag(TimeStampedModel):
    tag_name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = defaultfilters.slugify(unidecode(self.tag_name))
        return super(ProductTag, self).save(*args, **kwargs)

    def __str__(self):
        return self.tag_name


class ProductFilter(TimeStampedModel):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, null=True, blank=True)

    @classmethod
    def get_all_info(cls):
        context = []
        for pro_filter in cls.objects.all():
            fil_options = []
            for fil_option in pro_filter.options.all():
                fil_options.append({
                    'name': fil_option.name,
                    'slug': fil_option.slug
                })
            context.append({
                'name': pro_filter.name,
                'slug': pro_filter.slug,
                'options': fil_options
            })

    @classmethod
    def instantiate_yourself(cls):
        sort_filter = cls.objects.get_or_create(name='مرتب سازی بر اساس', slug='sort-by')[0]
        sort_filter.options.get_or_create(name='جدید ترین', slug='newest')
        sort_filter.options.get_or_create(name='پر بازدید ترین', slug='most-viewed')
        sort_filter.options.get_or_create(name='محبوب ترین', slug='most-favorite')
        return sort_filter

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = defaultfilters.slugify(unidecode(self.name))
        return super(ProductFilter, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class FilterOption(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, null=True, blank=True)
    related_filter = models.ForeignKey(ProductFilter, on_delete=models.CASCADE, related_name='options')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = defaultfilters.slugify(unidecode(self.name))
        return super(FilterOption, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(TimeStampedModel):
    name = models.CharField(max_length=200, blank=True, null=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    material = models.CharField(max_length=200, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, related_name='related_products')
    price = models.IntegerField()
    filter_options = models.ManyToManyField(FilterOption, related_name='filtered_products', blank=True)
    tags = models.ManyToManyField(ProductTag, related_name='tagged_products', blank=True)
    sizes = models.ManyToManyField(Size, related_name='sizes', blank=True)
    colors = models.ManyToManyField(Color, related_name='colors', blank=True)

    view_counter = models.IntegerField(default=0)

    class Meta:
        ordering = ('-created_at', )

    def get_absolute_url(self):
        return reverse('frontview:product_detail', kwargs={'slug': self.slug})

    def get_rates_average(self):
        return self.rates.aggregate(Avg('rate'))['rate__avg']

    def _get_unique_slug(self):
        slug = defaultfilters.slugify(unidecode(self.name))
        counter = 1
        while Product.objects.filter(slug=slug).exists():
            slug = '{}-{}'.format(slug, counter)
            counter += 1
        return slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        return super(Product, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        for product_image in self.images.all():
            product_image.delete()
        return super(Product, self).delete(*args, **kwargs)

    def __str__(self):
        return self.name


class ProductImage(TimeStampedModel):
    def get_image_path(self, filename):
        filename = get_random_string(length=24) + "." + filename.split('.')[-1]
        path = 'products/images/{}'.format(filename)
        return path

    NAME_CHOICES = (
        ('front', 'تصویر جلو'),
        ('back', 'تصویر پشت'),
        ('other', 'تصویر عادی')
    )
    name = models.CharField(max_length=200, choices=NAME_CHOICES, default='other')
    image = models.ImageField(upload_to=get_image_path, validators=[validators.file_size])
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

    def delete(self, *args, **kwargs):
        if os.path.exists(self.image.path) and os.path.isfile(self.image.path):
            os.remove(self.image.path)
        return super(ProductImage, self).delete(*args, **kwargs)

    def __str__(self):
        return "{}-{}".format(self.product.name, self.name)
