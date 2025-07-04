# Generated by Django 5.2 on 2025-05-09 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quermesse', '0004_alter_caixa_descricao_alter_fiado_descricao_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='despesas',
            name='datapago',
            field=models.DateField(blank=True, null=True, verbose_name='Data do pagamento'),
        ),
        migrations.AddField(
            model_name='despesas',
            name='is_pago',
            field=models.BooleanField(blank=True, default=False, verbose_name='Pago'),
        ),
    ]
