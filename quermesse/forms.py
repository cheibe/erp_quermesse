from django import forms
from quermesse.models import Clientes, ClienteUsuario, Fiado, Produto, Caixa, Categoria, Despesas, Entradas, Cortesia

class ClientesForm(forms.ModelForm):
    class Meta:
        model = Clientes
        fields = [
            'nome',
            'is_cliente'
        ]

    def __init__(self, request, *args, **kwargs):
        super(ClientesForm, self).__init__(*args, **kwargs)
        del self.fields['is_cliente']

class ClientesEditForm(forms.ModelForm):
    class Meta:
        model = Clientes
        fields = [
            'nome'
        ]

class AutorizadoForm(forms.ModelForm):
    class Meta:
        model = ClienteUsuario
        fields = [
            'cliente',
            'nome'
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cliente'].queryset = Clientes.objects.filter(is_cliente=True).order_by('nome').all()

class FiadoForm(forms.ModelForm):
    class Meta:
        model = Fiado
        fields = [
            'cliente',
            'cliente_usuario',
            'valor',
            'datadoc',
            'is_pago',
            'descricao',
        ]
        widgets = {
            'datadoc': forms.widgets.DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['is_pago']
        self.fields['cliente'].queryset = Clientes.objects.filter(is_cliente=True).order_by('nome').all()
        self.fields['cliente_usuario'].queryset = ClienteUsuario.objects.order_by('nome').all()

class FiadoEditForm(forms.ModelForm):
    class Meta:
        model = Fiado
        fields = [
            'cliente',
            'cliente_usuario',
            'valor',
            'datadoc',
            'datapago',
            'is_pago',
            'descricao',
        ]
        widgets = {
            'datadoc': forms.widgets.DateInput(attrs={'type': 'date'}),
            'datapago': forms.widgets.DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cliente'].queryset = Clientes.objects.filter(is_cliente=True).order_by('nome').all()
        self.fields['cliente_usuario'].queryset = ClienteUsuario.objects.order_by('nome').all()

class FindFiadoForm(forms.ModelForm):
    is_pago = forms.NullBooleanField(
        required=False,
        widget=forms.NullBooleanSelect(),
        label='Pago'
    )
    class Meta:
        model = Fiado
        fields = [
            'cliente',
            'datadoc',
            'datapago',
            'is_pago'
        ]
        widgets = {
            'datadoc': forms.widgets.DateInput(attrs={'type': 'date'}),
            'datapago': forms.widgets.DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cliente'].queryset = Clientes.objects.filter(is_cliente=True).order_by('nome').all()
        self.fields['is_pago'].widget.choices = [
            (None, '— todos —'),
            (True, 'Sim'),
            (False, 'Não'),
        ]

class OperadoresForm(forms.ModelForm):
    class Meta:
        model = Clientes
        fields = [
            'nome',
            'is_caixa'
        ]

    def __init__(self, request, *args, **kwargs):
        super(OperadoresForm, self).__init__(*args, **kwargs)
        del self.fields['is_caixa']

class OperadoresEditForm(forms.ModelForm):
    class Meta:
        model = Clientes
        fields = [
            'nome'
        ]

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = [
            'nome',
            'valor',
            'descricao'
        ]

class CaixaForm(forms.ModelForm):
    class Meta:
        model = Caixa
        fields = [
            'cliente',
            'valor',
            'data',
            'descricao',
            'qtd_dinheiro',
            'qtd_cd',
            'qtd_cc',
            'pix',
            'reimpressao'
        ]
        widgets = {
            'data': forms.widgets.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cliente'].queryset = Clientes.objects.filter(is_caixa=True).order_by('nome').all()

class CaixaFindForm(forms.ModelForm):
    class Meta:
        model = Caixa
        fields = [
            'cliente',
            'data'
        ]
        widgets = {
            'data': forms.widgets.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cliente'].queryset = Clientes.objects.filter(is_caixa=True).order_by('nome').all()

class CortesiaForm(forms.ModelForm):
    class Meta:
        model = Cortesia
        fields = [
            'data'
        ]
        widgets = {
            'data': forms.widgets.DateInput(attrs={'type': 'date'}),
        }

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = [
            'nome',
            'is_despesa',
            'is_entrada'
        ]
    
    def __init__(self, request, *args, **kwargs):
        super(CategoriaForm, self).__init__(*args, **kwargs)
        if 'is_despesa' in self.fields:
            del self.fields['is_despesa']
        if 'is_entrada' in self.fields:
            del self.fields['is_entrada']

class CategoriaEditForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = [
            'nome'
        ]

class DespesasForm(forms.ModelForm):
    class Meta:
        model = Despesas
        fields = [
            'categoria',
            'valor',
            'data',
            'is_pago',
            'datapago',
            'descricao',
            'doc'
        ]
        widgets = {
            'data': forms.widgets.DateInput(attrs={'type': 'date'}),
            'datapago': forms.widgets.DateInput(attrs={'type': 'date'}),
            'is_pago': forms.widgets.CheckboxInput()
        }
        helpe_texts = {
            'doc': 'Tipo de arquivos: .PDF/.JPG/.JPEG/.PNG'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categoria'].queryset = Categoria.objects.filter(is_despesa=True).order_by('nome').all()

class DespesasFindForm(forms.ModelForm):
    class Meta:
        model = Despesas
        fields = [
            'categoria',
            'data',
            'datapago',
            'is_pago',
        ]
        widgets = {
            'data': forms.widgets.DateInput(attrs={'type': 'date'}),
            'datapago': forms.widgets.DateInput(attrs={'type': 'date'}),
            'is_pago': forms.widgets.Select()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categoria'].queryset = Categoria.objects.filter(is_despesa=True).order_by('nome').all()
        self.fields['is_pago'].widget.choices = [
            (None, '- Todos -'),
            (True, 'Sim'),
            (False, 'Não'),
        ]

class EntradasForm(forms.ModelForm):
    class Meta:
        model = Entradas
        fields = [
            'categoria',
            'valor',
            'data',
            'descricao'
        ]
        widgets = {
            'data': forms.widgets.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['categoria'].queryset = Categoria.objects.filter(is_entrada=True).order_by('nome').all()

class EntradasFindForm(forms.ModelForm):
    class Meta:
        model = Despesas
        fields = [
            'categoria',
            'data'
        ]
        widgets = {
            'data': forms.widgets.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categoria'].queryset = Categoria.objects.filter(is_entrada=True).order_by('nome').all()