from django import forms
from django.contrib.auth.forms import UserCreationForm

from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm

from .models import User
from .models import Medication
import re

class CustomUserCreationForm(UserCreationForm):
    whatsapp_number = forms.CharField(max_length=30, required=False, help_text='Optional.')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'whatsapp_number',)

    def clean_whatsapp_number(self):
        whatsappNumber = self.cleaned_data.get('whatsapp_number')
        whatsappDigits = re.sub(r'[^\d]', '', whatsappNumber)
        
        pattern = re.compile(r'^\(?\d{2}\)? ?\d{4}-?\d{4}$')

        if not pattern.match(whatsappNumber) or len(whatsappDigits) != 11:
            raise ValidationError('Número não está no formato correto. Por favor digite um número com 10 digitos incluindo o DDD, assim como está cadastrado no WhatsApp. Use o formato a seguir: (99) 9999-9999')
        

        return whatsappDigits
    
class CustomAuthenticationForm(AuthenticationForm):
    error_messages = {
        'invalid_login': ("A senha ou usuário está incorreto. Por favor verifique essas informações e tente novamente."),
        'inactive': ("Usuário Inativo."),
    }

class CustomMedicationCreationForm(forms.ModelForm):
    name = forms.CharField(
        label='Nome do medicamento', 
        max_length=100, 
        required=True, 
        help_text='Nome do medicamento que será utilizado no tratamento.',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Nome do medicamento',
                'title': 'Qual é o nome do medicamento que será utilizado no tratamento?',
            }
        )
    )

    frequency = forms.IntegerField(
        label='Frequência (minutos)', 
        min_value=1, 
        required=True, 
        help_text='Quantidade de minutos entre as dosagens.',
        widget=forms.NumberInput(
            attrs={
                'step': '1',
                'title': 'De quantos em quantos minutos o medicamento deve ser administrado?',
            }
        )
    )
    
    dose = forms.CharField(
        label='Dosagem', 
        max_length=100, 
        required=True, 
        help_text='Quanto do medicamento é administrado. Por exemplo: 1 comprimido, 10 mg, etc...',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Ex.: 1 comprimido, 10 mg, etc...',
                'title': 'Quanto do medicamento deve ser usado?',
            }
        )
    )

    start_datetime = forms.DateTimeField(
        label='Data de início', 
        required=True, 
        help_text='Data em que irá iniciar o tratamento com o remédio. O formato da data é: dd/mm/aaaa hh:mm.',
        widget=forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'title': 'Esta é a data em que irá iniciar o tratamento com o remédio. O formato da data é: dd/mm/aaaa hh:mm.',
            }
        )
    )

    end_datetime = forms.DateTimeField(
        label='Data de fim', 
        required=False,
        help_text='Última data que o remédio precisa ser aministrado. O formato da data é: dd/mm/aaaa hh:mm. Caso não tenha uma data de fim, deixe em branco.',
        widget=forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'title': 'Última data que o remédio precisa ser aministrado. O formato da data é: dd/mm/aaaa hh:mm. Caso não tenha uma data de fim, deixe em branco.',
            }
        )
    )

    notify = forms.BooleanField(
        label='Receber avisos', 
        required=False, 
        help_text='Deseja receber lembretes de quando tomar o remédio pelo telefone?',
        widget=forms.CheckboxInput(
            attrs={
                'type': 'checkbox',
                'title': 'Deseja receber lembretes de quando tomar o remédio pelo telefone?',
            }
        )
    )

    observations = forms.CharField(
        label='Observações', 
        required=False, 
        help_text='Informações extras sobre o tratamento',
        widget=forms.Textarea(
            attrs={
                'rows': 5,
                'maxlength': 500,
                'placeholder': 'Alguma informação a mais que gostaria de adicionar para ser lembrado?',
                'title': 'Adicione qualquer informação que julgar importante sobre o tratamento para ser lembrado.',
            }
        )
    )

    class Meta:
        model = Medication
        fields = ('name', 'frequency', 'dose', 'start_datetime', 'end_date', 'notify', 'observations')
