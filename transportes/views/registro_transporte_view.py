from django.urls import reverse_lazy
from django.views.generic import CreateView,UpdateView,ListView,DeleteView,DetailView
from transportes.models import RegistroTransporte
from transportes.forms.registro_transporte_form import RegistroTransporteForm
from django.contrib.messages.views import SuccessMessageMixin

class RegistroTransporteCreateView(SuccessMessageMixin,CreateView):
    model =RegistroTransporte
    form_class=RegistroTransporteForm
    template_name='registro_transporte/form_registro_transporte.html'
    context_object_name='form'
    success_url=reverse_lazy('transportes:list-regis-transporte')
    success_message='Cadastro realizado com sucesso'

    
class RegistroTransporteUpdateView(SuccessMessageMixin,UpdateView):
    model =RegistroTransporte
    form_class=RegistroTransporteForm
    template_name='registro_transporte/form_registro_transporte.html'
    context_object_name='form'
    success_url=reverse_lazy('transportes:list-regis-transporte')
    success_message='Cadastro alterado  com sucesso'
    
       
class RegistroTransporteListView(ListView):
    model=RegistroTransporte
    template_name='registro_transporte/list_registro_transporte.html'
    context_object_name='transportes'
    paginate_by=1
    
class RegistroTransporteDetailView(DetailView):
    model=RegistroTransporte
    context_object_name='transporte'
    template_name='registro_transporte/detail_registro_transporte.html'


class RegistroTransporteDeleteView(SuccessMessageMixin, DeleteView):
    model=RegistroTransporte
    success_url=reverse_lazy('transportes:list-regis-transporte')
    success_message='Registro excluido com sucesso'
        
    def get(self, request,*args, **kwargs):
         return self.post(request, *args, **kwargs)


