# Generated by Django 4.2.7 on 2025-06-23 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('despesas', '0008_rename_aprovado_diaria_diaria_aprovado_por_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reembolso',
            name='valor_desp',
            field=models.DecimalField(decimal_places=2, default='', max_digits=8, null=True, verbose_name='Valor'),
        ),
    ]
