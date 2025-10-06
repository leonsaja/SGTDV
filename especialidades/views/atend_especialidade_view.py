
from especialidades.models import AtendimentoEspecialidade, PacienteSia,PacienteEspecialidade
from especialidades.forms.form_atendimento_especialidade import AtendimentoEspecialidadeForm,GerarPDFAtendimentoForm
from django.shortcuts import get_object_or_404, render
from django.contrib.messages.views import SuccessMessageMixin
from especialidades.forms.form_paciente_set import AtendPacienteSet
from django.views.generic import DetailView, ListView,DeleteView,CreateView,UpdateView
from django.shortcuts import get_object_or_404 
from django.urls import reverse_lazy
from rolepermissions.decorators import has_role_decorator
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from django.db.models import Q
from dal import autocomplete
from io import BytesIO
from django.utils.decorators import method_decorator
from django.db import transaction

@method_decorator(has_role_decorator(['regulacao'], redirect_url=reverse_lazy('usuarios:acesso_negado')), name='dispatch')
class AtendimentoEspecialidadeCreateView(SuccessMessageMixin,CreateView):
    model = AtendimentoEspecialidade
    form_class = AtendimentoEspecialidadeForm
    template_name = 'atendimento_especialidade/form_atend_especialidade.html'
    success_url = reverse_lazy('especialidades:list-atend_especialidade')
    success_message= 'Atendimento cadastrado com sucesso!'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['prefix'] = 'atendimento'
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = AtendPacienteSet(self.request.POST, instance=self.object, prefix='paciente')
        else:
            context['formset'] = AtendPacienteSet(instance=self.object, prefix='paciente')
        return context

    def form_valid(self, form):
  
        formset = self.get_context_data()['formset']      
        if formset.is_valid():
            
            """especialidade = form.cleaned_data.get('especialidade')
            total_pacientes = 0
           
            for f in formset.cleaned_data:  # formset.cleaned_data contém apenas os formulários que não foram marcados para exclusão
                if f and not f.get('DELETE'):
                     total_pacientes += 1
            
            saldo_atual = especialidade.limite_pacientes
            novo_saldo = saldo_atual - total_pacientes

            if novo_saldo < 0:
                form.add_error(
                    'especialidade', 
                    f"Saldo insuficiente! A especialidade '{especialidade.nome}' tem apenas {saldo_atual} vagas disponíveis, mas você está tentando cadastrar {total_pacientes} pacientes."
                )
                return self.form_invalid(form)"""

            self.object = form.save(commit=False)
            self.object.criado_por = self.request.user.nome_completo
            self.object.save()
            
            # 4. Atualiza o Saldo (diminui o limite de pacientes da Especialidade)
            #especialidade.limite_pacientes = novo_saldo
            #especialidade.save() # Salva a especialidade com o novo limite/saldo
            
            # 5. Salva os pacientes (Formset)
            formset.instance = self.object  
            formset.save()
            
            return super().form_valid(form)
        else:
            
            return self.form_invalid(form)
        
    def form_invalid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        return self.render_to_response(self.get_context_data(form=form, formset=formset))    

@method_decorator(has_role_decorator(['regulacao'], redirect_url=reverse_lazy('usuarios:acesso_negado')), name='dispatch')       
class AtendimentoEspecialidadeUpdateView(SuccessMessageMixin,UpdateView):
    model = AtendimentoEspecialidade
    form_class = AtendimentoEspecialidadeForm
    template_name = 'atendimento_especialidade/form_atend_especialidade.html'
    success_url = reverse_lazy('especialidades:list-atend_especialidade')
    allowed_roles=['regulacao']
    success_message='Atendimento alterado com sucesso'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['prefix'] = 'atendimento'
        return kwargs

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = AtendPacienteSet(self.request.POST, instance=self.object, prefix='paciente')
        else:
            context['formset'] = AtendPacienteSet(instance=self.object, prefix='paciente')
        return context
    
    def form_valid(self, form):
        
        formset = self.get_context_data()['formset']      
     
        if formset.is_valid():
                        
           """ # Número de pacientes ANTES de salvar (já ligados a este Atendimento)
            pacientes_antes = self.object.atend_paciente_especialidade.count()
            
            # Número de pacientes DEPOIS de salvar (pacientes do formset, exceto os deletados)
            pacientes_depois = 0
            for f in formset.cleaned_data:
                # Conta apenas os formulários que são válidos e NÃO estão marcados para exclusão
                if f and not f.get('DELETE'):
                    pacientes_depois += 1
            
            # Diferença líquida: Se for positivo, estamos adicionando pacientes (DÉBITO).
            # Se for negativo, estamos removendo pacientes (CRÉDITO/RESTITUIÇÃO).
            diferenca_liquida = pacientes_depois - pacientes_antes
            
            especialidade = form.cleaned_data.get('especialidade')
            
            # --- 2. Validação de Saldo (apenas se estiver adicionando pacientes) ---
            
            if diferenca_liquida > 0:

                saldo_atual = especialidade.limite_pacientes
                novo_saldo_projetado = saldo_atual - diferenca_liquida
                
                if novo_saldo_projetado < 0:
                    # Saldo insuficiente para cobrir a diferença
                    form.add_error(
                        'especialidade', 
                        f"Saldo insuficiente! Você está tentando adicionar {diferenca_liquida} pacientes, mas a especialidade '{especialidade.nome}' tem apenas {saldo_atual} vagas disponíveis."
                    )
                    # Retorna form_invalid para reexibir o formulário com o erro
                    return self.form_invalid(form)"""

            # --- 3. Executar o Salvamento e Atualização (Transação) ---
            
            # Usar uma transação garante que o atendimento E o saldo sejam atualizados juntos.
           with transaction.atomic():
                # Salva o Atendimento (principal)
                self.object = form.save(commit=False)
                self.object.alterado_por = self.request.user.nome_completo # Atualiza o campo de alteração
                self.object.save()
                
                # Salva os pacientes (Formset)
                formset.instance = self.object  
                formset.save()
                
                # Atualiza o Saldo da Especialidade
                # O ajuste é sempre a 'diferenca_liquida':
                # - Se positivo, subtrai (débito).
                # - Se negativo, soma (crédito/restituição).
                
                # Exemplo: Saldo 10. Antes: 5 pacientes. Depois: 7 pacientes. Diferença: +2. Novo Saldo: 10 - 2 = 8.
                # Exemplo: Saldo 10. Antes: 5 pacientes. Depois: 3 pacientes. Diferença: -2. Novo Saldo: 10 - (-2) = 12.
                
                #especialidade.limite_pacientes -= diferenca_liquida 
                #especialidade.save()
            
            # Retorna o sucesso
                return super().form_valid(form)
        else:
            return self.form_invalid(form)
    def form_invalid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        return self.render_to_response(self.get_context_data(form=form, formset=formset))    

@method_decorator(has_role_decorator(['regulacao','secretario','coordenador','recepcao'], redirect_url=reverse_lazy('usuarios:acesso_negado')), name='dispatch')
class AtendEspecialidadeListView(ListView):
    
    model=AtendimentoEspecialidade
    template_name='atendimento_especialidade/list_atend_especialidade.html'
    context_object_name='atend_especialidades'
    paginate_by=10

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs).select_related('especialidade')

        buscar=self.request.GET.get('buscar',None)
        status=self.request.GET.get('status',None)
        data = self.request.GET.get('data', None)

        if buscar:
            qs=qs.filter(especialidade__nome__icontains=buscar.rstrip())
    
        if status:
            qs=qs.filter(status=status)

        if data:
            qs = qs.filter(data__iexact=data)

        if not buscar and not status and not data:
                qs=qs.filter(status='1')
        return qs.order_by('-data')
    
@method_decorator(has_role_decorator(['regulacao','secretario','coordenador','recepcao'], redirect_url=reverse_lazy('usuarios:acesso_negado')), name='dispatch')
class AtendEspecialidadeDetailView(DetailView):

    model=AtendimentoEspecialidade
    template_name='atendimento_especialidade/detail_atend_especialidade.html'
    
    def get_context_data(self,*args, **kwargs):
        context=super().get_context_data(*args, **kwargs)
        atendimento_especialidade= AtendimentoEspecialidade.objects.select_related('especialidade').get(id=self.kwargs['pk'])
        
        context['atendimento_especialidade']=atendimento_especialidade
        context['pacientes_set']=PacienteSia.objects.select_related('paciente').filter(atendimento_paciente__id=atendimento_especialidade.id)
        return context

@method_decorator(has_role_decorator(['coordenador'], redirect_url=reverse_lazy('usuarios:acesso_negado')), name='dispatch')
class AtendEspecialidadeDeleteView(SuccessMessageMixin, DeleteView):


    model=AtendimentoEspecialidade
    success_url=reverse_lazy('especialidades:list-atend_especialidade')
    success_message='Registro excluido com sucesso '


    def get(self, request, *args, **kwargs):
        return self.post().get(request, *args, **kwargs)
  
class PacienteAutocomplete(autocomplete.Select2QuerySetView):
    
    def get_queryset(self):
        
        if not self.request.user.is_authenticated:
            return PacienteEspecialidade.objects.none()

        especialidade_id = self.forwarded.get('atendimento-especialidade', None)        
    
        if especialidade_id:
            qs = PacienteEspecialidade.objects.select_related('paciente','especialidade','procedimento').filter(Q(status='1')|Q(status='4')|Q(status='5'),especialidade__id=especialidade_id).order_by('paciente__nome_completo')
        else:
            return PacienteEspecialidade.objects.none()
        if self.q:
            self.q=self.q.rstrip()
            qs = qs.filter(
                Q(paciente__nome_completo__unaccent__icontains=self.q) |
                Q(paciente__cns__icontains=self.q)
            ).filter(Q(status='1')|Q(status='5'))

        return qs


  


def gerar_pdf_atend(request,context):

   atendimento_id=context['atendimento_especialidade']

   lista_pacientes = PacienteSia.objects.select_related('paciente').filter(atendimento_paciente=atendimento_id).all()
   
   ordenar=context['ordenar']


   if ordenar == '1':
       print('teste')
       lista_pacientes=lista_pacientes.order_by('paciente__paciente__nome_completo')

   elif ordenar == '2':
       lista_pacientes=lista_pacientes.order_by('-paciente__paciente__nome_completo')
       
   elif ordenar == '3':
       lista_pacientes=lista_pacientes.order_by('hora')
    
   elif ordenar == '4':
       lista_pacientes=lista_pacientes.order_by('-hora')
       
   elif ordenar == '5':
       lista_pacientes=lista_pacientes.order_by('paciente__procedimento__nome_procedimento')
       
   elif ordenar == '6':
       lista_pacientes=lista_pacientes.order_by('-paciente__procedimento__nome_procedimento')
   
   elif ordenar == '7':
   
      lista_pacientes=lista_pacientes.order_by('paciente__paciente__microarea__estabelecimento')
       
   elif ordenar == '8':
       lista_pacientes=lista_pacientes.order_by('-paciente__paciente__microarea__estabelecimento')
       
   context = {
        'atendimento_especialidade': atendimento_id,
        'pacientes_set': lista_pacientes,
    }

    # 3. Renderiza o template HTML.
   html_string = render_to_string(
        'atendimento_especialidade/pdf_atend_especialidade.html',
        context
    )

    # 4. Cria um buffer na memória para o PDF.
   buffer = BytesIO()

    # 5. Gera o PDF usando WeasyPrint e salva no buffer.
   HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(buffer)
   
   # 6. Prepara a resposta HTTP para download.
   response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
   response['Content-Disposition'] = f'inline; filename="Atendimento_{atendimento_id.especialidade.nome}_{atendimento_id.data.strftime("%d/%m/%Y")}.pdf"'

   return response


@has_role_decorator(['regulacao','coordenador','recepcao','secretario'],redirect_url=reverse_lazy('usuarios:acesso_negado'))  
def atend_especialidade_pdf(request, id):
    context={}
    context['atendimento_especialidade'] = get_object_or_404(
        AtendimentoEspecialidade.objects.select_related('especialidade'),
        id=id
    )

    if request.method == 'POST':
            form=GerarPDFAtendimentoForm(request.POST or None)
            
            if form.is_valid():
                context['ordenar']=form.cleaned_data.get('ordenar')
                
                print('tipo',context['ordenar'])
            
            return gerar_pdf_atend(request,context)
            

    else:
        form=GerarPDFAtendimentoForm(request.POST or None)    
        
    return render(request,'atendimento_especialidade/ordenar_atend_especialidade.html',{'form':form})           