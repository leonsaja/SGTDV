# Generated by Django 4.2.7 on 2025-07-07 10:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transportes', '0002_rename_paciente_passageiroviagem_paciente2'),
    ]

    operations = [
        migrations.RenameField(
            model_name='passageiroviagem',
            old_name='paciente2',
            new_name='paciente',
        ),
    ]
