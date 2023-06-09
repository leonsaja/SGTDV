# Generated by Django 4.2.1 on 2023-06-10 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tfds', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recibopassagemtfd',
            name='data_recibo',
            field=models.DateField(null=True, verbose_name='Data'),
        ),
        migrations.AddField(
            model_name='recibopassagemtfd',
            name='valor_unitario',
            field=models.DecimalField(decimal_places=2, max_digits=6, null=True, verbose_name='Valor Unitário'),
        ),
        migrations.AlterField(
            model_name='recibopassagemtfd',
            name='meio_transporte',
            field=models.CharField(choices=[('1', '1-TERRESTRE'), ('2', '2-AÉREO'), ('3', '3-OUTROS')], max_length=1, verbose_name='Meio de Transporte'),
        ),
    ]
