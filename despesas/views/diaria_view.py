from django.db.models import ProtectedError, Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from weasyprint import HTML
from rolepermissions.mixins import HasRoleMixin
from rolepermissions.decorators import has_role_decorator
from despesas.forms.diaria_form import DiariaForm,DiariaStatusForm
from django.contrib.messages.views import SuccessMessageMixin
from ..models import Diaria, Reembolso
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib.auth import get_user_model
from io import BytesIO
from django.utils.decorators import method_decorator

@method_decorator(has_role_decorator(['digitador'], redirect_url=reverse_lazy('usuarios:acesso_negado')), name='dispatch')
class DiariaCreateView(SuccessMessageMixin,CreateView):
   model=Diaria
   form_class=DiariaForm 
   template_name='diaria/form_diaria.html'
   success_url=reverse_lazy('despesas:list-diaria')
   success_message='Cadastro realizado com sucesso'

   def form_valid(self, form):
        
        self.object = form.save(commit=False)
        self.object.criado_por = self.request.user.nome_completo
        self.object.save()
        return  super().form_valid(form)
 
@method_decorator(has_role_decorator(['digitador','secretario'], redirect_url=reverse_lazy('usuarios:acesso_negado')), name='dispatch')  
class DiariaUpdateView(SuccessMessageMixin,UpdateView):

    model=Diaria             
    form_class=DiariaForm
    template_name='diaria/form_diaria.html'
    success_url=reverse_lazy('despesas:list-diaria')
    success_message='Dados atualizado com sucesso'


    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.alterado_por = self.request.user.nome_completo
        self.object.save()
        return  super().form_valid(form)

@method_decorator(has_role_decorator(['digitador','coordenador','secretario'], redirect_url=reverse_lazy('usuarios:acesso_negado')), name='dispatch')
class DiariaListView(ListView):

    model=Diaria
    template_name='diaria/list_diaria.html'
    context_object_name='diarias'
    paginate_by=10
    queryset=Diaria.objects.select_related('profissional').order_by('-created_at')

@method_decorator(has_role_decorator(['digitador','coordenador','secretario'], redirect_url=reverse_lazy('usuarios:acesso_negado')), name='dispatch')
class DiariaSearchListView(ListView):

    model=Diaria
    template_name='diaria/list_diaria.html'
    context_object_name='diarias'
    paginate_by=10

    def get_queryset(self, *args, **kwargs):
        qs = super(DiariaSearchListView,self).get_queryset(*args, **kwargs)
        
        buscar=self.request.GET.get('buscar',None).rstrip()
        data=self.request.GET.get('data',None)
        
        if buscar:
            qs=qs.select_related('profissional').filter(Q(profissional__nome_completo__icontains=buscar)|\
                Q(profissional__cpf__icontains=buscar)).\
                order_by('-created_at')
        if data:
            qs=qs.select_related('profissional').filter(data_diaria__iexact=data).order_by('-created_at')
    
        return qs
    
@method_decorator(has_role_decorator(['secretario'], redirect_url=reverse_lazy('usuarios:acesso_negado')), name='dispatch')
class DiariaStatusUpdateView(SuccessMessageMixin, UpdateView):
    
   model=Diaria
   form_class=DiariaStatusForm 
   template_name='diaria/detail_diaria.html'
   success_url=reverse_lazy('despesas:list-diaria')
   success_message='Operação realizado com sucesso'

   def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.aprovado_por = self.request.user.nome_completo
        self.object.save()
        return  super().form_valid(form)

@method_decorator(has_role_decorator(['digitador','coordenador','secretario'], redirect_url=reverse_lazy('usuarios:acesso_negado')), name='dispatch')
class DiariaDetailView(DetailView):
    model=Diaria
    template_name='diaria/detail_diaria.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        diaria=Diaria.objects.select_related('profissional').get(id=self.kwargs['pk'])
        context['diaria']=diaria
        context['reembolsos'] =Reembolso.objects.select_related('diaria').filter(diaria__id=diaria.id)
        context['form']=DiariaStatusForm(self.request.POST or None,instance=diaria)
        return context

@has_role_decorator(['coordenador'],redirect_url=reverse_lazy('usuarios:acesso_negado'))
def diaria_delete(request, id):
    diaria=get_object_or_404(Diaria,id=id)
    
    try:
        diaria.delete()
        messages.add_message(request,constants.SUCCESS,'Registro excluir com sucesso')
    except ProtectedError:
        messages.add_message(request, constants.ERROR, "Infelizmente não foi possível, pois existe  uma ou mais referências e não pode ser excluído.")
    finally:
        return redirect('despesas:list-diaria')

@has_role_decorator(['digitador','coordenador','secretario'],redirect_url=reverse_lazy('usuarios:acesso_negado'))
def diaria_pdf(request,id):
   

    diaria=get_object_or_404(Diaria,id=id)
    User=get_user_model()

    profissional=User.objects.filter(is_active=True).filter(perfil='5').first()
    
    buffer = BytesIO()
    html_string = render_to_string('diaria/pdf_diaria.html',{'diaria':diaria,'profissional':profissional})
    HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(buffer)
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="Diaria_{diaria.profissional.profis()}_{diaria.data_diaria.strftime("%d/%m/%Y")}.pdf"'

    return response
