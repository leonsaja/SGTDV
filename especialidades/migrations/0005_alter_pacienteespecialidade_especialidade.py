# Generated by Django 4.2.1 on 2023-05-28 13:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('especialidades', '0004_alter_pacienteespecialidade_especialidade'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pacienteespecialidade',
            name='especialidade',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='paciente_especialidades', to='especialidades.especialidade'),
        ),
    ]
