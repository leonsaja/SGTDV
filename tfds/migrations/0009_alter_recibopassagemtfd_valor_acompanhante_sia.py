# Generated by Django 4.2.1 on 2023-06-12 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tfds', '0008_alter_recibopassagemtfd_valor_paciente_sia'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recibopassagemtfd',
            name='valor_acompanhante_sia',
            field=models.CharField(max_length=30, null=True, verbose_name='Valor'),
        ),
    ]