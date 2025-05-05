import django_tables2 as tables
from quermesse import models

class ClientesTable(tables.Table):
    nome = tables.Column(verbose_name='Nome', orderable=False)
    is_cliente = tables.BooleanColumn(verbose_name='Cliente', yesno=('Sim', 'Não'), orderable=False)
    is_caixa = tables.BooleanColumn(verbose_name='Operador', yesno=('Sim', 'Não'), orderable=False)
    opcoes = tables.TemplateColumn(template_name='clientes/botao_acoes_clientes.html', verbose_name='Opções', orderable=False)

    class Meta:
        model = models.Clientes
        attrs = {'class': 'table table-bordered table-hover'}
        fields = ('nome', 'is_cliente', 'is_caixa')

class AutorizadoTable(tables.Table):
    cliente = tables.Column(verbose_name='Cliente', orderable=False)
    nome = tables.Column(verbose_name='Nome do autorizado', orderable=False)
    opcoes = tables.TemplateColumn(template_name='autorizados/botao_acoes_autorizados.html', verbose_name='Opções', orderable=False)

    class Meta:
        model = models.ClienteUsuario
        attrs = {'class': 'table table-bordered table-hover'}
        fields = ('cliente', 'nome')

class FiadosTable(tables.Table):
    select = tables.CheckBoxColumn(accessor='pk', attrs={'th__input': {'id': 'select-all'}, 'td__input': {'class': 'row-select'}})
    cliente = tables.Column(verbose_name='Cliente', orderable=False)
    cliente_usuario = tables.Column(verbose_name='Autorizado do cliente', orderable=False)
    valor = tables.Column(verbose_name='Valor', orderable=False)
    datadoc = tables.DateColumn(verbose_name='Data do lançamento', orderable=False)
    is_pago = tables.BooleanColumn(verbose_name='Pago', yesno=('Sim', 'Não'), orderable=False)
    opcoes = tables.TemplateColumn(template_name='fiados/botao_acoes_fiados.html', verbose_name='Opções', orderable=False)

    class Meta:
        model = models.Fiado
        attrs = {'class': 'table table-bordered table-hover'}
        fields = ('select', 'cliente', 'cliente_usuario', 'valor', 'datadoc', 'is_pago')

class ProdutosTable(tables.Table):
    nome = tables.Column(verbose_name='Nome', orderable=False)
    valor = tables.Column(verbose_name='Valor', orderable=False)
    opcoes = tables.TemplateColumn(template_name='produtos/botao_acoes_produtos.html', verbose_name='Opções', orderable=False)
    class Meta:
        model = models.Produto
        attrs = {'class': 'table table-bordered table-hover'}
        fields = ('nome', 'valor')