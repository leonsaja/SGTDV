# Generated by Django 4.1.6 on 2023-04-15 14:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('despesas', '0011_alter_reembolso_diaria'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reembolso',
            name='diaria',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reembolsos', to='despesas.diaria'),
        ),
    ]
