# Generated by Django 4.2.1 on 2023-08-30 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tfds', '0005_remove_recibopassagemtfd_qta_passagem'),
    ]

    operations = [
        migrations.AddField(
            model_name='recibopassagemtfd',
            name='quanti_passagem_acompanhante',
            field=models.PositiveBigIntegerField(blank=True, null=True, verbose_name='Qta de Passagem'),
        ),
    ]
