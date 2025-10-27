# sua_app/migrations/0003_migracao_dados_destino.py

from django.db import migrations
from django.db.models.functions import Upper

# --- Função de Migração de Dados (RunPython) ---
def migrar_dados_destino(apps, schema_editor):
 
    
    # 1. Obter as versões históricas dos modelos
    # IMPORTANTE: Use 'apps.get_model' e substitua 'sua_app' pelo nome real da sua app
    Viagem = apps.get_model('transportes', 'RegistroTransporte')
    Destino = apps.get_model('transportes', 'DestinoViagem')
    
    # 2. Coleta todos os destinos únicos (strings) CONVERTIDOS PARA MAIÚSCULAS
    # Isso garante que 'Rio' e 'rio' se tornem um único objeto 'RIO'.
    destinos_existentes = (
        Viagem.objects
        .annotate(destino_viagem_upper=Upper('destino'))
        .values_list('destino_viagem_upper', flat=True)
        .distinct()
    )
    
    # 3. Cria o mapa de destinos (nome_em_maiuscula -> objeto_Destino)
    destino_map = {}
    for nome_destino in destinos_existentes:
        if nome_destino:
            # get_or_create: Garante que um Destino é criado apenas se não existir
            destino_obj, created = Destino.objects.get_or_create(nome=nome_destino)
            destino_map[nome_destino] = destino_obj
            
    # 4. Mapeia a Diaria existente para o novo objeto Destino
    for viagem in Viagem.objects.all():
        # Converte o valor da diária atual para maiúsculas antes de buscar no mapa
        destino_upper = viagem.destino.upper() if viagem.destino else None
        
        if destino_upper and destino_upper in destino_map:
            viagem.destino_viagem=destino_map[destino_upper]
            viagem.save(update_fields=['destino_viagem'])


# --- Classe de Migração do Django ---
class Migration(migrations.Migration):

    # Dependências: O nome do arquivo de migração anterior (aquele que adicionou novo_destino)
    dependencies = [
        ('transportes', '0011_registrotransporte_destino_viagem'), # <-- MUDAR PARA SUA ÚLTIMA MIGRATION
    ]

    operations = [
        # Executa a função Python definida acima.
        # RunPython.noop é usado para o rollback, pois não queremos desfazer a criação de dados.
        migrations.RunPython(migrar_dados_destino, reverse_code=migrations.RunPython.noop),
    ]