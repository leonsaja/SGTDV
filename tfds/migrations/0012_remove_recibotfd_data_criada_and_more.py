# Generated by Django 4.2.1 on 2023-06-25 15:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tfds', '0011_alter_recibopassagemtfd_codigo_sia_paciente'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recibotfd',
            name='data_criada',
        ),
        migrations.RemoveField(
            model_name='recibotfd',
            name='data_editada',
        ),
    ]
