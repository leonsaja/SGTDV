# sua_app/migrations/0003_migracao_dados_destino.py

from django.db import migrations
from django.db.models.functions import Upper

# --- Função de Migração de Dados (RunPython) ---
def migrar_dados_destino(apps, schema_editor):
    """
    Cria objetos Destino únicos e mapeia o campo CharField (viagem_dest)
    para o novo campo ForeignKey (novo_destino).
    """
    
    # 1. Obter as versões históricas dos modelos
    # IMPORTANTE: Use 'apps.get_model' e substitua 'sua_app' pelo nome real da sua app
    Diaria = apps.get_model('despesas', 'Diaria')
    Destino = apps.get_model('transportes', 'DestinoViagem')
    
    # 2. Coleta todos os destinos únicos (strings) CONVERTIDOS PARA MAIÚSCULAS
    # Isso garante que 'Rio' e 'rio' se tornem um único objeto 'RIO'.
    destinos_existentes = (
        Diaria.objects
        .annotate(viagem_dest_upper=Upper('viagem_dest'))
        .values_list('viagem_dest_upper', flat=True)
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
    for diaria in Diaria.objects.all():
        # Converte o valor da diária atual para maiúsculas antes de buscar no mapa
        destino_upper = diaria.viagem_dest.upper() if diaria.viagem_dest else None
        
        if destino_upper and destino_upper in destino_map:
            diaria.novo_destino =destino_map[destino_upper]
            diaria.save()

# --- Classe de Migração do Django ---
class Migration(migrations.Migration):

    # Dependências: O nome do arquivo de migração anterior (aquele que adicionou novo_destino)
    dependencies = [
        ('despesas', '0007_diaria_novo_destino'), # <-- MUDAR PARA SUA ÚLTIMA MIGRATION
    ]

    operations = [
        # Executa a função Python definida acima.
        # RunPython.noop é usado para o rollback, pois não queremos desfazer a criação de dados.
        migrations.RunPython(migrar_dados_destino, reverse_code=migrations.RunPython.noop),
    ]