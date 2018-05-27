from django.contrib import admin
from store.models import Product, Color, Size, ProductImage, Category, ProductTag, ProductProperty, ProductFilter, FilterOption, ProductRate


class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 1


class PropertyInline(admin.StackedInline):
    model = ProductProperty
    extra = 1


class ProductFilterInline(admin.StackedInline):
    model = ProductFilter
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'name', 'slug', 'material', 'category', 'price', 'view_counter', 'get_rates_average']

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

    def has_add_permission(self, request):
        return request.user.is_authenticated and (request.user.is_superuser or request.user.is_staff)

    def has_change_permission(self, request, obj=None):
        return request.user.is_authenticated and (request.user.is_superuser or request.user.is_staff)

    def has_delete_permission(self, request, obj=None):
        return request.user.is_authenticated and (request.user.is_superuser or request.user.is_staff)

    def has_module_permission(self, request):
        return request.user.is_authenticated and (request.user.is_superuser or request.user.is_staff)


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

    def has_add_permission(self, request):
        return request.user.is_authenticated and (request.user.is_superuser or request.user.is_staff)

    def has_change_permission(self, request, obj=None):
        return request.user.is_authenticated and (request.user.is_superuser or request.user.is_staff)

    def has_delete_permission(self, request, obj=None):
        return request.user.is_authenticated and (request.user.is_superuser or request.user.is_staff)

    def has_module_permission(self, request):
        return request.user.is_authenticated and (request.user.is_superuser or request.user.is_staff)


class FilterOptionsInline(admin.StackedInline):
    model = FilterOption
    extra = 3


class ProductFilterAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'get_options_displayed']

    def get_options_displayed(self, obj):
        return ' , '.join([obj.name for obj in obj.options.all()])

    get_options_displayed.short_description = 'options'

    inlines = [FilterOptionsInline, ]

    def get_actions(self, request):
        actions = super(ProductFilterAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def has_add_permission(self, request):
        auth_perm = request.user.is_authenticated
        staff_perm = request.user.is_staff
        super_perm = request.user.is_superuser
        return auth_perm and (super_perm or staff_perm)

    def has_change_permission(self, request, obj=None):
        if obj is None:
            return True
        auth_perm = request.user.is_authenticated
        staff_perm = request.user.is_staff and obj.slug != 'sort-by'
        super_perm = request.user.is_superuser
        return auth_perm and (super_perm or staff_perm)

    def has_delete_permission(self, request, obj=None):
        if obj is None:
            return True
        auth_perm = request.user.is_authenticated
        staff_perm = request.user.is_staff and obj.slug != 'sort-by'
        super_perm = request.user.is_superuser
        return auth_perm and (super_perm or staff_perm)

    def has_module_permission(self, request):
        auth_perm = request.user.is_authenticated
        staff_perm = request.user.is_staff
        super_perm = request.user.is_superuser
        return auth_perm and (super_perm or staff_perm)


admin.site.register(Product, ProductAdmin)
admin.site.register(Color)
admin.site.register(Size)
admin.site.register(Category)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(ProductTag)
admin.site.register(ProductFilter, ProductFilterAdmin)
