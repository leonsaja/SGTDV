# Generated by Django 4.2.1 on 2023-10-23 00:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('especialidades', '0004_alter_atendimentoespecialidade_especialidade_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='atendpaciente',
            old_name='Atendespecialidade',
            new_name='atendespecialidade',
        ),
    ]