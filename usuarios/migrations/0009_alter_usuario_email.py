# Generated by Django 4.2.1 on 2023-06-04 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0008_alter_usuario_tipo_usuario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='E-mail'),
        ),
    ]