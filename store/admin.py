from django.contrib import admin
from store.models import Product, Color, Size, ProductImage, Category, ProductTags, ProductProperty


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class PropertyInline(admin.TabularInline):
    model = ProductProperty
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, PropertyInline]


admin.site.register(Product, ProductAdmin)
# admin.site.register(Color)
# admin.site.register(Size)
# admin.site.register(Category)
admin.site.register(ProductImage)
# admin.site.register(ProductTags)
# admin.site.register(ProductProperty)
