from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django.utils import timezone
from quermesse.tables import ClientesTable, AutorizadoTable ,FiadosTable
from quermesse.models import Clientes, ClienteUsuario ,Fiado
from quermesse.forms import ClientesForm, ClientesEditForm, AutorizadoForm, FiadoForm, FindFiadoForm, FiadoEditForm
from decimal import Decimal

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login/login.html', {'form': form})

def logout(request):
    auth_logout(request)
    return redirect('login')

@login_required
def home(request):
    return render(request, 'base.html', {
        'title': 'Dashboard',
    })

@login_required
def clientes(request):
    clientes = Clientes.objects.all()
    table = ClientesTable(clientes)
    return render(request, 'clientes/clientes.html', {
        'title': 'Clientes',
        'table': table
    })

@login_required
def add_cliente(request):
    if request.method == 'POST':
        form = ClientesForm(request, request.POST)
        if form.is_valid():
            novo_cliente = form.save(commit=False)
            novo_cliente.is_cliente = form.cleaned_data.get('is_cliente', True)
            novo_cliente.create_user = form.cleaned_data.get('create_user', request.user)
            novo_cliente.assign_user = form.cleaned_data.get('assign_user', request.user)
            novo_cliente.save()
            messages.success(request, f'O cliente {novo_cliente.nome} foi adicionado com sucesso!')
            return redirect('clientes')
    else:
        form = ClientesForm(request)
    return render(request, 'clientes/add_cliente.html', {
        'title': 'Adicionar Cliente',
        'form': form
    })

@login_required
def edit_cliente(request, cliente_id):
    cliente = get_object_or_404(Clientes, pk=cliente_id)
    if request.method == 'POST':
        form = ClientesEditForm(request.POST, instance=cliente)
        if form.is_valid():
            cliente_edit = form.save(commit=False)
            cliente_edit.assign_user = form.cleaned_data.get('assign_user', request.user)
            cliente_edit.save()
            messages.success(request, f'O cliente {cliente_edit} foi editado com sucesso!')
            return redirect('clientes')
    else:
        form = ClientesEditForm(instance=cliente)
    return render(request, 'clientes/add_cliente.html', {
        'title': 'Editar cliente',
        'form': form
    })

@login_required
def delete_cliente(request, cliente_id):
    cliente = get_object_or_404(Clientes, pk=cliente_id)
    cliente.delete()
    messages.success(request, f'O cliente foi excluido com sucesso!')
    return redirect('clientes')

@login_required
def autorizados(request):
    autorizados = ClienteUsuario.objects.all()
    table = AutorizadoTable(autorizados)
    return render(request, 'autorizados/autorizados.html', {
        'title': 'Autorizados',
        'table': table
    })

@login_required
def add_autorizado(request):
    if request.method == 'POST':
        form = AutorizadoForm(request.POST)
        if form.is_valid():
            novo_autorizado = form.save(commit=False)
            novo_autorizado.create_user = form.cleaned_data.get('create_user', request.user)
            novo_autorizado.assign_user = form.cleaned_data.get('assign_user', request.user)
            novo_autorizado.save()
            messages.success(request, f'O novo autorizado: "{novo_autorizado}" adicionado com sucesso!')
            return redirect('autorizados')
    else:
        form = AutorizadoForm()
    return render(request, 'autorizados/add_autorizados.html', {
        'title': 'Adicionar autorizados',
        'form': form
    })

@login_required
def edit_autorizado(request, autorizado_id):
    autorizado = get_object_or_404(ClienteUsuario, pk=autorizado_id)
    if request.method == 'POST':
        form = AutorizadoForm(request.POST, instance=autorizado)
        if form.is_valid():
            autorizado = form.save(commit=False)
            autorizado.assign_user = form.cleaned_data.get('assign_user', request.user)
            messages.success(request, f'O usuario autorizado: "{autorizado}" foi editado com sucesso!')
            return redirect('autorizados')
    else:
        form = AutorizadoForm(instance=autorizado)
    return render(request, 'autorizados/add_autorizados.html', {
        'title': 'Editar autorizado',
        'form': form
    })

@login_required
def delete_autorizado(request, autorizado_id):
    autorizado = get_object_or_404(ClienteUsuario, pk=autorizado_id)
    autorizado.delete()
    messages.success(request, 'O usuario autorizado foi deletado com sucesso!')
    return redirect('autorizados')

@login_required
def fiados(request):
    if request.method == 'POST':
        selecionados = request.POST.getlist('select')
        if selecionados:
            Fiado.objects.filter(pk__in=selecionados).update(
                is_pago=True,
                datapago=timezone.now()
            )
            messages.success(request, f"{len(selecionados)} fiado(s) marcado(s) como pago.")
        else:
            messages.warning(request, "Nenhum registro selecionado.")
        return redirect('fiados')
    form = FindFiadoForm(request.GET)
    form.fields['cliente'].required = False
    form.fields['datadoc'].required = False
    filter_search = {}
    if form.is_valid():
        cliente = form.cleaned_data.get('cliente')
        datadoc = form.cleaned_data.get('datadoc')
        datapago = form.cleaned_data.get('datapago')
        if cliente:
            filter_search['cliente'] = cliente
        if datadoc:
            filter_search['datadoc'] = datadoc
        if datapago:
            filter_search['datapago'] = datapago
    fiados = Fiado.objects.filter(**filter_search)
    soma_valor = fiados.aggregate(total_valor=Sum('valor'))['total_valor'] or Decimal('0.00')
    table = FiadosTable(fiados)
    return render(request, 'fiados/fiados.html', {
        'title': 'Fiados',
        'soma_valor': soma_valor,
        'table': table,
        'form': form
    })

@login_required
def add_fiado(request):
    if request.method == 'POST':
        form = FiadoForm(request.POST)
        if form.is_valid():
            novo_fiado = form.save(commit=False)
            novo_fiado.creat_user = form.cleaned_data.get('create_user', request.user)
            novo_fiado.assign_user = form.cleaned_data.get('assign_user', request.user)
            novo_fiado.save()
            messages.success(request, f'O fiado do cliente {novo_fiado.cliente} foi adicionado com sucesso!')
            return redirect('fiados')
    else:
        form = FiadoForm()
    return render(request, 'fiados/add_fiado.html', {
        'title': 'Adicionar fiado',
        'form': form
    })

@login_required
def edit_fiado(request, fiado_id):
    fiado = get_object_or_404(Fiado, pk=fiado_id)
    if request.method == 'POST':
        form = FiadoEditForm(request.POST, instance=fiado)
        if form.is_valid():
            fiado = form.save(commit=False)
            fiado.assign_user = form.cleaned_data.get('assign_user', request.user)
            fiado.save()
            messages.success(request, f'O fiado do cliente {fiado.cliente} foi editado com sucesso!')
            return redirect('fiados')
    else:
        form = FiadoEditForm(instance=fiado)
    return render(request, 'fiados/add_fiado.html', {
        'title': 'Editar fiado',
        'form': form
    })

@login_required
def delete_fiado(request, fiado_id):
    fiado = get_object_or_404(Fiado, pk=fiado_id)
    fiado.delete()
    messages.success(request, 'O fiado foi excluido com sucesso!')
    return redirect('fiados')