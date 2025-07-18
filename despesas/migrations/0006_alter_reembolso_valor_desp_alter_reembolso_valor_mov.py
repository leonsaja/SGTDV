# Generated by Django 4.2.7 on 2025-07-16 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('despesas', '0005_reembolso_descricao_reembolso'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reembolso',
            name='valor_desp',
            field=models.DecimalField(decimal_places=2, max_digits=8, null=True, verbose_name='Valor'),
        ),
        migrations.AlterField(
            model_name='reembolso',
            name='valor_mov',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name='Valor'),
        ),
    ]
