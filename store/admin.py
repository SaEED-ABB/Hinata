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

    actions = ['really_delete_selected']

    def get_actions(self, request):
        actions = super(ProductAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def really_delete_selected(self, request, queryset):
        for obj in queryset:
            obj.delete()

        if queryset.count() == 1:
            message_bit = "1 set_product entry was"
        else:
            message_bit = "%s set_product entries were" % queryset.count()
        self.message_user(request, "%s successfully deleted." % message_bit)

    really_delete_selected.short_description = "Delete selected entries (related image files will be deleted)"


class ProductImageAdmin(admin.ModelAdmin):

    actions = ['really_delete_selected']

    def get_actions(self, request):
        actions = super(ProductImageAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def really_delete_selected(self, request, queryset):
        for obj in queryset:
            obj.delete()

        if queryset.count() == 1:
            message_bit = "1 set_product_image entry was"
        else:
            message_bit = "%s set_product_image entries were" % queryset.count()
        self.message_user(request, "%s successfully deleted." % message_bit)

    really_delete_selected.short_description = "Delete selected entries (image file will be deleted)"


admin.site.register(Product, ProductAdmin)
admin.site.register(Color)
admin.site.register(Size)
admin.site.register(Category)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(ProductTags)
# admin.site.register(ProductProperty)
