# Generated by Django 4.2.1 on 2023-06-10 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tfds', '0002_recibopassagemtfd_data_recibo_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recibopassagemtfd',
            name='codigosia',
        ),
        migrations.RemoveField(
            model_name='recibopassagemtfd',
            name='valor_unitario',
        ),
        migrations.AddField(
            model_name='recibopassagemtfd',
            name='codigo_sia_acompanhante',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Código SIA do Acompanhante'),
        ),
        migrations.AddField(
            model_name='recibopassagemtfd',
            name='codigo_sia_paciente',
            field=models.CharField(max_length=10, null=True, verbose_name='Código SIA do Paciente'),
        ),
        migrations.AddField(
            model_name='recibopassagemtfd',
            name='valor_acompanhante_sia',
            field=models.DecimalField(decimal_places=2, max_digits=6, null=True, verbose_name='Valor Unitário Acompanhante'),
        ),
        migrations.AddField(
            model_name='recibopassagemtfd',
            name='valor_paciente_sia',
            field=models.DecimalField(decimal_places=2, max_digits=6, null=True, verbose_name='Valor Unitário Paciente'),
        ),
    ]
