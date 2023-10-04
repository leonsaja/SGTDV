# Generated by Django 4.2.1 on 2023-09-30 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tfds', '0003_codigosia_valor_total_alter_codigosia_codigo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='codigosia',
            name='codigo',
            field=models.CharField(max_length=10, unique=True, verbose_name='Código'),
        ),
        migrations.AlterField(
            model_name='codigosia',
            name='valor_contrapartida',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name='Contra Partida'),
        ),
    ]
