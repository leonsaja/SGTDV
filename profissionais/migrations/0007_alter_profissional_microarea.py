# Generated by Django 4.1.6 on 2023-03-29 13:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('estabelecimentos', '0002_microarea_estabelecimento'),
        ('profissionais', '0006_profissional_estabelecimento_profissional_microarea_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profissional',
            name='microarea',
            field=models.ForeignKey(blank=True, help_text='Campo somente para ACS', null=True, on_delete=django.db.models.deletion.SET_NULL, to='estabelecimentos.microarea', verbose_name='Micro área'),
        ),
    ]
