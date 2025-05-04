from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from quermesse import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),

    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    path('clientes/', views.clientes, name='clientes'),
    path('clientes/adicionar', views.add_cliente, name='add_cliente'),
    path('clientes/editar/<cliente_id>', views.edit_cliente, name='edit_cliente'),
    path('clientes/delete/<cliente_id>', views.delete_cliente, name='delete_cliente'),

    path('autorizados/', views.autorizados, name='autorizados'),
    path('autorizados/adicionar', views.add_autorizado, name='add_autorizados'),
    path('autorizados/editar/<autorizado_id>', views.edit_autorizado, name='edit_autorizado'),
    path('autorizados/deletar/<autorizado_id>', views.delete_autorizado, name='delete_autorizado'),

    path('fiados/', views.fiados, name='fiados'),
    path('fiados/adicionar', views.add_fiado, name='add_fiado'),
    path('fiados/editar/<fiado_id>', views.edit_fiado, name='edit_fiado'),
    path('fiados/delete/<fiado_id>', views.delete_fiado, name='delete_fiado'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
