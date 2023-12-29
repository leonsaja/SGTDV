# Generated by Django 4.2.7 on 2023-12-27 10:29

from django.db import migrations
import localflavor.br.models


class Migration(migrations.Migration):

    dependencies = [
        ('cidadao', '0002_alter_cidadao_microarea'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cidadao',
            name='cpf',
            field=localflavor.br.models.BRCPFField(blank=True, error_messages='Já existe cidadao com esse CPF informado', max_length=14, null=True, unique=True, verbose_name='CPF'),
        ),
    ]
