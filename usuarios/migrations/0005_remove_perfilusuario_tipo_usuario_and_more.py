# Generated by Django 4.2.1 on 2023-12-12 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0004_perfilusuario_remove_usuario_tipo_usuario_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='perfilusuario',
            name='tipo_usuario',
        ),
        migrations.AddField(
            model_name='perfilusuario',
            name='perfil',
            field=models.CharField(choices=[('1', '1-ACS'), ('2', '2-Coordenação'), ('3', '3-Digitador'), ('4', '4-Recepção'), ('5', '5-Secretario'), ('6', '6-Regulação')], max_length=1, null=True, verbose_name='Tipo de perfil'),
        ),
    ]
