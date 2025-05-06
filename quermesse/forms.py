from django import forms
from quermesse.models import Clientes, ClienteUsuario, Fiado, Produto, Caixa

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

class FiadoForm(forms.ModelForm):
    class Meta:
        model = Fiado
        fields = [
            'cliente',
            'cliente_usuario',
            'valor',
            'datadoc',
            'descricao',
        ]
        widgets = {
            'datadoc': forms.widgets.DateInput(attrs={'type': 'date'})
        }

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

class FindFiadoForm(forms.ModelForm):
    class Meta:
        model = Fiado
        fields = [
            'cliente',
            'datadoc',
            'datapago',
        ]
        widgets = {
            'datadoc': forms.widgets.DateInput(attrs={'type': 'date'}),
            'datapago': forms.widgets.DateInput(attrs={'type': 'date'})
        }

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
        ]
        widgets = {
            'data': forms.widgets.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cliente'].queryset = Clientes.objects.filter(is_caixa=True)

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
        self.fields['cliente'].queryset = Clientes.objects.filter(is_caixa=True)