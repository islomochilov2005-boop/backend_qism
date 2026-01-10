from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model

User = get_user_model()


class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'telefon', 'yaratilgan']
    search_fields = ['username', 'email', 'telefon']

    fieldsets = BaseUserAdmin.fieldsets + (
        ('Qo\'shimcha ma\'lumotlar', {
            'fields': ('telefon', 'rasm')
        }),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Qo\'shimcha ma\'lumotlar', {
            'fields': ('telefon', 'rasm')
        }),
    )


admin.site.register(User, UserAdmin)