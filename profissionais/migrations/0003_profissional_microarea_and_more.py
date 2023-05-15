# Generated by Django 4.1.6 on 2023-03-29 09:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('estabelecimentos', '0001_initial'),
        ('profissionais', '0002_profissional_estabelecimento'),
    ]

    operations = [
        migrations.AddField(
            model_name='profissional',
            name='microarea',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='estabelecimentos.microarea', verbose_name='Micro área'),
        ),
        migrations.AlterField(
            model_name='profissional',
            name='estabelecimento',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='estabelecimentos.estabelecimento', verbose_name='Estabelecimento'),
        ),
    ]
