# Generated by Django 4.2.1 on 2023-09-29 18:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tfds', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='codigosia',
            name='qtd_procedimento',
        ),
        migrations.RemoveField(
            model_name='codigosia',
            name='recibo_tfd',
        ),
        migrations.RemoveField(
            model_name='codigosia',
            name='valor_total',
        ),
        migrations.AddField(
            model_name='codigosia',
            name='nome_proced',
            field=models.CharField(default='', max_length=254, verbose_name='Nome do Procedimento'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='codigosia',
            name='valor_contrapartida',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name='Valor ContraPartida'),
        ),
        migrations.AlterField(
            model_name='codigosia',
            name='valor_unitario',
            field=models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Valor Unitário'),
        ),
        migrations.CreateModel(
            name='ProcedimentoSia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qtd_procedimento', models.PositiveBigIntegerField(verbose_name='Quantidade')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('codigosia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='procedimento_codigo', to='tfds.codigosia')),
                ('recibo_tfd', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='procedimento_recibo_tfd', to='tfds.recibotfd')),
            ],
        ),
    ]
