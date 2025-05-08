from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django.db import transaction
from django.utils import timezone
from django_tables2 import RequestConfig
from django.forms import inlineformset_factory
from decimal import Decimal
from quermesse import tables
from quermesse import models
from quermesse import forms

ItemCaixaCreatFormSet = inlineformset_factory(
    models.Caixa,
    models.ItemCaixa,
    fields=('produtos','quantidade'),
    extra=1,
    can_delete=True
)

ItemCaixaEditFormSet = inlineformset_factory(
    models.Caixa,
    models.ItemCaixa,
    fields=('produtos','quantidade'),
    extra=0,
    can_delete=True
)

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
    clientes = models.Clientes.objects.filter(is_cliente=True).all()
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
            novo_cliente.is_caixa = form.cleaned_data.get('is_caixa', False)
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
    fiados = models.Fiado.objects.filter(**filter_search).order_by('cliente__nome')
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
def operadores(request):
    operadores = models.Clientes.objects.filter(is_caixa=True).all()
    table = tables.OperadorTable(operadores)
    RequestConfig(request, paginate={"per_page": 15}).configure(table)
    return render(request, 'operadores/operadores.html', {
        'title': 'Operadores',
        'table': table
    })

@login_required
def add_operador(request):
    if request.method == 'POST':
        form = forms.OperadoresForm(request, request.POST)
        if form.is_valid():
            novo_operador = form.save(commit=False)
            novo_operador.is_caixa = form.cleaned_data.get('is_caixa', True)
            novo_operador.is_cliente = form.cleaned_data.get('is_cliente', False)
            novo_operador.create_user = form.cleaned_data.get('create_user', request.user)
            novo_operador.assign_user = form.cleaned_data.get('assign_user', request.user)
            novo_operador.save()
            messages.success(request, f'O operador {novo_operador.nome} foi adicionado com sucesso!')
            return redirect('operadores')
    else:
        form = forms.OperadoresForm(request)
    return render(request, 'operadores/add_operador.html', {
        'title': 'Adicionar operador',
        'form': form
    })

@login_required
def edit_operador(request, operador_id):
    qs_operador = get_object_or_404(models.Clientes, pk=operador_id)
    if request.method == 'POST':
        form = forms.OperadoresEditForm(request.POST, instance=qs_operador)
        if form.is_valid():
            operador = form.save(commit=False)
            operador.assign_user = form.cleaned_data.get('assign_user', request.user)
            operador.save()
            messages.success(request, f'O operador {operador.nome} foi editado com sucesso!')
            return redirect('operadores')
    else:
        form = forms.OperadoresEditForm(instance=qs_operador)
    return render(request, 'operadores/add_operador.html', {
        'title': 'Editar operador',
        'form': form
    })

@login_required
def delete_operador(request, operador_id):
    operador = get_object_or_404(models.Clientes, pk=operador_id)
    operador.delete()
    messages.success(request, 'O operador foi deletado com sucesso!')
    return redirect('operadores')

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
            produto.save()
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

@login_required
def caixas(request):
    form = forms.CaixaFindForm(request.GET)
    form.fields['cliente'].required = False
    form.fields['data'].required = False
    filter_search = {}
    if form.is_valid():
        cliente = form.cleaned_data.get('cliente')
        data = form.cleaned_data.get('data')
        if cliente:
            filter_search['cliente'] = cliente
        if data:
            filter_search['data'] = data
    caixas = models.Caixa.objects.filter(**filter_search)
    soma_valor = caixas.aggregate(total_valor=Sum('valor'))['total_valor'] or Decimal('0.00')
    soma_dinheiro = caixas.aggregate(total_valor=Sum('qtd_dinheiro'))['total_valor'] or Decimal('0.00')
    soma_cd = caixas.aggregate(total_valor=Sum('qtd_cd'))['total_valor'] or Decimal('0.00')
    soma_cc = caixas.aggregate(total_valor=Sum('qtd_cc'))['total_valor'] or Decimal('0.00')
    soma_pix = caixas.aggregate(total_valor=Sum('pix'))['total_valor'] or Decimal('0.00')
    table = tables.CaixaTable(caixas)
    RequestConfig(request, paginate={"per_page": 25}).configure(table)
    return render(request, 'caixas/caixas.html', {
        'title': 'Caixas',
        'form': form,
        'table': table,
        'soma_valor': soma_valor,
        'soma_dinheiro': soma_dinheiro,
        'soma_cd': soma_cd,
        'soma_cc': soma_cc,
        'soma_pix': soma_pix
    })

@login_required
def add_caixa(request):
    if request.method == 'POST':
        form = forms.CaixaForm(request.POST)
        formset = ItemCaixaCreatFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            caixa = form.save(commit=False)
            caixa.create_user = form.cleaned_data.get('create_user', request.user)
            caixa.assign_user = form.cleaned_data.get('assign_user', request.user)
            caixa.save()
            formset.instance = caixa
            formset.save()
            messages.success(request, f'O novo registro do caixa foi feito com sucesso!')
            return redirect('caixas')
    else:
        form = forms.CaixaForm()
        formset = ItemCaixaCreatFormSet()
    return render(request, 'caixas/add_caixa.html', {
        'title': 'Adicionar novo registro',
        'form': form,
        'formset': formset
    })

@login_required
def edit_caixa(request, caixa_id):
    caixa = get_object_or_404(models.Caixa, pk=caixa_id)
    if request.method == 'POST':
        form = forms.CaixaForm(request.POST, instance=caixa)
        formset = ItemCaixaEditFormSet(request.POST, instance=caixa)
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                caixa = form.save(commit=False)
                caixa.assign_user = request.user
                caixa.save()
                formset.save()
            messages.success(request, 'O registro do caixa foi editado com sucesso!')
            return redirect('caixas')
    else:
        form    = forms.CaixaForm(instance=caixa)
        formset = ItemCaixaEditFormSet(instance=caixa)
    return render(request, 'caixas/add_caixa.html', {
        'title':   'Editar registro do caixa',
        'form':    form,
        'formset': formset,
    })

@login_required
def delete_caixa(request, caixa_id):
    qs_caixa = get_object_or_404(models.Caixa, pk=caixa_id)
    qs_caixa.delete()
    messages.success(request, 'O registro do caixa foi deletado com sucesso!')
    return redirect('caixas')

@login_required
def categoria_entrada(request):
    categoria_entrada = models.Categoria.objects.filter(is_entrada=True).all()
    table = tables.CategoriaEntradaTable(categoria_entrada)
    RequestConfig(request, paginate={"per_page": 15}).configure(table)
    return render(request, 'categorias/categorias_entradas.html', {
        'title': 'Categorias',
        'table': table
    })

@login_required
def add_categoria_entrada(request):
    if request.method == 'POST':
        form = forms.CategoriaForm(request, request.POST)
        if form.is_valid():
            nova_categoria = form.save(commit=False)
            nova_categoria.is_despesa = False
            nova_categoria.is_entrada = True
            nova_categoria.create_user = form.cleaned_data.get('create_user') or request.user
            nova_categoria.assign_user = form.cleaned_data.get('assign_user') or request.user
            nova_categoria.save()
            messages.success(request, f'A categoria {nova_categoria.nome} foi adicionada com sucesso!')
            return redirect('categoria_entrada')
    else:
        form = forms.CategoriaForm(request)
    return render(request, 'categorias/add_categoria_entrada.html', {
        'title': 'Adicionar categoria',
        'form': form
    })

@login_required
def edit_categoria_entrada(request, categoria_entrada_id):
    qs_categoria = get_object_or_404(models.Categoria, pk=categoria_entrada_id)
    if request.method == 'POST':
        form = forms.CategoriaEditForm(request.POST, instance=qs_categoria)
        if form.is_valid():
            categoria = form.save(commit=False)
            categoria.assign_user = form.cleaned_data.get('assign_user') or request.user
            categoria.save()
            messages.success(request, f'A categoria {categoria.nome} foi editada com sucesso!')
            return redirect('categoria_entrada')
    else:
        form = forms.CategoriaEditForm(instance=qs_categoria)
    return render(request, 'categorias/add_categoria_entrada.html', {
        'title': 'Editar categoria',
        'form': form
    })

@login_required
def delete_categoria_entrada(request, categoria_entrada_id):
    categoria = get_object_or_404(models.Categoria, pk=categoria_entrada_id)
    categoria.delete()
    messages.success(request, 'A categoria foi deletada com sucesso!')
    return redirect('categoria_entrada')

@login_required
def categoria_despesa(request):
    categoria_despesa = models.Categoria.objects.filter(is_despesa=True).all()
    table = tables.CategoriaDespesaTable(categoria_despesa)
    RequestConfig(request, paginate={"per_page": 15}).configure(table)
    return render(request, 'categorias/categorias_despesas.html', {
        'title': 'Categorias',
        'table': table
    })

@login_required
def add_categoria_despesa(request):
    if request.method == 'POST':
        form = forms.CategoriaForm(request, request.POST)
        if form.is_valid():
            nova_categoria = form.save(commit=False)
            nova_categoria.is_despesa = True
            nova_categoria.is_entrada = False
            nova_categoria.create_user = form.cleaned_data.get('create_user') or request.user
            nova_categoria.assign_user = form.cleaned_data.get('assign_user') or request.user
            nova_categoria.save()
            messages.success(request, f'A categoria {nova_categoria.nome} foi adicionada com sucesso!')
            return redirect('categoria_despesa')
    else:
        form = forms.CategoriaForm(request)
    return render(request, 'categorias/add_categoria_despesa.html', {
        'title': 'Adicionar categoria',
        'form': form
    })

@login_required
def edit_categoria_despesa(request, categoria_despesa_id):
    qs_categoria = get_object_or_404(models.Categoria, pk=categoria_despesa_id)
    if request.method == 'POST':
        form = forms.CategoriaEditForm(request.POST, instance=qs_categoria)
        if form.is_valid():
            categoria = form.save(commit=False)
            categoria.assign_user = form.cleaned_data.get('assign_user') or request.user
            categoria.save()
            messages.success(request, f'A categoria {categoria.nome} foi editada com sucesso!')
            return redirect('categoria_despesa')
    else:
        form = forms.CategoriaEditForm(instance=qs_categoria)
    return render(request, 'categorias/add_categoria_despesa.html', {
        'title': 'Editar categoria',
        'form': form
    })

@login_required
def delete_categoria_despesa(request, categoria_despesa_id):
    categoria = get_object_or_404(models.Categoria, pk=categoria_despesa_id)
    categoria.delete()
    messages.success(request, 'A categoria foi deletada com sucesso!')
    return redirect('categoria_despesa')


@login_required
def entradas(request):
    form = forms.EntradasFindForm(request.GET)
    form.fields['categoria'].required = False
    form.fields['data'].required = False
    filter_search = {}
    if form.is_valid():
        categoria = form.cleaned_data.get('categoria')
        data = form.cleaned_data.get('data')
        if categoria:
            filter_search['categoria'] = categoria
        if data:
            filter_search['data'] = data
    entradas = models.Entradas.objects.filter(**filter_search).all()
    soma_valor = entradas.aggregate(total_valor=Sum('valor'))['total_valor'] or Decimal('0.00')
    table = tables.EntradasTable(entradas)
    RequestConfig(request, paginate={"per_page": 25}).configure(table)
    return render(request, 'entradas/entradas.html', {
        'title': 'Entradas',
        'form': form,
        'table': table,
        'soma_valor': soma_valor
    })

@login_required
def add_entrada(request):
    if request.method == 'POST':
        form = forms.EntradasForm(request.POST)
        if form.is_valid():
            nova_entrada = form.save(commit=False)
            nova_entrada.create_user = form.cleaned_data.get('create_user') or request.user
            nova_entrada.assign_user = form.cleaned_data.get('assign_user') or request.user
            nova_entrada.save()
            messages.success(request, 'O novo registro de entradas foi feito com sucesso!')
            return redirect('entradas')
    else:
        form = forms.EntradasForm()
    return render(request, 'entradas/add_entrada.html', {
        'title': 'Adicionar entrada avulsa',
        'form': form
    })

@login_required
def edit_entrada(request, entrada_id):
    qs_entrada = get_object_or_404(models.Entradas, pk=entrada_id)
    if request.method == 'POST':
        form = forms.EntradasForm(request.POST, instance=qs_entrada)
        if form.is_valid():
            entrada = form.save(commit=False)
            entrada.assign_user = form.cleaned_data.get('assign_user') or request.user
            entrada.save()
            messages.success(request, 'O registro de entradas foi editado com sucesso!')
            return redirect('entradas')
    else:
        form = forms.EntradasForm(instance=qs_entrada)
    return render(request, 'entradas/add_entrada.html', {
        'title': 'Editar entrada avulsa',
        'form': form
    })

@login_required
def delete_entrada(request, entrada_id):
    entrada = get_object_or_404(models.Entradas, pk=entrada_id)
    entrada.delete()
    messages.success(request, 'O registro da entrada foi deletado com sucesso!')
    return redirect('entradas')