# Generated by Django 4.2.1 on 2023-06-04 18:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transportes', '0002_pacientesviagem_telefone'),
    ]

    operations = [
        migrations.AddField(
            model_name='viagem',
            name='carro',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.PROTECT, related_name='carro_viagens', to='transportes.carro'),
            preserve_default=False,
        ),
    ]
