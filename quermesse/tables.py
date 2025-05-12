import django_tables2 as tables
from quermesse import models

class ClientesTable(tables.Table):
    nome = tables.Column(verbose_name='Nome', orderable=False)
    opcoes = tables.TemplateColumn(template_name='clientes/botao_acoes_clientes.html', verbose_name='Opções', orderable=False)

    class Meta:
        model = models.Clientes
        template_name = "django_tables2/bootstrap4.html"
        attrs = {'class': 'table table-bordered table-hover'}
        fields = ('nome',)

class AutorizadoTable(tables.Table):
    cliente = tables.Column(verbose_name='Cliente', orderable=False)
    nome = tables.Column(verbose_name='Nome do autorizado', orderable=False)
    opcoes = tables.TemplateColumn(template_name='autorizados/botao_acoes_autorizados.html', verbose_name='Opções', orderable=False)

    class Meta:
        model = models.ClienteUsuario
        template_name = "django_tables2/bootstrap4.html"
        attrs = {'class': 'table table-bordered table-hover'}
        fields = ('cliente', 'nome')

class FiadosTable(tables.Table):
    select = tables.CheckBoxColumn(accessor='pk', attrs={'th__input': {'id': 'select-all'}, 'td__input': {'class': 'row-select'}})
    cliente = tables.Column(verbose_name='Cliente', orderable=False)
    cliente_usuario = tables.Column(verbose_name='Autorizado do cliente', orderable=False)
    valor = tables.Column(verbose_name='Valor', orderable=False)
    datadoc = tables.DateColumn(verbose_name='Data do lançamento', orderable=False)
    is_pago = tables.BooleanColumn(verbose_name='Pago', yesno=('Sim', 'Não'), orderable=False, attrs={
            'td': {
                'class': lambda record: 'bg-success text-white' if record.is_pago else 'bg-danger text-white'
            }
        })
    opcoes = tables.TemplateColumn(template_name='fiados/botao_acoes_fiados.html', verbose_name='Opções', orderable=False)

    class Meta:
        model = models.Fiado
        template_name = "django_tables2/bootstrap4.html"
        attrs = {'class': 'table table-bordered table-hover'}
        fields = ('select', 'cliente', 'cliente_usuario', 'valor', 'datadoc', 'is_pago')

class OperadorTable(tables.Table):
    nome = tables.Column(verbose_name='Nome', orderable=False)
    opcoes = tables.TemplateColumn(template_name='operadores/botao_acoes_operadores.html', verbose_name='Opções', orderable=False)

    class Meta:
        model = models.Clientes
        template_name = "django_tables2/bootstrap4.html"
        attrs = {'class': 'table table-bordered table-hover'}
        fields = ('nome',)

class ProdutosTable(tables.Table):
    nome = tables.Column(verbose_name='Nome', orderable=False)
    valor = tables.Column(verbose_name='Valor', orderable=False)
    opcoes = tables.TemplateColumn(template_name='produtos/botao_acoes_produtos.html', verbose_name='Opções', orderable=False)
    class Meta:
        model = models.Produto
        template_name = "django_tables2/bootstrap4.html"
        attrs = {'class': 'table table-bordered table-hover'}
        fields = ('nome', 'valor')

class CaixaTable(tables.Table):
    cliente = tables.Column(verbose_name='Operador', orderable=False)
    data = tables.Column(verbose_name='Data', orderable=False)
    qtd_dinheiro = tables.Column(verbose_name='Valor em dinheiro', orderable=False)
    qtd_cd = tables.Column(verbose_name='Valor cartão de débito', orderable=False)
    qtd_cc = tables.Column(verbose_name='Valor cartão de crédito', orderable=False)
    pix = tables.Column(verbose_name='Valor em pix', orderable=False)
    valor = tables.Column(verbose_name='Valor total', orderable=False)
    opcoes = tables.TemplateColumn(template_name='caixas/botao_acoes_caixas.html', verbose_name='Opções', orderable=False)
    class Meta:
        model = models.Caixa
        template_name = "django_tables2/bootstrap4.html"
        attrs = {'class': 'table table-bordered table-hover'}
        fields = ('cliente', 'data', 'qtd_dinheiro', 'qtd_cd', 'qtd_cc', 'pix', 'valor')

class CategoriaEntradaTable(tables.Table):
    nome = tables.Column(verbose_name='Categoria', orderable=False)
    opcoes = tables.TemplateColumn(template_name='categorias/botao_acoes_categoria_entradas.html', verbose_name='Opções', orderable=False)

    class Meta:
        model = models.Categoria
        template_name = "django_tables2/bootstrap4.html"
        attrs = {'class': 'table table-bordered table-hover'}
        fields = ('nome',)

class CategoriaDespesaTable(tables.Table):
    nome = tables.Column(verbose_name='Categoria', orderable=False)
    opcoes = tables.TemplateColumn(template_name='categorias/botao_acoes_categoria_despesas.html', verbose_name='Opções', orderable=False)

    class Meta:
        model = models.Categoria
        template_name = "django_tables2/bootstrap4.html"
        attrs = {'class': 'table table-bordered table-hover'}
        fields = ('nome',)

class DespesasTable(tables.Table):
    categoria = tables.Column(verbose_name='Categoria', orderable=False)
    valor = tables.Column(verbose_name='Valor', orderable=False)
    data = tables.Column(verbose_name='Data', orderable=False)
    documento = tables.TemplateColumn(
        template_code='''
            {% if record.doc.name %}
                <a href="{{ record.doc.url }}" target="_blank" rel="noopener noreferrer">
                    Ver
                </a>
            {% else %}
                —
            {% endif %}
        ''',
        verbose_name='Documento',
        orderable=False
    )
    opcoes = tables.TemplateColumn(template_name='despesas/botao_acoes_despesas.html', verbose_name='Opções', orderable=False)

    class Meta:
        model = models.Despesas
        template_name = "django_tables2/bootstrap4.html"
        attrs = {'class': 'table table-bordered table-hover'}
        fields = ('categoria', 'valor', 'data')

class EntradasTable(tables.Table):
    categoria = tables.Column(verbose_name='Categoria', orderable=False)
    valor = tables.Column(verbose_name='Valor', orderable=False)
    data = tables.Column(verbose_name='Data', orderable=False)
    opcoes = tables.TemplateColumn(template_name='entradas/botao_acoes_entradas.html', verbose_name='Opções', orderable=False)

    class Meta:
        model = models.Entradas
        template_name = "django_tables2/bootstrap4.html"
        attrs = {'class': 'table table-bordered table-hover'}
        fields = ('categoria', 'valor', 'data')

class QtdProdutos(tables.Table):
    produto = tables.Column(verbose_name='Produto', orderable=False)
    total_qtd = tables.Column(verbose_name='Quantidade total', orderable=False)
    total_valor = tables.Column(verbose_name='Valor total', orderable=False)

    class Meta:
        template_name = "django_tables2/bootstrap4.html"
        fields = ('produto', 'total_qtd', 'total_valor')

    def render_total_valor(self, value):
        formatted = f"{value:.2f}"
        return formatted.replace('.', ',')