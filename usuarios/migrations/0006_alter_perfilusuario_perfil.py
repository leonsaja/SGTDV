# Generated by Django 4.2.1 on 2023-12-12 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0005_remove_perfilusuario_tipo_usuario_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfilusuario',
            name='perfil',
            field=models.CharField(choices=[('1', '1-ACS'), ('2', '2-Coordenador'), ('3', '3-Digitador'), ('4', '4-Recepção'), ('5', '5-Secretario'), ('6', '6-Regulação')], max_length=1, null=True, verbose_name='Tipo de perfil'),
        ),
    ]