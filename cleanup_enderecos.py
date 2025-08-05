# cleanup_enderecos.py

import os
import django

# Substitua 'seu_projeto.settings' pelo nome do seu projeto e do seu arquivo de settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sgtdv.settings')
django.setup()

# Importe os modelos após a configuração do ambiente
from django.db.models import ObjectDoesNotExist
from cidadao.models import Cidadao, Endereco

# ---

# Obtenha todos os cidadaos
todos_cidadaos = Cidadao.objects.all()

print(f"Total de cidadaos encontrados: {todos_cidadaos.count()}\n")

# Itere sobre cada cidadao
for cidadao in todos_cidadaos:
    print('paciente',cidadao)
    try:
        # Acessa todos os endereços do cidadao
        enderecos_do_cidadao = cidadao.endereco_cidadao.all()
        print('teste10000')
        # Verifica se o cidadao tem mais de um endereço
        if enderecos_do_cidadao.count() > 1:
            print('teste20000')
            # Pega o segundo endereço da lista (índice 1)
            segundo_endereco = enderecos_do_cidadao[1]
            
            print(f"cidadao: {cidadao.nome_completo} (ID: {cidadao.id}) - Encontrado mais de um endereço.")
            print(f"    - Endereço a ser excluído: {segundo_endereco.logradouro}")
            
            # Exclui o segundo endereço do banco de dados
            segundo_endereco.delete()
            
            print("    - Endereço excluído com sucesso.\n")
            
        else:
            print(f"cidadao: {cidadao.nome_completo} (ID: {cidadao.id}) - Tem apenas um ou nenhum endereço. Nada para excluir.\n")
            
    except ObjectDoesNotExist:
        print(f"Erro: cidadao {cidadao.id} não encontrado, mas a consulta falhou. Continuar...\n")

print("Processo concluído.")