from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

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
    list_display = ('phone_number', 'first_name', 'last_name', 'account_type')
    list_filter = ('account_type',)
    fieldsets = (
        (None, {'fields': ('phone_number', )}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'favorites', 'profile_picture')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'first_name', 'last_name', 'password1', 'password2')
        }),
    )
    search_fields = ('phone_number',)
    ordering = ('phone_number',)
    filter_horizontal = ()

    inlines = [UserAddressInline, ]


class SelectedProductInline(admin.StackedInline):
    model = SelectedProduct
    extra = 1


class BasketAdmin(admin.ModelAdmin):
    list_display = ('code', 'user', 'status', 'payment_type', 'total_price')

    inlines = [SelectedProductInline]

    actions = ['really_delete_selected']

    def get_actions(self, request):
        actions = super(BasketAdmin, self).get_actions(request)
        del actions['delete_selected']
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


class CommentAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'comment', 'is_approved')


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
admin.site.register(SelectedProduct, SelectedProductAdmin)
admin.site.register(Basket, BasketAdmin)
admin.site.register(Comment, CommentAdmin)
