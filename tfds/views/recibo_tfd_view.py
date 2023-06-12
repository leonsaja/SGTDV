from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView

from tfds.forms.form_tfd import CodigoSIASet, TFDForm
from tfds.models import CodigoSIA, ReciboTFD


def reciboTFDCreate(request):
    tfd=ReciboTFD()
    if request.method == 'POST':

        form = TFDForm(request.POST,instance=tfd,prefix='recibo' )
        formset=CodigoSIASet(request.POST,instance=tfd,prefix='codigo')
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('tfds:list-recibo_tfd')

    form = TFDForm(request.POST or None,instance=tfd,prefix='recibo')
    formset=CodigoSIASet(request.POST or None,instance=tfd,prefix='codigo')
    
    return render(request, 'recibo_tfd/form_recibo_tfd.html', {'form': form,'formset':formset})
    
def reciboTFDUpdate(request,id):
    recibo_tfd=get_object_or_404(ReciboTFD, pk=id)

    if request.method =='POST':
        form=TFDForm(request.POST, instance=recibo_tfd,prefix='recibo')
        formset=CodigoSIASet(request.POST, instance=recibo_tfd,prefix='codigo')
        if form.is_valid() and formset.is_valid():
           form.save()
           formset.save()
           return redirect('tfds:list-recibo_tfd')

    form=TFDForm(request.POST or None, instance=recibo_tfd,prefix='recibo')
    formset=CodigoSIASet(request.POST or None, instance=recibo_tfd,prefix='codigo')
    return render(request, 'recibo_tfd/form_recibo_tfd.html', {'form': form,'formset':formset})

class ReciboTFDListView(ListView):
    model=ReciboTFD
    template_name='recibo_tfd/list_recibos_tfds.html'
    
    def get_context_data(self, *args, **kwargs):
        context=super().get_context_data(*args, **kwargs)
        context['recibos_tfds']=ReciboTFD.objects.select_related('paciente','acompanhante').all()
        
        return context
   
class ReciboTFDDetailView(DetailView):

    model=ReciboTFD
    template_name='recibo_tfd/detail_recibo_tfd.html'
    
    def get_context_data(self,*args, **kwargs):
        context=super().get_context_data(*args, **kwargs)
        recibo_tfd= ReciboTFD.objects.select_related('paciente','acompanhante').get(id=self.kwargs['pk'])
        
        context['recibo_tfd']=recibo_tfd
        context['recibo_codigo']=CodigoSIA.objects.select_related('recibo_tfd').filter(recibo_tfd__id=recibo_tfd.id)
        
        return context


    