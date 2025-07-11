# Generated by Django 4.2.7 on 2025-07-05 02:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tfds', '0003_alter_recibotfd_qta_proced_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recibotfd',
            name='atend_fora_estado',
            field=models.CharField(choices=[('1', 'SIM'), ('2', 'NÃO')], max_length=1, null=True, verbose_name='Atendimento fora do estado'),
        ),
        migrations.AlterField(
            model_name='recibotfd',
            name='qta_proced',
            field=models.PositiveBigIntegerField(blank=True, null=True, verbose_name='Quant. Procedimento'),
        ),
        migrations.AlterField(
            model_name='recibotfd',
            name='unid_assistencial',
            field=models.CharField(max_length=240, null=True, verbose_name='Unidade Assistencial'),
        ),
    ]
