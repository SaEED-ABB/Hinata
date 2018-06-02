from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html

from customer.models import User, UserAddress, Basket, SelectedProduct, Comment
from .forms import UserCreationForm, UserChangeForm


class UserAddressInline(admin.StackedInline):
    model = UserAddress
    extra = 1


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('phone_number', 'first_name', 'last_name', 'account_type', 'get_user_panel_link')
    list_filter = ('account_type',)
    fieldsets = (
        (None, {'fields': ('phone_number',)}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'favorites', 'profile_picture')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'first_name', 'last_name', 'account_type', 'password1', 'password2')
        }),
    )
    search_fields = ('phone_number',)
    ordering = ('phone_number',)
    filter_horizontal = ()

    inlines = [UserAddressInline, ]

    def get_user_panel_link(self, obj):
        return format_html('<a href="{url}">{url}</a>', url=obj.get_absolute_url())

    get_user_panel_link.short_description = 'User Panel Link'

    actions = ['really_delete_selected']

    def get_queryset(self, request):
        qs = super(UserAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(pk=request.user.pk)

    def get_actions(self, request):
        actions = super(UserAdmin, self).get_actions(request)
        del actions['delete_selected']
        if not request.user.is_superuser and 'really_delete_selected' in actions:
            del actions['really_delete_selected']
        return actions

    def really_delete_selected(self, request, queryset):
        for obj in queryset:
            obj.delete()

        if queryset.count() == 1:
            message_bit = "1 set_basket entry was"
        else:
            message_bit = "%s set_basket entries were" % queryset.count()
        self.message_user(request, "%s successfully deleted." % message_bit)

    really_delete_selected.short_description = "Delete selected entries"

    def has_add_permission(self, request):
        auth_perm = request.user.is_authenticated
        super_perm = request.user.is_superuser
        return auth_perm and super_perm

    def has_change_permission(self, request, obj=None):
        if obj is None:
            return True
        auth_perm = request.user.is_authenticated
        staff_perm = request.user.is_staff and request.user == obj
        super_perm = request.user.is_superuser
        return auth_perm and (super_perm or staff_perm)

    def has_delete_permission(self, request, obj=None):
        if obj is None:
            return True
        auth_perm = request.user.is_authenticated
        staff_perm = request.user.is_staff and request.user == obj
        super_perm = request.user.is_superuser
        return auth_perm and (super_perm or staff_perm)

    def has_module_permission(self, request):
        auth_perm = request.user.is_authenticated
        super_perm = request.user.is_superuser
        staff_perm = request.user.is_staff
        return auth_perm and (super_perm or staff_perm)


class SelectedProductInline(admin.StackedInline):
    model = SelectedProduct
    extra = 1


class BasketAdmin(admin.ModelAdmin):
    list_display = ('code', 'user', 'phone_number', 'address', 'status', 'payment_type', 'total_price', 'paid_at')

    readonly_fields = ('code', )
    fieldsets = (
        (None, {
            'fields': ('user', 'phone_number', 'address', 'payment_type', 'total_price', 'status', ),
        }),
    )

    inlines = [SelectedProductInline]

    actions = ['really_delete_selected']

    def get_actions(self, request):
        actions = super(BasketAdmin, self).get_actions(request)
        del actions['delete_selected']
        if not request.user.is_superuser and 'really_delete_selected' in actions:
            del actions['really_delete_selected']
        return actions

    def really_delete_selected(self, request, queryset):
        for obj in queryset:
            obj.delete()

        if queryset.count() == 1:
            message_bit = "1 set_basket entry was"
        else:
            message_bit = "%s set_basket entries were" % queryset.count()
        self.message_user(request, "%s successfully deleted." % message_bit)

    really_delete_selected.short_description = "Delete selected entries"

    def has_add_permission(self, request):
        return request.user.is_authenticated and request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_authenticated and (request.user.is_superuser or request.user.is_staff)

    def has_delete_permission(self, request, obj=None):
        return request.user.is_authenticated and request.user.is_superuser

    def has_module_permission(self, request):
        return request.user.is_authenticated and (request.user.is_superuser or request.user.is_staff)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('comment', 'product', 'user', 'session_name', 'is_approved')

    fieldsets = (
        (None, {'fields': ('comment', 'product', 'is_approved',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide', ),
            'fields': ('comment', 'product')
        })
    )

    actions = ['really_delete_selected']

    def get_actions(self, request):
        actions = super(CommentAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def really_delete_selected(self, request, queryset):
        counter = 0
        for obj in queryset:
            if request.user.is_superuser or request.user == obj.user:
                obj.delete()
        if counter == 0:
            return
        elif counter == 1:
            message_bit = "1 set_selected_product entry was"
        else:
            message_bit = "%s set_selected_products entries were" % counter
        self.message_user(request, "%s successfully deleted." % message_bit)

    really_delete_selected.short_description = "Delete selected entries"

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.user = request.user
            obj.is_approved = True
        return super(CommentAdmin, self).save_model(request, obj, form, change)

    def has_add_permission(self, request):
        auth_perm = request.user.is_authenticated
        staff_perm = request.user.is_staff
        super_perm = request.user.is_superuser
        return auth_perm and (super_perm or staff_perm)

    def has_change_permission(self, request, obj=None):
        if obj is None:
            return True
        auth_perm = request.user.is_authenticated
        staff_perm = request.user.is_staff and request.user == obj.user
        super_perm = request.user.is_superuser
        return auth_perm and (super_perm or staff_perm)

    def has_delete_permission(self, request, obj=None):
        if obj is None:
            return True
        auth_perm = request.user.is_authenticated
        staff_perm = request.user.is_staff and request.user == obj.user
        super_perm = request.user.is_superuser
        return auth_perm and (super_perm or staff_perm)

    def has_module_permission(self, request):
        auth_perm = request.user.is_authenticated
        staff_perm = request.user.is_staff
        super_perm = request.user.is_superuser
        return auth_perm and (super_perm or staff_perm)


class SelectedProductAdmin(admin.ModelAdmin):

    actions = ['really_delete_selected']

    def get_actions(self, request):
        actions = super(SelectedProductAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def really_delete_selected(self, request, queryset):
        for obj in queryset:
            obj.delete()

        if queryset.count() == 1:
            message_bit = "1 set_selected_product entry was"
        else:
            message_bit = "%s set_selected_products entries were" % queryset.count()
        self.message_user(request, "%s successfully deleted." % message_bit)

    really_delete_selected.short_description = "Delete selected entries"


admin.site.register(User, UserAdmin)
# admin.site.register(SelectedProduct, SelectedProductAdmin)
admin.site.register(Basket, BasketAdmin)
admin.site.register(Comment, CommentAdmin)
