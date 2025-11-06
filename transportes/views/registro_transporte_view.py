
from django.urls import reverse_lazy
from django.views.generic import CreateView,UpdateView,ListView,DeleteView,DetailView
from transportes.models import RegistroTransporte,Carro
from transportes.forms.registro_transporte_form import RegistroTransporteForm
from django.contrib.messages.views import SuccessMessageMixin
from rolepermissions.mixins import HasRoleMixin
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from rolepermissions.decorators import has_role_decorator

@method_decorator(login_required(login_url='usuarios:login_usuario'), name='dispatch')
@method_decorator(has_role_decorator(['recepcao','regulacao'], redirect_url=reverse_lazy('usuarios:acesso_negado')), name='dispatch')
class RegistroTransporteCreateView(SuccessMessageMixin,CreateView):
    model =RegistroTransporte
    form_class=RegistroTransporteForm
    template_name='registro_transporte/form_registro_transporte.html'
    context_object_name='form'
    success_url=reverse_lazy('transportes:list-regis-transporte')
    success_message='Cadastro realizado com sucesso'
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.criado_por = self.request.user.nome_completo
        self.object.save()
        return  super().form_valid(form)

@method_decorator(login_required(login_url='usuarios:login_usuario'), name='dispatch')
@method_decorator(has_role_decorator(['recepcao','regulacao'], redirect_url=reverse_lazy('usuarios:acesso_negado')), name='dispatch')
class RegistroTransporteUpdateView(SuccessMessageMixin,UpdateView):
    model =RegistroTransporte
    form_class=RegistroTransporteForm
    template_name='registro_transporte/form_registro_transporte.html'
    context_object_name='form'
    success_url=reverse_lazy('transportes:list-regis-transporte')
    success_message='Cadastro alterado  com sucesso'
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.alterado_por = self.request.user.nome_completo
        self.object.save()
        return  super().form_valid(form)

@method_decorator(login_required(login_url='usuarios:login_usuario'), name='dispatch')
@method_decorator(has_role_decorator(['coordenador','secretario','recepcao','regulacao'], redirect_url=reverse_lazy('usuarios:acesso_negado')), name='dispatch')
class RegistroTransporteListView(ListView):
    model=RegistroTransporte
    template_name='registro_transporte/list_registro_transporte.html'
    context_object_name='transportes'
    ordering='-created_at'
    paginate_by=10
       
@method_decorator(login_required(login_url='usuarios:login_usuario'), name='dispatch')
@method_decorator(has_role_decorator(['coordenador','secretario','recepcao','regulacao'], redirect_url=reverse_lazy('usuarios:acesso_negado')), name='dispatch')      
class RegistroTransporteDetailView(DetailView):
    model=RegistroTransporte
    context_object_name='transporte'
    template_name='registro_transporte/detail_registro_transporte.html'

@method_decorator(login_required(login_url='usuarios:login_usuario'), name='dispatch')
@method_decorator(has_role_decorator(['coordenador'], redirect_url=reverse_lazy('usuarios:acesso_negado')), name='dispatch')      
class RegistroTransporteDeleteView(SuccessMessageMixin, DeleteView):
    model=RegistroTransporte
    success_url=reverse_lazy('transportes:list-regis-transporte')
    success_message='Registro excluido com sucesso'

    def get(self, request,*args, **kwargs):
         return self.post(request, *args, **kwargs)

@method_decorator(login_required(login_url='usuarios:login_usuario'), name='dispatch')
@method_decorator(has_role_decorator(['coordenador','secretario','recepcao','regulacao'], redirect_url=reverse_lazy('usuarios:acesso_negado')), name='dispatch')     
class RegistroTransporteSearchListView(ListView):
    model=RegistroTransporte
    template_name='registro_transporte/list_registro_transporte.html'
    context_object_name='transportes'
    paginate_by=10


    def get_queryset(self):
        qs=super().get_queryset().select_related('paciente','carro').order_by('-created_at')
        
        nome_paciente=self.request.GET.get('nome_paciente',None)
        dt_atendimento=self.request.GET.get('data',None)
        placa_carro=self.request.GET.get('placa_carro',None)
        
        
        if nome_paciente:
            nome_paciente=nome_paciente.rstrip()
            qs=qs.filter(Q(paciente__nome_completo__unaccent__icontains=nome_paciente) |Q(paciente__cpf__icontains=nome_paciente)|Q(paciente__cns__icontains=nome_paciente))
        
        if dt_atendimento:
            qs=qs.select_related('paciente','carro').filter(dt_atendimento=dt_atendimento).order_by('-created_at')

        if placa_carro:
            qs=qs.select_related('paciente','carro').filter(carro__placa__icontains=placa_carro).order_by('-created_at')
            
        return qs
"""    
class ImportDadosTransporteView(View):
    template_name='registro_transporte/importar_dados.html'

    def get(self, request):
        transportes = RegistroTransporte.objects.all()
        form = ImportarDadosForm()
        return render(request, self.template_name, {
            'form': form,
            'clientes': transportes
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
"""
"""def criar_cidadao_e_endereco(self, row):
        
        
        status_choices_excel = row.get('ATENDIDO','')
                
        STATUS_CHOICES={
            'SIM':1,
          
        }
        status = STATUS_CHOICES.get(status_choices_excel, '1')
        
       
        caract_atendi_excel = str(row.get('CARACTERISTICA DO ATENDIMENTO', '')).upper()
        
        caract_atendi_map = {
            'EVENTUAL': 1,
            'ROTINEIRO': 2,
           
        }

        tipo_atend_final = caract_atendi_map.get(caract_atendi_excel, 0)
        
        
        acompanhante_excel =row.get('ACOMPANHANTE','')
       
        ACOMPANHANTE_CHOICES_MAP={
            'SIM':1,
            'NÃO':2,
        }
        acompanhante_final = ACOMPANHANTE_CHOICES_MAP.get(acompanhante_excel, 0)

        ZONA_RURAL_excel = str(row.get('ATENDIMENTO EM ZONA RURAL', '')).upper()
        ZONA_RURAL_MAP={
            'SIM':1,
            'NÃO':2,
        }
        zona_rural_final = ZONA_RURAL_MAP.get(ZONA_RURAL_excel, 0)
       
        
        cidadao=Cidadao.objects.get(cns=row.get('CNS',''))

        carro=Carro.objects.get(placa=str(row.get('PLACA','')).upper())
      

        try:
            registro, created = RegistroTransporte.objects.get_or_create(
            paciente=cidadao, # CNS como chave única
           
                status=status,
                dt_atendimento= row.get('DATA DO ATENDIMENTO'), 
                carro= carro,
                tipo_atend=tipo_atend_final,
                acompanhante= acompanhante_final ,
                atend_zona_rural=zona_rural_final,
                origem=row.get('ORIGEM'),
                destino=row.get('DESTINO'),
                dist_percorrida=row.get('DISTÂNCIA PERCORRIDA '),
                quant_proced_paciente=row.get('TIPO1',''),
                quant_proced_acompanhante=row.get('TIPO2',''),
            
            )
        except Exception as e:
            print(f"Erro ao criar/obter cidadão: {e} - Linha: {row}")

        
        
"""