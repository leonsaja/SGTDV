from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, DeleteView, DetailView, ListView

from cidadao.models import Cidadao
from tfds.forms.form_tfd import CodigoSIASet, TFDForm
from tfds.models import ReciboTFD


def tfdcadastro(request):
    tfd=ReciboTFD()
    if request.method == 'POST':

        form = TFDForm(request.POST,instance=tfd,prefix='recibo' )
        formset=CodigoSIASet(request.POST,instance=tfd,prefix='codigo')
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('tfd:list-tfd')

    form = TFDForm(request.POST or None,instance=tfd,prefix='recibo')
    formset=CodigoSIASet(request.POST or None,instance=tfd,prefix='codigo')
    
    return render(request, 'tfd/form_tfd.html', {'form': form,'formset':formset})
    

def editartfd(request,id):
    recibo_tfd=get_object_or_404(ReciboTFD, pk=id)

    if request.method =='POST':
        form=TFDForm(request.POST, instance=recibo_tfd,prefix='recibo')
        formset=CodigoSIASet(request.POST, instance=recibo_tfd,prefix='codigo')
        if form.is_valid() and formset.is_valid():
           form.save()
           formset.save()
           return redirect('tfd:list-tfd')

    form=TFDForm(request.POST or None, instance=recibo_tfd,prefix='recibo')
    formset=CodigoSIASet(request.POST or None, instance=recibo_tfd,prefix='codigo')
    return render(request,'tfd/form_tfd.html',{'form':form,'formset':formset})

def listatfd(request):
    recibos=ReciboTFD.objects.all()
    print('recibos',recibos)
    return render(request,'tfd/list_tfd.html',{'recibos':recibos})

class DetailReciboTFDView(DetailView):

    model=ReciboTFD
    template_name='tfd/detail_tfd.html'
    
    def get_context_data(self,*args, **kwargs):
        context=super().get_context_data(*args, **kwargs)

        context['title']='Recibo de Pagamento de TFD'
        context['recibo']=ReciboTFD.objects.get(id=self.kwargs['pk'])
        print('recibo',context['recibo'])
        print('teste')
        return context


    