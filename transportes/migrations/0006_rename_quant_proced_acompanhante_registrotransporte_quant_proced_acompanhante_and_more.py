# Generated by Django 4.2.1 on 2023-10-10 09:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transportes', '0005_alter_registrotransporte_destino'),
    ]

    operations = [
        migrations.RenameField(
            model_name='registrotransporte',
            old_name='Quant_proced_acompanhante',
            new_name='quant_proced_acompanhante',
        ),
        migrations.RenameField(
            model_name='registrotransporte',
            old_name='Quant_proced_paciente',
            new_name='quant_proced_paciente',
        ),
    ]
