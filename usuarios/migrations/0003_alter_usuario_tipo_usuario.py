# Generated by Django 4.2.1 on 2023-06-03 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_usuario_tipo_usuario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='tipo_usuario',
            field=models.CharField(default=1, max_length=1, verbose_name='Tipo de Usuario'),
            preserve_default=False,
        ),
    ]