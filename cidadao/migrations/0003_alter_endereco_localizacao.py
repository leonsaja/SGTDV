# Generated by Django 4.2.7 on 2025-07-15 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cidadao', '0002_alter_cidadao_rg'),
    ]

    operations = [
        migrations.AlterField(
            model_name='endereco',
            name='localizacao',
            field=models.CharField(choices=[('1', '---'), ('2', 'Urbana'), ('3', 'Rural')], default='', max_length=1, null=True, verbose_name='LOCALIZAÇÃO'),
        ),
    ]
