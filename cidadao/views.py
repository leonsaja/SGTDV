from django.contrib import messages
from django.db.models import ProtectedError, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import DetailView, ListView
import pandas as pd

from cidadao.forms.cidadao_form import CidadaoForm, EnderecoForm
from cidadao.forms.dados import ImportarDadosForm
from cidadao.models import Cidadao, Endereco
from django.contrib.messages import constants
from django.contrib import messages
from rolepermissions.decorators import has_role_decorator
from rolepermissions.mixins import HasRoleMixin

@has_role_decorator(['acs','recepcao','regulacao'])
def cidadao_create(request):
    if request.method == 'POST':
        form=CidadaoForm(request.POST or None)
        form_endereco=EnderecoForm(request.POST or None)
    
        if form.is_valid() and form_endereco.is_valid():
          
            forms=form.save(commit=False)
            form_end=form_endereco.save()
            forms.endereco=form_end
            forms.save()
            messages.add_message(request,constants.SUCCESS,'cadastro realizado com sucesso')

            return redirect('cidadao:list-cidadao')
    
    form=CidadaoForm(request.POST or None)
    form_endereco=EnderecoForm(request.POST or None)      
    return render(request,'cidadao/form_cidadao.html',{'form':form,'endereco':form_endereco})

@has_role_decorator(['acs','recepcao','regulacao'])
def cidadao_update(request,id):

    cidadao=get_object_or_404(Cidadao,id=id)
    
    
    if request.method =='POST':
        form=CidadaoForm(request.POST or None, instance=cidadao)
        form_endereco=EnderecoForm(request.POST or None, instance=cidadao.endereco)
        
        if form.is_valid() and form_endereco.is_valid():
            cidadao_form=form.save(commit=False)
            endereco_form=form_endereco.save()
            cidadao_form.endereco=endereco_form
            cidadao_form.save()
            messages.add_message(request,constants.SUCCESS,'Dados atualizado com sucesso')
            return redirect('cidadao:list-cidadao')
        
    form=CidadaoForm(request.POST or None,instance=cidadao)
    form_endereco=EnderecoForm(request.POST or None, instance=cidadao.endereco)

    return render(request,'cidadao/form_cidadao.html',{'form':form,'endereco':form_endereco})

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
            qs=qs.select_related('endereco','microarea').filter(Q(nome_completo__icontains=search_nome_cpf_cns)| Q(cpf__icontains=search_nome_cpf_cns)|Q(cns__icontains=search_nome_cpf_cns))
              
        if search_nome_mae:
            qs=qs.select_related('endereco','microarea').filter(nome_mae__icontains=search_nome_mae)
        
        if search_dt_nascimento:
            qs=qs.select_related('endereco','microarea').filter(dt_nascimento__iexact=search_dt_nascimento)

        return qs

"""
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

         if row['ENDEREÇO']:

         
            # Cria o endereço associado ao cliente
            if row['NÚMERO']:
                endereco=Endereco.objects.create(
                    cod_logradouro=row['CÓD. LOGRADOURO'],
                    logradouro=row['ENDEREÇO'],
                    cep=row['CEP'],
                    bairro=row['BAIRRO'],
                    complemento=row['COMPLEMENTO'],
                    numero=row['NÚMERO'],
                    estado='MG',
                    cidade='SANTO ANTÔNIO DO JACINTO',
                )
            
            

        # Use get_or_create para evitar a necessidade de verificar a existência antes de criar
                if row['SEXO'] =='F':
                    cliente, criado = Cidadao.objects.get_or_create(
                    cns=row['CNS'],
                    defaults={
                        'nome_completo': row['NOME'],
                        'sexo': 'F',
                        'dt_nascimento': row['DATA DE NASCIMENTO'],
                        'telefone1':'00000000000',
                        'endereco':endereco,

                    }
                )
                else:
                    cliente, criado = Cidadao.objects.get_or_create(
                    cns=row['CNS'],
                    defaults={
                    'nome_completo': row['NOME'],
                    'sexo':'M',
                    'dt_nascimento': row['DATA DE NASCIMENTO'],
                    'telefone1':'00000000000',
                    'endereco':endereco,

                    })
        
           
           """