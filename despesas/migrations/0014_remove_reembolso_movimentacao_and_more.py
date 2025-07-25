# Generated by Django 4.2.7 on 2025-07-19 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('despesas', '0013_alter_reembolso_valor_desp_alter_reembolso_valor_mov'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reembolso',
            name='movimentacao',
        ),
        migrations.RemoveField(
            model_name='reembolso',
            name='valor_mov',
        ),
        migrations.AddField(
            model_name='reembolso',
            name='aprovado_por',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Aprovado por '),
        ),
        migrations.AddField(
            model_name='reembolso',
            name='criado_por',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Criado por '),
        ),
        migrations.AddField(
            model_name='reembolso',
            name='obs',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='OBSERVAÇÃO'),
        ),
        migrations.AddField(
            model_name='reembolso',
            name='status',
            field=models.CharField(choices=[('1', 'AGUARDANDO'), ('2', 'APROVADO'), ('3', 'REPROVADO')], default='1', max_length=1, verbose_name='Avaliar Reembolso'),
        ),
        migrations.AlterField(
            model_name='diaria',
            name='descricao',
            field=models.TextField(verbose_name='Descrição '),
        ),
    ]
