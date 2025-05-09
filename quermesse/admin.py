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

@admin.register(models.ClienteUsuario)
class ClienteUsuarioAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'nome', 'create_user', 'created', 'assign_user', 'modified')

@admin.register(models.Fiado)
class FiadoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'cliente_usuario', 'valor', 'datadoc', 'datapago', 'is_pago')

@admin.register(models.Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'valor', 'create_user', 'created', 'assign_user', 'modified')

@admin.register(models.Caixa)
class CaixaAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'valor', 'data', 'qtd_dinheiro', 'qtd_cd', 'qtd_cc', 'pix')

@admin.register(models.ItemCaixa)
class ItemCaixa(admin.ModelAdmin):
    list_display = ('caixa', 'produtos', 'quantidade')

@admin.register(models.Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'is_despesa', 'is_entrada', 'create_user', 'created', 'assign_user', 'modified')

@admin.register(models.Despesas)
class DespesaAdmin(admin.ModelAdmin):
    list_display = ('categoria', 'valor', 'data', 'create_user', 'created', 'assign_user', 'modified')

@admin.register(models.Entradas)
class EntradaAdmin(admin.ModelAdmin):
    list_display = ('categoria', 'valor', 'data', 'create_user', 'created', 'assign_user', 'modified')