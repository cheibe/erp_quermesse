from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.conf import settings
from django.core.validators import FileExtensionValidator

class QuermesseUserCuston(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_picture/', blank=True, null=True)

class Clientes(models.Model):
    nome = models.CharField(verbose_name='Nome', max_length=40)
    is_cliente = models.BooleanField(blank=True, null=True)
    is_caixa = models.BooleanField(blank=True, null=True)
    create_user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Criado por', on_delete=models.PROTECT, related_name='cliente_user_create', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    assign_user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Modificado por', on_delete=models.PROTECT, related_name='cliente_user_assign', blank=True, null=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome

class ClienteUsuario(models.Model):
    cliente = models.ForeignKey(Clientes, verbose_name='Cliente', on_delete=models.PROTECT)
    nome = models.CharField(verbose_name='Nome', max_length=40)
    create_user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Criado por', on_delete=models.PROTECT, related_name='clienteUsuario_user_create', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    assign_user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Modificado por', on_delete=models.PROTECT, related_name='clienteUsuario_user_assign', blank=True, null=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome

class Fiado(models.Model):
    cliente = models.ForeignKey(Clientes, verbose_name='Clientes', on_delete=models.PROTECT)
    cliente_usuario = models.ForeignKey(ClienteUsuario, verbose_name='Cliente usuario', on_delete=models.PROTECT, blank=True, null=True)
    valor = models.DecimalField(verbose_name='Valor', decimal_places=2, max_digits=20)
    datadoc = models.DateField(verbose_name='Data do lançamento')
    datapago = models.DateField(verbose_name='Data do pagamento', blank=True, null=True)
    is_pago = models.BooleanField(blank=True, null=True, verbose_name='Pago')
    descricao = models.CharField(verbose_name='Descrição', blank=True, null=True, max_length=250)
    create_user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Criado por', on_delete=models.PROTECT, related_name='clienteFiado_user_create', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    assign_user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Modificado por', on_delete=models.PROTECT, related_name='clienteFiado_user_assign', blank=True, null=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.cliente.nome

class Produto(models.Model):
    nome = models.CharField(verbose_name='Nome', max_length=40)
    valor = models.DecimalField(verbose_name='Valor', decimal_places=2, max_digits=20)
    descricao = models.CharField(verbose_name='Descrição', blank=True, null=True, max_length=100)
    create_user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Criado por', on_delete=models.PROTECT, related_name='clienteProduto_user_create', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    assign_user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Modificado por', on_delete=models.PROTECT, related_name='clienteProduto_user_assign', blank=True, null=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome

class Caixa(models.Model):
    cliente = models.ForeignKey(Clientes, on_delete=models.PROTECT, verbose_name='Operador', db_index=True)
    valor = models.DecimalField(verbose_name='Valor total', decimal_places=2, max_digits=20)
    data = models.DateField(verbose_name='Data de operação')
    descricao = models.CharField(verbose_name='Descrição', blank=True, null=True, max_length=250)
    qtd_dinheiro = models.DecimalField(verbose_name='Valor em Dinheiro', decimal_places=2, max_digits=20)
    qtd_cd = models.DecimalField(verbose_name='Valor em cartão de débito', decimal_places=2, max_digits=20)
    qtd_cc = models.DecimalField(verbose_name='Valor em cartão de crédito', decimal_places=2, max_digits=20)
    pix = models.DecimalField(verbose_name='Pix', decimal_places=2, max_digits=20)
    reimpressao = models.DecimalField(verbose_name='Reimpressão', decimal_places=2, max_digits=15, blank=True, default=0.00)
    produtos = models.ManyToManyField(Produto, through='ItemCaixa', related_name='caixas')
    create_user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Criado por', on_delete=models.PROTECT, related_name='clienteCaixa_user_create', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    assign_user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Modificado por', on_delete=models.PROTECT, related_name='clienteCaixa_user_assign', blank=True, null=True)
    modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['cliente'])
        ]

    def __str__(self):
        return self.cliente.nome

class ItemCaixa(models.Model):
    caixa = models.ForeignKey(Caixa, on_delete=models.CASCADE, verbose_name='Caixa')
    produtos = models.ForeignKey(Produto, on_delete=models.CASCADE, verbose_name='Produtos')
    quantidade = models.PositiveIntegerField(verbose_name='Quantidade')
    
    class Meta:
        unique_together = ('caixa', 'produtos')

    def __str__(self):
        return self.produtos.nome
    
class Categoria(models.Model):
    nome = models.CharField(verbose_name='Nome', max_length=100)
    is_despesa = models.BooleanField(verbose_name='Categoria', blank=True)
    is_entrada = models.BooleanField(verbose_name='Entradas', blank=True)
    create_user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Criado por', on_delete=models.PROTECT, related_name='categoria_user_create', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    assign_user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Modificado por', on_delete=models.PROTECT, related_name='categoria_user_assign', blank=True, null=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome

class Despesas(models.Model):
    categoria = models.ForeignKey(Categoria, verbose_name='Categoria', on_delete=models.PROTECT)
    valor = models.DecimalField(verbose_name='Valor', decimal_places=2, max_digits=25)
    data = models.DateField(verbose_name='Data da operação')
    is_pago = models.BooleanField(verbose_name='Pago', blank=True, default=False)
    datapago = models.DateField('Data do pagamento', blank=True, null=True)
    descricao = models.CharField(verbose_name='Descrição', max_length=250, blank=True, null=True)
    doc = models.FileField(verbose_name='Nota', upload_to='doc_despesas/', blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'])])
    create_user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Criado por', on_delete=models.PROTECT, related_name='despesa_user_create', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    assign_user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Modificado por', on_delete=models.PROTECT, related_name='despesa_user_assign', blank=True, null=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.categoria.nome

class Entradas(models.Model):
    categoria = models.ForeignKey(Categoria, verbose_name='Categoria', on_delete=models.PROTECT)
    valor = models.DecimalField(verbose_name='Valor', decimal_places=2, max_digits=25)
    data = models.DateField(verbose_name='Data da operação')
    descricao = models.CharField(verbose_name='Descrição', max_length=250, blank=True, null=True)
    create_user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Criado por', on_delete=models.PROTECT, related_name='entrada_user_create', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    assign_user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Modificado por', on_delete=models.PROTECT, related_name='entrada_user_assign', blank=True, null=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.categoria.nome