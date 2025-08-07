from django.contrib import messages
from django.db.models import ProtectedError, Q
from dal import autocomplete
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import DetailView, ListView,CreateView, UpdateView
import pandas as pd
from cidadao.forms.cidadao_form import CidadaoForm, EnderecoForm
from cidadao.forms.dados import ImportarDadosForm
from cidadao.models import Cidadao, Endereco
from django.contrib.messages import constants
from django.contrib import messages
from rolepermissions.decorators import has_role_decorator
from rolepermissions.mixins import HasRoleMixin
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from estabelecimentos.models import MicroArea


class CidadaoCreateView(SuccessMessageMixin,HasRoleMixin,CreateView):
    model = Cidadao
    form_class = CidadaoForm
    template_name = 'cidadao/form_cidadao.html'
    success_url = reverse_lazy('cidadao:list-cidadao')
    success_message='Cadastro realizado com sucesso'
    allowed_roles=['acs','recepcao','regulacao']
    success_message='Cadastro realizado com sucesso'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['endereco'] = EnderecoForm(self.request.POST)
        else:
            context['endereco'] = EnderecoForm()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        form_endereco = context['endereco']

        if form_endereco.is_valid():
            self.object = form.save()  
            form_endereco.instance.cidadao = self.object 
            form_endereco.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        context = self.get_context_data()
        return self.render_to_response(context)

class CidadaoUpdateView(SuccessMessageMixin,HasRoleMixin,UpdateView):
    model = Cidadao
    form_class = CidadaoForm
    template_name = 'cidadao/form_cidadao.html' 
    success_url = reverse_lazy('cidadao:list-cidadao')
    allowed_roles=['acs','recepcao','regulacao']
    success_message='Dados atualizados com sucesso'

    def get_object(self, queryset=None):
        return get_object_or_404(Cidadao, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cidadao_instance = self.object
        try:
            endereco_instance = Endereco.objects.get(cidadao=cidadao_instance)
        except Endereco.DoesNotExist:
            endereco_instance = Endereco(cidadao=cidadao_instance) # Cria uma nova instância se não existir

        if self.request.POST:
            context['endereco'] = EnderecoForm(self.request.POST, instance=endereco_instance)
        else:
            context['endereco'] = EnderecoForm(instance=endereco_instance)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        form_endereco = context['endereco']

        if form_endereco.is_valid():
            self.object = form.save()
            form_endereco.instance.cidadao = self.object
            form_endereco.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        context = self.get_context_data()
        return self.render_to_response(context)

class CidadaoDetailView(HasRoleMixin,DetailView):
    model=Cidadao
    template_name='cidadao/detail_cidadao.html'
    allowed_roles = ['acs','coordenador','regulacao','recepcao']

    def get_context_data(self, *args, **kwargs):
        context=super().get_context_data(*args, **kwargs)
        context['paciente']=Cidadao.objects.select_related('microarea').get(pk=self.kwargs['pk'])
        try:
            context['endereco']=Endereco.objects.select_related('cidadao').get(cidadao=context['paciente'])
        except Endereco.DoesNotExist:
            context['endereco']=Endereco(cidadao=context['paciente'])
        return context

class CidadaoListView(HasRoleMixin,ListView):
    model=Cidadao
    template_name='cidadao/list_cidadao.html'
    context_object_name='pacientes'
    paginate_by=15
    allowed_roles = ['acs','coordenador','regulacao','recepcao']
   
class CidadaoSearchListView(HasRoleMixin,ListView):
    
    model=Cidadao
    template_name='cidadao/list_cidadao.html'
    context_object_name='pacientes'
    paginate_by=10
    allowed_roles = ['acs','coordenador','regulacao','recepcao']
   
    def get_queryset(self, *args, **kwargs):
        qs = super(CidadaoSearchListView,self).get_queryset(*args, **kwargs)

        search_nome_cpf_cns=self.request.GET.get('search_nome_cpf',None).rstrip()
        search_nome_mae=self.request.GET.get('search_nome_mae',None).rstrip()
        search_dt_nascimento=self.request.GET.get('search_dt_nascimento',None)
      
        if search_nome_cpf_cns:
            qs=qs.select_related('microarea').filter(Q(nome_completo__iregex=search_nome_cpf_cns)| Q(cpf__icontains=search_nome_cpf_cns)|Q(cns__icontains=search_nome_cpf_cns))
              
        if search_nome_mae:
            qs=qs.select_related('microarea').filter(nome_mae__icontains=search_nome_mae)
        
        if search_dt_nascimento:
            qs=qs.select_related('microarea').filter(dt_nascimento__iexact=search_dt_nascimento)

        return qs

"""

def importar_dados_excel(request):
    
    template_name='cidadao/importar_dados.html'

   
    if request.method == 'POST':
        form = ImportarDadosForm(request.POST, request.FILES)
        if form.is_valid():
            arquivo_excel = request.FILES['arquivo']
            df = pd.read_excel(arquivo_excel,dtype={'CPF': str})
    
            for index, row in df.iterrows():
                # Prepara os dados de forma limpa e segura
                
                cod_logradouro_map = {
                'RUA': '2',
                'FAZENDA': '3',
                'PRACA': '4',
                'PRAÇA': '4', 
                'TRAVESSA': '5',
                'SÍTIO':'6',
                }
                cod_logradouro_excel = str(row.get('TIPO LOGRADOURO', '')).upper()
                cod_logradouro = cod_logradouro_map.get(cod_logradouro_excel, '1') # '1' pode ser para 'OUTROS' ou padrão
                
                
                cod_localizacao_map = {
                'URBANA': '2',
                'RURAL': '3',
                
                }
                cod_logalizacao_excel = str(row.get('TIPO LOCALIZAÇÃO', '')).upper()
                cod_localizacao = cod_localizacao_map.get(cod_logalizacao_excel, '1') # '1' pode ser para 'OUTROS' ou padrão


                sexo_excel = str(row.get('SEXO', '')).upper()

                sexo_map = {'F': 'F', 'M': 'M'}


                sexo_final = sexo_map.get(sexo_excel, 'M')
                
                print('CPF',row.get('CPF'))
                
                microare=MicroArea.objects.get(microarea=str(row.get('MA')).strip())
                
                dados_cidadao = {
                    'cpf': row.get('CPF'),
                    'nome_completo': str(row.get('NOME CIDADAO')).strip() if pd.notna(row.get('NOME CIDADAO')) else None,
                    'sexo':sexo_final,
                    'dt_nascimento': row.get('DATA NASCIMENTO'),
                    'nome_mae': str(row.get('NOME DA MAE')).strip() if pd.notna(row.get('NOME DA MAE')) else None,
                    'nome_pai':row.get('NOME DO PAI'),
                    'nacionalidade': str(row.get('MUNIC. NASCIMENTO')).strip() if pd.notna(row.get('MUNIC. NASCIMENTO')) else None,
                    'microarea': microare,
                    'telefone1':str(row.get('CONTATO')).strip()
                }

                dados_endereco = {
                    'cod_logradouro': cod_logradouro,
                    'logradouro':str(row.get('LOGRADOURO')).strip(),
                    'numero': str(row.get('N')).strip(),
                    'complemento':str(row.get('COMPLEMENTO')).strip(),
                    'bairro': str(row.get('BAIRRO')).strip(),
                    'cidade': 'SANTO ANTÔNIO DO JACINTO',
                    'estado': 'MG',
                    'cep': '39935-000',
                    'localizacao':cod_localizacao,
                }

                cidadao = None
                
                # Limpar os dados para evitar problemas na busca
                dados_cidadao = {k: v for k, v in dados_cidadao.items() if v is not None}
                dados_endereco = {k: v for k, v in dados_endereco.items() if v is not None}

        
                if dados_cidadao.get('cpf'):
                    try:
                        cidadao = Cidadao.objects.get(cpf=dados_cidadao['cpf'])
                        print(f"Cidadão encontrado por CPF: {cidadao.cpf}. Atualizando...")
                    except Cidadao.DoesNotExist:
                        pass
                    
                        
                # 3. Se um cidadão foi encontrado, atualiza os dados
                if cidadao:
                    for chave, valor in dados_cidadao.items():
                        setattr(cidadao, chave, valor)
                    cidadao.save()
                    print(f"Dados do cidadão '{cidadao.nome_completo}' atualizados.")
                else:
                    # 4. Se não encontrou, cria um novo registro de cidadão
                    cidadao = Cidadao.objects.create(**dados_cidadao)
                    print(f"Novo cidadão '{cidadao.nome_completo}' criado.")

                # 5. Lógica para encontrar ou criar o endereço, associado ao cidadão
                if dados_endereco:
                    busca_endereco = {'cidadao': cidadao, **dados_endereco}
                    try:
                        endereco = Endereco.objects.get(**busca_endereco)
                        # Se o endereço já existe para esse cidadão, apenas o atualiza
                        for chave, valor in dados_endereco.items():
                            setattr(endereco, chave, valor)
                        endereco.save()
                        print(f"Endereço para '{cidadao.nome_completo}' atualizado.")
                    except Endereco.DoesNotExist:
                        # Se não existe, cria um novo
                        Endereco.objects.create(**busca_endereco)
                        print(f"Novo endereço criado para '{cidadao.nome_completo}'.")
            
            return redirect('cidadao:list-cidadao')
        else: 
            form=ImportarDadosForm(ImportarDadosForm(request.POST or None, request.FILES))
    else:
        
        form=ImportarDadosForm()
                    
        return render(request,template_name, {'form': form}) 
    """
"""
def importar_dados_excel(request):
    
    template_name='cidadao/importar_dados.html'

   
    if request.method == 'POST':
        form = ImportarDadosForm(request.POST, request.FILES)
        if form.is_valid():
            arquivo_excel = request.FILES['arquivo']
            df = pd.read_excel(arquivo_excel,dtype={'CPF': str})
    
            for index, row in df.iterrows():
                # Prepara os dados de forma limpa e segura
                
                cod_logradouro_map = {
                'RUA': '2',
                'FAZENDA': '3',
                'PRACA': '4',
                'PRAÇA': '4', 
                'TRAVESSA': '5',
                'SÍTIO':'6',
                }
                cod_logradouro_excel = str(row.get('TIPO LOGRADOURO', '')).upper()
                cod_logradouro = cod_logradouro_map.get(cod_logradouro_excel, '1') # '1' pode ser para 'OUTROS' ou padrão
                
                
                cod_localizacao_map = {
                'URBANA': '2',
                'RURAL': '3',
                
                }
                cod_logalizacao_excel = str(row.get('TIPO LOCALIZAÇÃO', '')).upper()
                cod_localizacao = cod_localizacao_map.get(cod_logalizacao_excel, '1') # '1' pode ser para 'OUTROS' ou padrão


                sexo_excel = str(row.get('SEXO', '')).upper()

                sexo_map = {'F': 'F', 'M': 'M'}


                sexo_final = sexo_map.get(sexo_excel, 'M')
                
                print('CPF',row.get('CPF'))
                
                microare=MicroArea.objects.get(microarea=str(row.get('MA')).strip())
                
                dados_cidadao = {
                    'cpf': row.get('CPF'),
                    'nome_completo': str(row.get('NOME CIDADAO')).strip() if pd.notna(row.get('NOME CIDADAO')) else None,
                    'sexo':sexo_final,
                    'dt_nascimento': row.get('DATA NASCIMENTO'),
                    'nome_mae': str(row.get('NOME DA MAE')).strip() if pd.notna(row.get('NOME DA MAE')) else None,
                    'nome_pai':row.get('NOME DO PAI'),
                    'nacionalidade': str(row.get('MUNIC. NASCIMENTO')).strip() if pd.notna(row.get('MUNIC. NASCIMENTO')) else None,
                    'microarea': microare,
                    'telefone1':str(row.get('CONTATO')).strip()
                }

                dados_endereco = {
                    'cod_logradouro': cod_logradouro,
                    'logradouro':str(row.get('LOGRADOURO')).strip(),
                    'numero': str(row.get('N')).strip(),
                    'complemento':str(row.get('COMPLEMENTO')).strip(),
                    'bairro': str(row.get('BAIRRO')).strip(),
                    'cidade': 'SANTO ANTÔNIO DO JACINTO',
                    'estado': 'MG',
                    'cep': '39935-000',
                    'localizacao':cod_localizacao,
                }

                cidadao = None
                
                # Limpar os dados para evitar problemas na busca
                dados_cidadao = {k: v for k, v in dados_cidadao.items() if v is not None}
                dados_endereco = {k: v for k, v in dados_endereco.items() if v is not None}

        
                if dados_cidadao.get('cpf'):
                    try:
                        cidadao = Cidadao.objects.get(cpf=dados_cidadao['cpf'])
                        print(f"Cidadão encontrado por CPF: {cidadao.cpf}. Atualizando...")
                    except Cidadao.DoesNotExist:
                        pass
                    
                        
                # 3. Se um cidadão foi encontrado, atualiza os dados
                if cidadao:
                    for chave, valor in dados_cidadao.items():
                        setattr(cidadao, chave, valor)
                    cidadao.save()
                    print(f"Dados do cidadão '{cidadao.nome_completo}' atualizados.")
                else:
                    # 4. Se não encontrou, cria um novo registro de cidadão
                    cidadao = Cidadao.objects.create(**dados_cidadao)
                    print(f"Novo cidadão '{cidadao.nome_completo}' criado.")

                # 5. Lógica para encontrar ou criar o endereço, associado ao cidadão
                if dados_endereco:
                    busca_endereco = {'cidadao': cidadao, **dados_endereco}
                    try:
                        endereco = Endereco.objects.get(**busca_endereco)
                        # Se o endereço já existe para esse cidadão, apenas o atualiza
                        for chave, valor in dados_endereco.items():
                            setattr(endereco, chave, valor)
                        endereco.save()
                        print(f"Endereço para '{cidadao.nome_completo}' atualizado.")
                    except Endereco.DoesNotExist:
                        # Se não existe, cria um novo
                        Endereco.objects.create(**busca_endereco)
                        print(f"Novo endereço criado para '{cidadao.nome_completo}'.")

        else: 
            form=ImportarDadosForm(ImportarDadosForm(request.POST or None, request.FILES))
    else:
        
        form=ImportarDadosForm()
                    
        return render(request,template_name, {'form': form}) 



def importar_dados_excel(request):
    template_name = 'cidadao/importar_dados.html'

    if request.method == 'POST':
        form = ImportarDadosForm(request.POST, request.FILES)
        if form.is_valid():
            arquivo_excel = request.FILES['arquivo']
            df = pd.read_excel(arquivo_excel, dtype={'CPF': str, 'CNS': str})

            # Preenche os valores NaN com strings vazias para evitar o erro de 'nan' duplicado.
            df['CPF'] = df['CPF'].fillna('')
            df['CNS'] = df['CNS'].fillna('')

            # Contadores para o resumo da importação
            novos_registros_criados = 0
            registros_atualizados = 0
            registros_ignorados = 0

            for index, row in df.iterrows():
                # 1. Preparar os dados da linha
                cns = str(row.get('CNS', '')).strip() if row.get('CNS') else None
                cpf = str(row.get('CPF', '')).strip() if row.get('CPF') else None
                
                # Ignora a linha se não tivermos nem CNS nem CPF para a verificação
                if not cns and not cpf:
                    registros_ignorados += 1
                    continue

                # --- LÓGICA PRINCIPAL: ATUALIZAR POR CNS OU CPF > CRIAR NOVO ---
                
                cidadao_existente = None
                
                # Passo A: Tentar encontrar o cidadão por CNS (prioridade 1)
              
                    
                # Passo B: Se não encontrou por CNS, tenta encontrar por CPF (prioridade 2)
                if cpf:
                    cidadao_existente = Cidadao.objects.filter(cpf=cpf).first()

                if cidadao_existente:
                    # Se encontrou por CNS ou CPF, atualiza o registro
                    try:
                        # Prepara um dicionário com os campos a serem atualizados
                        # Para o seu caso, apenas o CNS é importante.
                        dados_para_atualizar = {}
                        if cns and cns != cidadao_existente.cns:
                             dados_para_atualizar['cns'] = cns

                        # Se houver dados para atualizar, faça a alteração
                        if dados_para_atualizar:
                            for chave, valor in dados_para_atualizar.items():
                                setattr(cidadao_existente, chave, valor)
                            cidadao_existente.save()
                            registros_atualizados += 1
                        else:
                            # Se encontrou, mas não há nada para atualizar, ignora
                            registros_ignorados += 1

                    except Exception as e:
                        print(f"Erro ao atualizar registro (CNS/CPF): {e}")

                

            # Adiciona uma mensagem de sucesso para o usuário com o resumo da importação
            messages.success(request, f"Importação concluída! {novos_registros_criados} novos registros criados, {registros_atualizados} registros atualizados e {registros_ignorados} registros ignorados.")
            
            # Redireciona para evitar que o formulário seja reenviado
            return redirect('cidadao:list-cidadao')
                
        else:
            form = ImportarDadosForm(request.POST, request.FILES)
    else:
        form = ImportarDadosForm()
            
    return render(request, template_name, {'form': form})

  """   
@has_role_decorator(['coordenador'])
def cidadao_delete(request,id):
    cidadao=get_object_or_404(Cidadao,id=id)

    try:
        cidadao.delete()
        messages.add_message(request, constants.SUCCESS ,"Registro excluido com sucesso")

    except ProtectedError:
        messages.add_message(request, constants.ERROR ,"Infelizmente não foi possível, pois existe  uma ou mais referências e não pode ser excluído.")
    finally:
        return redirect('cidadao:list-cidadao')
    
class CidadaoAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Garante que a busca só seja feita por usuários autenticados
        if not self.request.user.is_authenticated:
            return Cidadao.objects.none()

        qs = Cidadao.objects.all()

        if self.q:
            # Filtra por nome do cidadão.
            # Adapte 'nome' para o campo de Cidadao que deseja usar na busca.
            qs = qs.filter(nome_completo__icontains=self.q)

        return qs