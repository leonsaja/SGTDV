from django.contrib.auth import get_user_model
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView
from weasyprint import HTML
from django.template.loader import render_to_string
from django.db.models import Q
from io import BytesIO
from despesas.forms.reembolso_form import ReembolFormSet,DescricaoReembolsoForm
from despesas.models import Diaria, Reembolso
from django.contrib.messages import constants
from django.contrib import messages
from rolepermissions.decorators import has_role_decorator
from rolepermissions.mixins import HasRoleMixin

@has_role_decorator(['digitador'])
def reembolso_create(request,id):
    diaria=get_object_or_404(Diaria,id=id)
    
    if not diaria:
        return Http404()
    
    if request.method == 'POST':
        formset=ReembolFormSet(request.POST,instance=diaria,prefix='reembolso')
        form=DescricaoReembolsoForm(request.POST or None,instance=diaria,prefix='reembolso_diaria')

        if formset.is_valid() and form.is_valid():
            form.save()
            formset.save()
            messages.add_message(request,constants.SUCCESS,'cadastro realizado com sucesso')
            return redirect('despesas:list-reembolso')

    formset=ReembolFormSet(request.POST or None,instance=diaria,prefix='reembolso')
    form=DescricaoReembolsoForm(request.POST or None,instance=diaria,prefix='reembolso_diaria')
    
    return render(request, 'reembolso/form_reembolso.html', {'diaria': diaria,'formset':formset,'form':form})

@has_role_decorator(['digitador'])
def reembolso_update(request, id):
   diaria=get_object_or_404(Diaria,id=id)
    
   if not diaria:
        return Http404()
    
   if request.method == 'POST':
        formset=ReembolFormSet(request.POST,instance=diaria,prefix='reembolso')
        form=DescricaoReembolsoForm(request.POST or None,instance=diaria,prefix='reembolso_diaria')

        if formset.is_valid() and form.is_valid():
            form.save()
            formset.save()
            messages.add_message(request,constants.SUCCESS,'Dados atualizado com sucesso')
            return redirect('despesas:list-reembolso')
        

   formset=ReembolFormSet(request.POST or None,instance=diaria,prefix='reembolso')
   form=DescricaoReembolsoForm(request.POST or None,instance=diaria,prefix='reembolso_diaria')

   return render(request, 'reembolso/form_reembolso.html', {'diaria': diaria,'formset':formset,'form':form})

class ReembolsoListView(HasRoleMixin,ListView):
   
   model=Diaria
   template_name='reembolso/list_reembolso.html'
   context_object_name='diarias'
   queryset=Diaria.objects.select_related('profissional').filter(reembolso=1)
   ordering='-created_at'
   paginate_by=10
   allowed_roles=['digitador','coordenador','secretario']
   
class ReembolsoSearchListView(HasRoleMixin,ListView):
   model=Diaria
   template_name='reembolso/list_reembolso.html'
   context_object_name='diarias'
   paginate_by=10
   allowed_roles=['digitador','coordenador','secretario']

   def get_queryset(self, *args, **kwargs):
        qs = super(ReembolsoSearchListView,self).get_queryset(*args, **kwargs)
        buscar=self.request.GET.get('buscar',None)
        data=self.request.GET.get('data',None)
        
        if buscar:
            qs=qs.select_related('profissional')\
                .filter(reembolso=1).filter(Q(profissional__nome_completo__icontains=buscar)| Q(profissional__cpf__icontains=buscar)).order_by('-created_at')
        
        if data:
             qs=qs.select_related('profissional')\
                .filter(reembolso=1).filter(data_diaria__iexact=data).order_by('-created_at')
            
        return qs 

class ReembolsoDetailView(HasRoleMixin,DetailView):
    model=Diaria
    template_name='reembolso/detail_reembolso.html'
    allowed_roles=['digitador','coordenador','secretario']

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        diaria=Diaria.objects.select_related('profissional').get(id=self.kwargs['pk'])
        context['diaria']=diaria
        context['reembolsos'] =Reembolso.objects.select_related('diaria').filter(diaria__id=diaria.id)
        
        return context

@has_role_decorator(['digitador','coordenador','secretario'])
def reembolso_pdf(request,id):
    context={}
    diaria=get_object_or_404(Diaria,id=id)
    User=get_user_model()
   
    context['diaria']=diaria
    context['reembolsos'] =diaria.reembolsos.all().select_related('diaria')
    context['profissional']=User.objects.filter(is_active=True).filter(perfil='5').first()
    
    buffer = BytesIO()
    html_string = render_to_string('reembolso/pdf_reembolso.html', context)
    HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(buffer)
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="Reembolso_{id}.pdf"'

    return response
    
   