# Generated by Django 4.2.1 on 2023-09-11 01:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('estabelecimentos', '0002_alter_estabelecimento_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='microarea',
            options={'ordering': ['microarea']},
        ),
    ]
