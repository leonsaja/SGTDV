# Generated by Django 4.2.1 on 2023-05-22 00:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profissionais', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profissional',
            name='cargo',
            field=models.CharField(choices=[('', '-----------'), ('1', 'ACS'), ('2', 'COORDENADOR(A)'), ('3', 'DIGITADOR'), ('4', 'ENFERMEIRO'), ('5', 'FAXINEIRO'), ('6', 'MÉDICO'), ('7', 'MOTORISTA'), ('8', 'RECEPCIONISTA'), ('9', 'TEC.ENFERMAGEM'), ('10', 'DENTISTA'), ('11', 'Outros')], default='', max_length=2, verbose_name='Cargo:'),
        ),
    ]
