from django.contrib import admin
from store.models import Product, Color, Size, ProductImage, Category, ProductTags


class ProductImageInline(admin.TabularInline):
    model = ProductImage


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]


admin.site.register(Product, ProductAdmin)
admin.site.register(Color)
admin.site.register(Size)
admin.site.register(Category)
admin.site.register(ProductImage)
admin.site.register(ProductTags)
