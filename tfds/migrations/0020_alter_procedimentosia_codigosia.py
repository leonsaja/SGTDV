# Generated by Django 4.2.1 on 2023-10-16 00:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tfds', '0019_alter_recibopassagemtfd_codigo_sia_paciente'),
    ]

    operations = [
        migrations.AlterField(
            model_name='procedimentosia',
            name='codigosia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='procedimento_codigo', to='tfds.codigosia'),
        ),
    ]
