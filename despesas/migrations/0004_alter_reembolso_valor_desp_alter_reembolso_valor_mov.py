# Generated by Django 4.2.1 on 2023-08-12 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('despesas', '0003_alter_diaria_tipo_diaria'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reembolso',
            name='valor_desp',
            field=models.DecimalField(blank=True, decimal_places=2, default='0.00', max_digits=8, null=True, verbose_name='Valor'),
        ),
        migrations.AlterField(
            model_name='reembolso',
            name='valor_mov',
            field=models.DecimalField(blank=True, decimal_places=2, default='0.00', max_digits=8, null=True, verbose_name='Valor'),
        ),
    ]
