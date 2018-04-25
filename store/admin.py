from django.contrib import admin
from store.models import Product, Color, Size, ProductImage, Category

admin.site.register(Product)
admin.site.register(Color)
admin.site.register(Size)
admin.site.register(Category)
admin.site.register(ProductImage)
