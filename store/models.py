from django.db import models
from colorfield.fields import ColorField


class BaseData(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        abstract = True


class CategoryManager(models.Manager):
    def get_all_children(self):
        children = []
        print(self.model.children)
        for u in self.model.children:
            children.append(u.get_all_children())
        return children


class Category(BaseData):
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


class Size(BaseData):
    name = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name


class Color(BaseData):
    name = models.CharField(max_length=200, blank=True, null=True)
    color = ColorField(default='ffffff')

    def __str__(self):
        return self.name


class ProductProperty(BaseData):
    property = models.CharField(max_length=500)

    def __str__(self):
        return self.property


class ProductTags(BaseData):
    tag = models.CharField(max_length=200)

    def __str__(self):
        return self.tag


class Product(BaseData):
    name = models.CharField(max_length=200, blank=True, null=True)
    material = models.CharField(max_length=200, blank=True, null=True)
    properties = models.ManyToManyField(ProductProperty, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, related_name='related_products')
    tags = models.ManyToManyField(ProductTags, related_name='filtered_products', blank=True)
    sizes = models.ManyToManyField(Size, related_name='sizes', blank=True)
    colors = models.ManyToManyField(Color, related_name='colors', blank=True)
    price = models.IntegerField()

    def __str__(self):
        return self.name


class ProductImage(BaseData):
    NAME_CHOICES = (
        ('front', 'front image'),
        ('back', 'back image'),
        ('other', 'other')
    )
    name = models.CharField(max_length=200, choices=NAME_CHOICES, default='other')
    image = models.OneToOneField('customer.Image', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return "{}-{}".format(self.product.name, self.image.image.name)
