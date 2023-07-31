from django.db.models import ProtectedError, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView, ListView

from tfds.forms.form_tfd import CodigoSIASet, RecibcoTFDForm
from tfds.models import CodigoSIA, ReciboTFD


def reciboTFDCreate(request):
    tfd=ReciboTFD()
    if request.method == 'POST':

        form = RecibcoTFDForm(request.POST,instance=tfd,prefix='recibo' )
        formset=CodigoSIASet(request.POST,instance=tfd,prefix='codigo')
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('tfds:list-recibo_tfd')

    form = RecibcoTFDForm(request.POST or None,instance=tfd,prefix='recibo')
    formset=CodigoSIASet(request.POST or None,instance=tfd,prefix='codigo')
    
    return render(request, 'recibo_tfd/form_recibo_tfd.html', {'form': form,'formset':formset})
    
def reciboTFDUpdate(request,id):
    recibo_tfd=get_object_or_404(ReciboTFD, pk=id)

    if request.method =='POST':
        form=RecibcoTFDForm(request.POST, instance=recibo_tfd,prefix='recibo')
        formset=CodigoSIASet(request.POST, instance=recibo_tfd,prefix='codigo')
        if form.is_valid() and formset.is_valid():
           form.save()
           formset.save()
           return redirect('tfds:list-recibo_tfd')

    form=RecibcoTFDForm(request.POST or None, instance=recibo_tfd,prefix='recibo')
    formset=CodigoSIASet(request.POST or None, instance=recibo_tfd,prefix='codigo')
    return render(request, 'recibo_tfd/form_recibo_tfd.html', {'form': form,'formset':formset})

class ReciboTFDListView(ListView):

    model=ReciboTFD
    template_name='recibo_tfd/list_recibos_tfds.html'
    context_object_name='recibos_tfds'
    
    def get_queryset(self, *args, **kwargs):
        qs = super(ReciboTFDListView,self).get_queryset(*args, **kwargs)
        qs=qs.select_related('paciente','acompanhante').order_by('-data')[:10]
        return qs
    
class ReciboTFDSearchListView(ListView):
   
    model=ReciboTFD
    template_name='recibo_tfd/list_recibos_tfds.html'
    context_object_name='recibos_tfds'
    paginate_by=10
    
    def get_queryset(self, *args, **kwargs):
        qs = super(ReciboTFDSearchListView,self).get_queryset(*args, **kwargs)
        search_nome_cpf=self.request.GET.get('search_nome_cpf',None)
        data=self.request.GET.get('data',None)
      
        if search_nome_cpf and data:
            queryset=qs.select_related('paciente','acompanhante').filter(Q(paciente__nome_completo__icontains=search_nome_cpf)| Q(paciente__cpf__icontains=search_nome_cpf))\
                .filter(data__iexact=data).order_by('-data')
            return queryset
        
        elif search_nome_cpf:
            queryset=qs.select_related('paciente','acompanhante').filter(Q(paciente__nome_completo__icontains=search_nome_cpf)| Q(paciente__cpf__icontains=search_nome_cpf))\
            .order_by('-data')
            return queryset
        
        elif data:
             queryset=qs.select_related('paciente','acompanhante').filter(data__iexact=data).order_by('-data')
             return queryset

class ReciboTFDDetailView(DetailView):

    model=ReciboTFD
    template_name='recibo_tfd/detail_recibo_tfd.html'
    
    def get_context_data(self,*args, **kwargs):
        context=super().get_context_data(*args, **kwargs)
        recibo_tfd= ReciboTFD.objects.select_related('paciente','acompanhante').get(id=self.kwargs['pk'])
        
        context['recibo_tfd']=recibo_tfd
        context['recibo_codigo']=CodigoSIA.objects.select_related('recibo_tfd').filter(recibo_tfd__id=recibo_tfd.id)
        
        return context

class ReciboTFDDeleteView(DeleteView):

    model=ReciboTFD
    success_url=reverse_lazy('tfds:list-recibo_tfd')

    def get(self, request, *args, **kwargs):
        return self.post().get(request, *args, **kwargs)
    