
from django import forms
from django.forms import ValidationError, inlineformset_factory
from especialidades.models import AtendimentoEspecialidade
from django.utils import timezone
from datetime import date

class AtendimentoEspecialidadeForm(forms.ModelForm):

    data = forms.DateTimeField(
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
        fields='__all__'

    def clean_data(self):
        data = self.cleaned_data['data']
        data_atual=date.today().strftime('%d/%m/%Y')
        data=data.strftime('%d/%m/%Y')
      
        if  data < data_atual:
            raise ValidationError("A data do atendimento não pode ser anterior à data atual.")
        return data
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['hora'].widget.attrs.update({'class':'mask-hora'})
      
  
  

 

       