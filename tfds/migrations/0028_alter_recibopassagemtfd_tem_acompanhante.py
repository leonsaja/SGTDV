# Generated by Django 4.2.7 on 2023-12-28 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tfds', '0027_recibopassagemtfd_criado_por_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recibopassagemtfd',
            name='tem_acompanhante',
            field=models.CharField(choices=[('1', 'SIM'), ('2', 'NÃO')], max_length=1, verbose_name='Tem Acompanhante'),
        ),
    ]
