from django import forms
from .models import Agenda

class AgendamentoForm(forms.ModelForm):
    notes=forms.CharField(label='Descrição', required=True, widget=forms.Textarea( attrs={'rows':3,'cols':10}))

    class Meta:
        model = Agenda
        exclude=('user',)
        widgets = {
            'title': forms.TextInput(attrs={'id': 'id_title'}),
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'id': 'id_start_time'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'id': 'id_end_time'}),
            
        }