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
        return self.name


class Size(BaseData):
    name = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name


class Color(BaseData):
    name = models.CharField(max_length=200, blank=True, null=True)
    color = ColorField(default='ffffff')

    def __str__(self):
        return self.name


class Product(BaseData):
    name = models.CharField(max_length=200, blank=True, null=True)
    material = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    sizes = models.ManyToManyField(Size, related_name='sizes')
    colors = models.ManyToManyField(Color, related_name='colors')
    price = models.IntegerField()

    def __str__(self):
        return self.name


class ProductImage(BaseData):
    image = models.OneToOneField('customer.image', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return "{}-{}".format(self.product.name, self.image.image.name)
