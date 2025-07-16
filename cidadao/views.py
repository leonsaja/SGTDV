from django.contrib import messages
from django.db.models import ProtectedError, Q
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

class CidadaoCreateView(HasRoleMixin,CreateView,SuccessMessageMixin):
    model = Cidadao
    form_class = CidadaoForm
    template_name = 'cidadao/form_cidadao.html'
    success_url = reverse_lazy('cidadao:list-cidadao')
    success_message='Cadastro realizado com sucesso'
    allowed_roles=['acs','recepcao','regulacao']
    
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
            self.object = form.save()  # Save the Cidadao instance
            form_endereco.instance.cidadao = self.object # Assign the saved Cidadao to the Endereco
            form_endereco.save() # Save the Endereco instance
            return super().form_valid(form)
        else:
            return self.form_invalid(form) # If Endereco form is not valid, re-render the form with errors

    def form_invalid(self, form):
        context = self.get_context_data()
        return self.render_to_response(context)


class CidadaoUpdateView(HasRoleMixin,UpdateView,SuccessMessageMixin):
    model = Cidadao
    form_class = CidadaoForm
    template_name = 'cidadao/form_cidadao.html' 
    success_url = reverse_lazy('cidadao:list-cidadao')
    allowed_roles=['acs','recepcao','regulacao']
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
            messages.add_message(self.request, constants.SUCCESS ,"Dados atualizados com sucesso")
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        context = self.get_context_data()
        return self.render_to_response(context)

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

class CidadaoDetailView(HasRoleMixin,DetailView):
    model=Cidadao
    template_name='cidadao/detail_cidadao.html'
    allowed_roles = ['acs','coordenador','regulacao','recepcao']


    def get_context_data(self, *args, **kwargs):
        context=super().get_context_data(*args, **kwargs)
        context[ 'paciente']=Cidadao.objects.select_related('endereco','microarea').get(pk=self.kwargs['pk'])
        
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

        search_nome_cpf_cns=self.request.GET.get('search_nome_cpf',None)
        search_nome_mae=self.request.GET.get('search_nome_mae',None)
        search_dt_nascimento=self.request.GET.get('search_dt_nascimento',None)

        if search_nome_cpf_cns:
            qs=qs.select_related('microarea').filter(Q(nome_completo__iregex=search_nome_cpf_cns)| Q(cpf__icontains=search_nome_cpf_cns)|Q(cns__icontains=search_nome_cpf_cns))
              
        if search_nome_mae:
            qs=qs.select_related('microarea').filter(nome_mae__icontains=search_nome_mae)
        
        if search_dt_nascimento:
            qs=qs.select_related('microarea').filter(dt_nascimento__iexact=search_dt_nascimento)

        return qs

class ImportDadosView(View):
    template_name='cidadao/importar_dados.html'

    def get(self, request):
        cidadao = Cidadao.objects.all()
        form = ImportarDadosForm()
        return render(request, self.template_name, {
            'form': form,
            'clientes': cidadao
        })
    
    def post(self, request):
        form = ImportarDadosForm(request.POST, request.FILES)

        if form.is_valid():
            arquivo = request.FILES['arquivo']
            df = pd.read_excel(arquivo)

            for _, row in df.iterrows():
                # Itera sobre as linhas do DataFrame lido do arquivo Excel 
                self.criar_cidadao_e_endereco(row)

            return redirect('cidadao:list-cidadao')

        return render(request, self.template_name, {'form': form})

    def criar_cidadao_e_endereco(self, row):
        
        
        cod_logradouro_map = {
            'RUA': '2',
            'FAZENDA': '3',
            'PRACA': '4',
            'PRAÇA': '4', # Adicione variações se necessário
            'TRAVESSA': '5',
        }
        
        cod_logradouro_excel = str(row.get('CÓD. LOGRADOURO', '')).upper()
        
        # Pega o código mapeado ou '1' (ou outro padrão) se não encontrar
        cod_logradouro = cod_logradouro_map.get(cod_logradouro_excel, '1') # '1' pode ser para 'OUTROS' ou padrão
        endereco_obj = None
        
        # 2. Obter ou criar o Cidadão
        # Padroniza SEXO e RAÇA/COR para comparação
        sexo_excel = str(row.get('SEXO', '')).upper()
        raca_excel = str(row.get('RAÇA/COR', '')).upper()

        sexo_map = {'F': 'F', 'M': 'M'}
        raca_map = {
            'AMARELA': 1,
            'BRANCA': 2,
            'PARDA': 3,
            'PRETA': 4,
            # 'INDÍGENA': 5, # Adicione se houver
        }

        sexo_final = sexo_map.get(sexo_excel, 'M') # Padrão 'M' ou tratar erro
        raca_final = raca_map.get(raca_excel, 0) # Padrão 0 ou outro valor para "Não especificado"

        
        try:
            cidadao, created = Cidadao.objects.get_or_create(
                cns=str(row.get('CNS', '')).strip(), # CNS como chave única
                defaults={
                    'nome_completo': row.get('NOME', '').strip(),
                    'sexo': sexo_final,
                    'dt_nascimento': row.get('DATA DE NASCIMENTO'), # Certifique-se de que o formato do Excel é compatível com DateField
                    'telefone1': str(row.get('TELEFONE1', '00000000000')).strip(),
                    'raca': raca_final,
                    'nacionalidade': row.get('NACIONALIDADE', 'Brasileira').strip(),
                    
                }
            )
        except Exception as e:
            print(f"Erro ao criar/obter cidadão: {e} - Linha: {row}")
            # Logue o erro detalhadamente, talvez salve em um arquivo de log para depuração.
            # Considere retornar False ou levantar uma exceção para o chamador.
        
        if row.get('ENDEREÇO'): # Usar .get() para evitar KeyError
            try:
                # Usa .get() para valores que podem estar faltando no Excel
                endereco_obj, created = Endereco.objects.get_or_create(
                    logradouro=row.get('ENDEREÇO', '').strip(), # .strip() para remover espaços extras
                    cep=str(row.get('CEP', '')).strip(), # Converte para string para garantir
                    bairro=str(row.get('BAIRRO', '')).strip(),
                    numero=str(row.get('NÚMERO', '')).strip(), # Converte para string para garantir
                    defaults={
                        'cod_logradouro': cod_logradouro,
                        'complemento': row.get('COMPLEMENTO', '').strip(),
                        'estado': 'MG', # Supondo que seja sempre MG
                        'cidade': 'SANTO ANTÔNIO DO JACINTO', # Supondo que seja sempre esta cidade
                        'cidadao':cidadao
                    }
                )
            except Exception as e:
                print(f"Erro ao criar/obter endereço: {e} - Linha: {row}")
                # Considere logar o erro ou lidar com ele de forma mais robusta

        

            # Se o cidadão já existia, mas o endereço não estava associado, atualize
    

        
            
            

        """"if row['ENDEREÇO']:

         
            # Cria o endereço associado ao cliente
            if row['CÓD. LOGRADOURO']=='RUA' or row['CÓD. LOGRADOURO']=='rua' :
                endereco=Endereco.objects.get_or_create(
                    cod_logradouro='2',
                    logradouro=row['ENDEREÇO'],
                    cep=row['CEP'],
                    bairro=row['BAIRRO'],
                    complemento=row['COMPLEMENTO'],
                    numero=row['NÚMERO'],
                    estado='MG',
                    cidade='SANTO ANTÔNIO DO JACINTO',
                )
            elif row['CÓD. LOGRADOURO']=='FAZENDA' or row['CÓD. LOGRADOURO']=='fazenda':
                endereco=Endereco.objects.get_or_create(
                    cod_logradouro='3',
                    logradouro=row['ENDEREÇO'],
                    cep=row['CEP'],
                    bairro=row['BAIRRO'],
                    complemento=row['COMPLEMENTO'],
                    numero=row['NÚMERO'],
                    estado='MG',
                    cidade='SANTO ANTÔNIO DO JACINTO',
                )
            elif row['CÓD. LOGRADOURO']=='PRACA'or row['CÓD. LOGRADOURO']=='praca':
                endereco=Endereco.objects.get_or_create(
                    cod_logradouro='4',
                    logradouro=row['ENDEREÇO'],
                    cep=row['CEP'],
                    bairro=row['BAIRRO'],
                    complemento=row['COMPLEMENTO'],
                    numero=row['NÚMERO'],
                    estado='MG',
                    cidade='SANTO ANTÔNIO DO JACINTO',
                )
            elif row['CÓD. LOGRADOURO']=='TRAVESSA' or row['CÓD. LOGRADOURO']=='travessa':
                endereco=Endereco.objects.get_or_create(
                    cod_logradouro='5',
                    logradouro=row['ENDEREÇO'],
                    cep=row['CEP'],
                    bairro=row['BAIRRO'],
                    complemento=row['COMPLEMENTO'],
                    numero=row['NÚMERO'],
                    estado='MG',
                    cidade='SANTO ANTÔNIO DO JACINTO',
                )

        if row['SEXO'] =='F' or row['SEXO']=='f':
                    print('F')
                    if row['RAÇA/COR']=='PARDA':
                        print('PARDA')
                        cliente, criado = Cidadao.objects.get_or_create(
                        cns=row['CNS'],
                        defaults={
                            'nome_completo': row['NOME'],
                            'sexo': 'F',
                            'dt_nascimento': row['DATA DE NASCIMENTO'],
                            'telefone1':'00000000000',
                            'raca':3,
                            'nacionalidade':row['NACIONALIDADE'],
                           
                           

                        })
                    elif row['RAÇA/COR']=='AMARELA':
                        print('AMARELA')
                        cliente, criado = Cidadao.objects.get_or_create(
                        cns=row['CNS'],
                        defaults={
                            'nome_completo': row['NOME'],
                            'sexo': 'F',
                            'dt_nascimento': row['DATA DE NASCIMENTO'],
                            'telefone1':'00000000000',
                            'raca':1,
                            'nacionalidade':row['NACIONALIDADE'],
                            
                           

                        })
                    elif row['RAÇA/COR']=='PRETA':
                        cliente, criado = Cidadao.objects.get_or_create(
                        cns=row['CNS'],
                        defaults={
                            'nome_completo': row['NOME'],
                            'sexo': 'F',
                            'dt_nascimento': row['DATA DE NASCIMENTO'],
                            'telefone1':'00000000000',
                            'raca':4,
                            'nacionalidade':row['NACIONALIDADE'],
                           
                            

                        })
                    elif row['RAÇA/COR']=='BRANCA':
                        cliente, criado = Cidadao.objects.get_or_create(
                        cns=row['CNS'],
                        defaults={
                            'nome_completo': row['NOME'],
                            'sexo': 'F',
                            'dt_nascimento': row['DATA DE NASCIMENTO'],
                            'telefone1':'00000000000',
                            'raca':2,
                            'nacionalidade':row['NACIONALIDADE'],
                           
                            

                        })
                
        elif row['SEXO'] =='M' or row['SEXO']=='m':
                    if row['RAÇA/COR']=='PARDA':
                        print('NOME',row['NOME'])
                        print('parda')
                        cliente, criado = Cidadao.objects.get_or_create(
                        cns=row['CNS'],
                        defaults={
                            'nome_completo': row['NOME'],
                             'sexo':'M',
                            'dt_nascimento': row['DATA DE NASCIMENTO'],
                            'telefone1':'00000000000',
                            'raca':3,
                            'nacionalidade':row['NACIONALIDADE'],
                            
                           

                        })
                    elif row['RAÇA/COR']=='AMARELA':
                        cliente, criado = Cidadao.objects.get_or_create(
                        cns=row['CNS'],
                        defaults={
                            'nome_completo': row['NOME'],
                            'sexo':'M',
                            'dt_nascimento': row['DATA DE NASCIMENTO'],
                            'telefone1':'00000000000',
                            'raca':1,
                            'nacionalidade':row['NACIONALIDADE'],
                            
                            

                        })
                    elif row['RAÇA/COR']=='PRETA':
                        cliente, criado = Cidadao.objects.get_or_create(
                        cns=row['CNS'],
                        defaults={
                            'nome_completo': row['NOME'],
                             'sexo':'M',
                            'dt_nascimento': row['DATA DE NASCIMENTO'],
                            'telefone1':'00000000000',
                            'raca':1,
                            'nacionalidade':1,
                           
                           

                        })
                    elif row['RAÇA/COR']=='BRANCA':
                        cliente, criado = Cidadao.objects.get_or_create(
                        cns=row['CNS'],
                        defaults={
                            'nome_completo': row['NOME'],
                             'sexo':'M',
                            'dt_nascimento': row['DATA DE NASCIMENTO'],
                            'telefone1':'00000000000',
                            'raca':1,
                            'nacionalidade':2,
                            
                            

                        })
"""

           