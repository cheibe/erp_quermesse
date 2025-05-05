from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from quermesse import models

@admin.register(models.QuermesseUserCuston)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Avatar e extras', {
            'fields': ('profile_picture',),
        }),
    )
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'is_staff',
        'profile_picture',
    )

@admin.register(models.Clientes)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'is_cliente', 'is_caixa', 'create_user', 'created', 'assign_user', 'modified')
