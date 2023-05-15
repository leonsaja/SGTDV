# Generated by Django 4.1.6 on 2023-04-01 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profissionais', '0011_alter_profissional_microarea'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profissional',
            name='cargo',
            field=models.CharField(choices=[('', '-----------'), ('1', 'ACS'), ('2', 'COORDENADOR(A)'), ('3', 'DIGITADOR'), ('4', 'ENFERMEIRO'), ('5', 'FAXINEIRO'), ('6', 'MÉDICO'), ('7', 'MOTORISTA'), ('8', 'RECEPCIONISTA'), ('9', 'TEC.ENFERMAGEM'), ('10', 'Outros')], default='', max_length=2, verbose_name='Cargo:'),
        ),
    ]
