# Generated by Django 4.1.6 on 2023-04-17 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cidadao', '0003_alter_cidadao_cns'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cidadao',
            name='cns',
            field=models.PositiveBigIntegerField(help_text='Digite o cartão do SUS com 15 digitos.', unique=True, verbose_name='CNS'),
        ),
    ]
