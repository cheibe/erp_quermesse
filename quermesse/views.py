from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django.utils import timezone
from django_tables2 import RequestConfig
from decimal import Decimal
from quermesse import tables
from quermesse import models
from quermesse import forms

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
    clientes = models.Clientes.objects.all()
    table = tables.ClientesTable(clientes)
    RequestConfig(request, paginate={"per_page": 15}).configure(table)
    return render(request, 'clientes/clientes.html', {
        'title': 'Clientes',
        'table': table
    })

@login_required
def add_cliente(request):
    if request.method == 'POST':
        form = forms.ClientesForm(request, request.POST)
        if form.is_valid():
            novo_cliente = form.save(commit=False)
            novo_cliente.is_cliente = form.cleaned_data.get('is_cliente', True)
            novo_cliente.create_user = form.cleaned_data.get('create_user', request.user)
            novo_cliente.assign_user = form.cleaned_data.get('assign_user', request.user)
            novo_cliente.save()
            messages.success(request, f'O cliente {novo_cliente.nome} foi adicionado com sucesso!')
            return redirect('clientes')
    else:
        form = forms.ClientesForm(request)
    return render(request, 'clientes/add_cliente.html', {
        'title': 'Adicionar Cliente',
        'form': form
    })

@login_required
def edit_cliente(request, cliente_id):
    qs_cliente = get_object_or_404(models.Clientes, pk=cliente_id)
    if request.method == 'POST':
        form = forms.ClientesEditForm(request.POST, instance=qs_cliente)
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.assign_user = form.cleaned_data.get('assign_user', request.user)
            cliente.save()
            messages.success(request, f'O cliente {cliente.nome} foi editado com sucesso!')
            return redirect('clientes')
    else:
        form = forms.ClientesEditForm(instance=qs_cliente)
    return render(request, 'clientes/add_cliente.html', {
        'title': 'Editar cliente',
        'form': form
    })

@login_required
def delete_cliente(request, cliente_id):
    cliente = get_object_or_404(models.Clientes, pk=cliente_id)
    cliente.delete()
    messages.success(request, f'O cliente foi excluido com sucesso!')
    return redirect('clientes')

@login_required
def autorizados(request):
    autorizados = models.ClienteUsuario.objects.all()
    table = tables.AutorizadoTable(autorizados)
    RequestConfig(request, paginate={"per_page": 15}).configure(table)
    return render(request, 'autorizados/autorizados.html', {
        'title': 'Autorizados',
        'table': table
    })

@login_required
def add_autorizado(request):
    if request.method == 'POST':
        form = forms.AutorizadoForm(request.POST)
        if form.is_valid():
            novo_autorizado = form.save(commit=False)
            novo_autorizado.create_user = form.cleaned_data.get('create_user', request.user)
            novo_autorizado.assign_user = form.cleaned_data.get('assign_user', request.user)
            novo_autorizado.save()
            messages.success(request, f'O novo autorizado: "{novo_autorizado}" adicionado com sucesso!')
            return redirect('autorizados')
    else:
        form = forms.AutorizadoForm()
    return render(request, 'autorizados/add_autorizados.html', {
        'title': 'Adicionar autorizados',
        'form': form
    })

@login_required
def edit_autorizado(request, autorizado_id):
    qs_autorizado = get_object_or_404(models.ClienteUsuario, pk=autorizado_id)
    if request.method == 'POST':
        form = forms.AutorizadoForm(request.POST, instance=qs_autorizado)
        if form.is_valid():
            autorizado = form.save(commit=False)
            autorizado.assign_user = form.cleaned_data.get('assign_user', request.user)
            messages.success(request, f'O usuario autorizado: "{autorizado}" foi editado com sucesso!')
            return redirect('autorizados')
    else:
        form = forms.AutorizadoForm(instance=qs_autorizado)
    return render(request, 'autorizados/add_autorizados.html', {
        'title': 'Editar autorizado',
        'form': form
    })

@login_required
def delete_autorizado(request, autorizado_id):
    autorizado = get_object_or_404(models.ClienteUsuario, pk=autorizado_id)
    autorizado.delete()
    messages.success(request, 'O usuario autorizado foi deletado com sucesso!')
    return redirect('autorizados')

@login_required
def fiados(request):
    if request.method == 'POST':
        selecionados = request.POST.getlist('select')
        if selecionados:
            models.Fiado.objects.filter(pk__in=selecionados).update(
                is_pago=True,
                datapago=timezone.now()
            )
            messages.success(request, f"{len(selecionados)} fiado(s) marcado(s) como pago.")
        else:
            messages.warning(request, "Nenhum registro selecionado.")
        return redirect('fiados')
    form = forms.FindFiadoForm(request.GET)
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
    fiados = models.Fiado.objects.filter(**filter_search)
    soma_valor = fiados.aggregate(total_valor=Sum('valor'))['total_valor'] or Decimal('0.00')
    table = tables.FiadosTable(fiados)
    RequestConfig(request, paginate={"per_page": 15}).configure(table)
    return render(request, 'fiados/fiados.html', {
        'title': 'Fiados',
        'soma_valor': soma_valor,
        'table': table,
        'form': form
    })

@login_required
def add_fiado(request):
    if request.method == 'POST':
        form = forms.FiadoForm(request.POST)
        if form.is_valid():
            novo_fiado = form.save(commit=False)
            novo_fiado.creat_user = form.cleaned_data.get('create_user', request.user)
            novo_fiado.assign_user = form.cleaned_data.get('assign_user', request.user)
            novo_fiado.save()
            messages.success(request, f'O fiado do cliente {novo_fiado.cliente} foi adicionado com sucesso!')
            return redirect('fiados')
    else:
        form = forms.FiadoForm()
    return render(request, 'fiados/add_fiado.html', {
        'title': 'Adicionar fiado',
        'form': form
    })

@login_required
def edit_fiado(request, fiado_id):
    qs_fiado = get_object_or_404(models.Fiado, pk=fiado_id)
    if request.method == 'POST':
        form = forms.FiadoEditForm(request.POST, instance=qs_fiado)
        if form.is_valid():
            fiado = form.save(commit=False)
            fiado.assign_user = form.cleaned_data.get('assign_user', request.user)
            fiado.save()
            messages.success(request, f'O fiado do cliente {fiado.cliente} foi editado com sucesso!')
            return redirect('fiados')
    else:
        form = forms.FiadoEditForm(instance=qs_fiado)
    return render(request, 'fiados/add_fiado.html', {
        'title': 'Editar fiado',
        'form': form
    })

@login_required
def delete_fiado(request, fiado_id):
    fiado = get_object_or_404(models.Fiado, pk=fiado_id)
    fiado.delete()
    messages.success(request, 'O fiado foi excluido com sucesso!')
    return redirect('fiados')

@login_required
def produtos(request):
    produtos = models.Produto.objects.all()
    table = tables.ProdutosTable(produtos)
    RequestConfig(request, paginate={"per_page": 15}).configure(table)
    return render(request, 'produtos/produtos.html', {
        'title': 'Produtos',
        'table': table
    })

@login_required
def add_produto(request):
    if request.method == 'POST':
        form = forms.ProdutoForm(request.POST)
        if form.is_valid():
            novo_produto = form.save(commit=False)
            novo_produto.create_user = form.cleaned_data.get('create_user', request.user)
            novo_produto.assign_user = form.cleaned_data.get('assign_user', request.user)
            novo_produto.save()
            messages.success(request, f'O produto {novo_produto.nome} foi adicionado com sucesso!')
            return redirect('produtos')
    else:
        form = forms.ProdutoForm()
    return render(request, 'produtos/add_produto.html', {
        'title': 'Adicionar produto',
        'form': form
    })

@login_required
def edit_produto(request, produto_id):
    qs_produto = get_object_or_404(models.Produto, pk=produto_id)
    if request.method == 'POST':
        form = forms.ProdutoForm(request.POST, instance=qs_produto)
        if form.is_valid():
            produto = form.save(commit=False)
            produto.assign_user = form.cleaned_data.get('assign_user', request.user)
            messages.success(request, f'O produto {produto.nome} foi editado com sucesso!')
            return redirect('produtos')
    else:
        form = forms.ProdutoForm(instance=qs_produto)
    return render(request, 'produtos/add_produto.html', {
        'title': 'Editar produto',
        'form': form
    })

@login_required
def delete_produto(request, produto_id):
    produto = get_object_or_404(models.Produto, pk=produto_id)
    produto.delete()
    messages.success(request, 'O produto foi deletado com sucesso!')
    return redirect('produtos')