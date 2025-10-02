
from django import forms
from django.forms import ValidationError, inlineformset_factory
from especialidades.models import AtendimentoEspecialidade
from django.utils import timezone
from datetime import date,timedelta
from datetime import date, timedelta

class AtendimentoEspecialidadeForm(forms.ModelForm):

    data = forms.DateField(
        label='Data',
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'type': 'date',
            }),
        input_formats=('%Y-%m-%d',),
    )
    observacao=forms.CharField(label='Observação', required=False, widget=forms.Textarea( attrs={'rows':3,'cols':10}))

   
   
    class Meta:
        
        model=AtendimentoEspecialidade
        exclude=('criado_por','alterado_por',)

    def clean(self):
        
        cleaned_data = super().clean()
        data=cleaned_data.get('data')
        especialidade=cleaned_data.get('especialidade')
        hoje=date.today()
        limite_minimo=hoje-timedelta(days=30)
        limite_maximo=hoje+timedelta(days=30)
        
        
        if data:
                if  data < limite_minimo:
                    if not self.instance.pk:
                        self.add_error(
                            f"data","A data do atendimento deve estar entre 30 dias antes e 30 dias depois da data atual."
                        )
                
        #qs=AtendimentoEspecialidade.objects.filter(data=data,especialidade__nome=especialidade)
        
        """if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
                
        if qs.exists():
                print('test')
                self.add_error(f"data",'Já existe um atendimento especialidade com essa data. ')"""
                        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['hora'].widget.attrs.update({'class':'mask-hora'})
      
  
class GerarPDFAtendimentoForm(forms.Form):
    
    ORDEM=(
        
        ('1','Nome (A - Z)'),
        ('2','Nome (Z - A)'),
        ('3','Horário (00:00 - 23:59)'),
        ('4','Horário (23:59 - 00:00)'),
        ('5','Procedimento (A - Z)'),
        ('5','Procedimento (Z - A)'),

    )
    ordenar=forms.ChoiceField(label='Ordenar por ',required=True, widget=forms.Select,choices=ORDEM)


 

       