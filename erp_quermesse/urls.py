from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from quermesse import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),

    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    path('clientes/', views.clientes, name='clientes'),
    path('clientes/adicionar', views.add_cliente, name='add_cliente'),
    path('clientes/editar/<cliente_id>', views.edit_cliente, name='edit_cliente'),
    path('clientes/delete-modal', views.delete_cliente_modal, name='delete_cliente_modal'),
    path('clientes/delete/<cliente_id>', views.delete_cliente, name='delete_cliente'),

    path('autorizados/', views.autorizados, name='autorizados'),
    path('autorizados/adicionar', views.add_autorizado, name='add_autorizados'),
    path('autorizados/editar/<autorizado_id>', views.edit_autorizado, name='edit_autorizado'),
    path('autorizados/delete-modal', views.delete_autorizado_modal, name='delete_autorizado_modal'),
    path('autorizados/deletar/<autorizado_id>', views.delete_autorizado, name='delete_autorizado'),

    path('fiados/', views.fiados, name='fiados'),
    path('fiados/adicionar', views.add_fiado, name='add_fiado'),
    path('fiados/editar/<fiado_id>', views.edit_fiado, name='edit_fiado'),
    path('fiados/delete-modal', views.delete_fiado_modal, name='delete_fiado_modal'),
    path('fiados/delete/<fiado_id>', views.delete_fiado, name='delete_fiado'),

    path('produtos/', views.produtos, name='produtos'),
    path('produtos/adicionar', views.add_produto, name='add_produto'),
    path('produtos/editar/<produto_id>', views.edit_produto, name='edit_produto'),
    path('produtos/delete-modal/', views.delete_produto_modal, name='delete_produto_modal'),
    path('produtos/delete/<produto_id>', views.delete_produto, name='delete_produto'),
    path('produtos/total_produtos', views.total_produtos, name='total_produtos'),

    path('operadores/', views.operadores, name='operadores'),
    path('operadores/adicionar', views.add_operador, name='add_operador'),
    path('operadores/editar/<operador_id>', views.edit_operador, name='edit_operador'),
    path('operadores/delete-modal', views.delete_operador_modal, name='delete_operador_modal'),
    path('operadores/delete/<operador_id>', views.delete_operador, name='delete_operador'),

    path('caixas/', views.caixas, name='caixas'),
    path('caixas/adicionar', views.add_caixa, name='add_caixa'),
    path('caixas/editar/<caixa_id>', views.edit_caixa, name='edit_caixa'),
    path('caixas/delete-modal', views.delete_caixa_modal, name='delete_caixa_modal'),
    path('caixas/delete/<caixa_id>', views.delete_caixa, name='delete_caixa'),

    path('categoria_entrada/', views.categoria_entrada, name='categoria_entrada'),
    path('categoria_entrada/adicionar', views.add_categoria_entrada, name='add_categoria_entrada'),
    path('categoria_entrada/editar/<categoria_entrada_id>', views.edit_categoria_entrada, name='edit_categoria_entrada'),
    path('categoria_entrada/delete-modal', views.delete_categoria_entrada_modal, name='delete_categoria_entrada_modal'),
    path('categoria_entrada/delete/<categoria_entrada_id>', views.delete_categoria_entrada, name='delete_categoria_entrada'),

    path('categoria_despesa/', views.categoria_despesa, name='categoria_despesa'),
    path('categoria_despesa/adicionar', views.add_categoria_despesa, name='add_categoria_despesa'),
    path('categoria_despesa/editar/<categoria_despesa_id>', views.edit_categoria_despesa, name='edit_categoria_despesa'),
    path('categoria_despesa/delete-modal', views.delete_categoria_despesa_modal, name='delete_categoria_despesa_modal'),
    path('categoria_despesa/delete/<categoria_despesa_id>', views.delete_categoria_despesa, name='delete_categoria_despesa'),

    path('entradas/', views.entradas, name='entradas'),
    path('entradas/adicionar', views.add_entrada, name='add_entrada'),
    path('entradas/editar/<entrada_id>', views.edit_entrada, name='edit_entrada'),
    path('entradas/delete-modal', views.delete_entrada_modal, name='delete_entrada_modal'),
    path('entradas/delete/<entrada_id>', views.delete_entrada, name='delete_entrada'),

    path('despesas/', views.despesas, name='despesas'),
    path('despesas/adicionar', views.add_despesa, name='add_despesa'),
    path('despesas/editar/<despesa_id>', views.edit_despesa, name='edit_despesa'),
    path('despesas/delete-modal', views.delete_despesa_modal, name='delete_despesa_modal'),
    path('despesas/delete/<despesa_id>', views.delete_despesa, name='delete_despesa'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
