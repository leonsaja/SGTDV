# Generated by Django 4.2.1 on 2023-06-04 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transportes', '0004_passageiroviagem_viagem_motorista_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passageiroviagem',
            name='acompanhante',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Acompanhante'),
        ),
        migrations.AlterField(
            model_name='passageiroviagem',
            name='paciente',
            field=models.CharField(max_length=255, verbose_name='Nome do Paciente'),
        ),
    ]
