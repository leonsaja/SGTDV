# Generated by Django 4.2.1 on 2023-09-16 15:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cidadao', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReciboTFD',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('municipio_origem', models.CharField(default='Santo Antônio do Jacinto-MG', max_length=120, verbose_name='Municipio Origem')),
                ('municipio_destino', models.CharField(max_length=120, verbose_name='Municipio Destino')),
                ('data', models.DateField(verbose_name='Data')),
                ('grs', models.CharField(default='Pedra Azul-MG', max_length=50, verbose_name='GRS')),
                ('especialidade', models.CharField(max_length=100, verbose_name='Especialidade')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('acompanhante', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='recibo_acompanhante', to='cidadao.cidadao')),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='paciente', to='cidadao.cidadao')),
            ],
        ),
        migrations.CreateModel(
            name='ReciboPassagemTFD',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meio_transporte', models.CharField(choices=[('1', '1-TERRESTRE'), ('2', '2-AÉREO'), ('3', '3-OUTROS')], max_length=1, verbose_name='Meio de Transporte')),
                ('quant_passagem_paciente', models.PositiveIntegerField(verbose_name='Qta de Passagem')),
                ('quant_passagem_acompanhante', models.PositiveBigIntegerField(blank=True, null=True, verbose_name='Qta  Passagem')),
                ('trecho', models.CharField(max_length=200, verbose_name='Trecho')),
                ('codigo_sia_paciente', models.CharField(max_length=10, null=True, verbose_name='Código SIA')),
                ('codigo_sia_acompanhante', models.CharField(blank=True, max_length=10, null=True, verbose_name='Código SIA')),
                ('valor_paciente_sia', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Valor')),
                ('valor_acompanhante_sia', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name='Valor')),
                ('data_recibo', models.DateField(null=True, verbose_name='Data')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('acompanhante', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='recibo_passagem_acompanhante', to='cidadao.cidadao')),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='recibo_passagem_paciente', to='cidadao.cidadao')),
            ],
        ),
        migrations.CreateModel(
            name='CodigoSIA',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=10, verbose_name='Código SIA')),
                ('valor_unitario', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Valor Unitário')),
                ('qtd_procedimento', models.PositiveBigIntegerField(verbose_name='Quantidade')),
                ('valor_total', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Total')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('recibo_tfd', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recibo_codigo', to='tfds.recibotfd')),
            ],
        ),
    ]
