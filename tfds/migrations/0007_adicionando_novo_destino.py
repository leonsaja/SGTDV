from django.db import migrations
from django.db.models.functions import Upper

def popular_destino_viagem(apps, schema_editor):
    # Carrega os modelos no estado em que se encontravam na época desta migração
    ReciboTFD = apps.get_model('tfds', 'ReciboTFD')
    DestinoViagem = apps.get_model('transportes', 'DestinoViagem')

    # 1. Encontra todos os nomes de municípios de destino únicos do ReciboTFD
    nomes_destino_originais = ReciboTFD.objects.annotate(municipio_destino_upper=Upper('municipio_destino')).values_list('municipio_destino_upper', flat=True).distinct()


    # Mapeamento para armazenar os objetos DestinoViagem já criados/existentes
    # A chave do dicionário ainda é o nome ORIGINAL (como está no ReciboTFD)
    # e o valor é o objeto DestinoViagem criado/obtido (com o nome em MAIÚSCULAS)
    objetos_destino = {}
    
    # 2. Cria ou Obtém (get_or_create) o DestinoViagem para cada nome
    for nome_original in nomes_destino_originais:
       
        if nome_original:
            
            destino, created = DestinoViagem.objects.get_or_create(
                nome=nome_original
            )
            objetos_destino[nome_original] = destino

    # 3. Associa o DestinoViagem correspondente a cada ReciboTFD
    for recibo in ReciboTFD.objects.all():
        destino_upper = recibo.municipio_destino.strip().upper() if recibo.municipio_destino else None
        
        if destino_upper and destino_upper in objetos_destino:
            recibo.destino_viagem = objetos_destino[destino_upper]
            recibo.save(update_fields=['destino_viagem'])
            


# --- Classe de Migração do Django ---
class Migration(migrations.Migration):

    # Dependências: O nome do arquivo de migração anterior (aquele que adicionou novo_destino)
    dependencies = [
        ('tfds', '0006_recibotfd_destino_viagem'), 

    ]
    operations = [
        # Executa a função Python definida acima.
        # RunPython.noop é usado para o rollback, pois não queremos desfazer a criação de dados.
        migrations.RunPython(popular_destino_viagem, reverse_code=migrations.RunPython.noop),
    ]