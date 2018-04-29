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
        (None, {'fields': ('phone_number', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'favorites')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'first_name', 'last_name', 'password1', 'password2')}
        ),
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


class CommentAdmin(admin.ModelAdmin):

    list_display = ('product', 'user', 'comment', 'is_approved')



# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
# admin.site.unregister(Group)


admin.site.register(SelectedProduct)
admin.site.register(Basket, BasketAdmin)
# admin.site.register(UserAddress)
admin.site.register(Comment, CommentAdmin)
# admin.site.register(Image)
# admin.site.register(Favorite)
