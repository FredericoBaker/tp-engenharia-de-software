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
        
        pattern = re.compile(r'^\(?\d{2}\)? ?\d{5}-?\d{4}$')

        if not pattern.match(whatsappNumber) or len(whatsappDigits) != 11:
            raise ValidationError('Número não está no formato correto. Por favor digite um número com 11 digitos incluindo o DDD e o 9 inicial. Use o formato a seguir: XXXXXXXXXXX')
        

        return whatsappDigits
    
class CustomAuthenticationForm(AuthenticationForm):
    error_messages = {
        'invalid_login': ("A senha ou usuário está incorreto. Por favor verifique essas informações e tente novamente."),
        'inactive': ("Usuário Inativo."),
    }

class CustomMedicationCreationForm(forms.Form):
    name_field = forms.CharField(
        label="Nome do medicamento", 
        max_length=100, 
        required=True, 
        help_text="Nome do medicamento que será utilizado no tratamento."
    )

    frequency_field = forms.IntegerField(
        label="Frequência (horas)", 
        min_value=1, 
        required=True, 
        help_text="Quantidade de horas entre as dosagens."
    )
    
    dose_field = forms.CharField(
        label="Dosagem", 
        max_length=100, 
        required=True, 
        help_text="Quanto do medicamento é administrado. Por exemplo: 1 comprimido, 10 mg, etc..."
    )

    start_datetime_field = forms.SplitDateTimeField(
        label="Data de início", 
        required=True, 
        help_text="Data em que irá iniciar o tratamento com o remédio."
    )

    end_datetime_field = forms.SplitDateTimeField(
        label="Data de fim", 
        required=False,
        help_text="Última data que o remédio precisa ser aministrado."
    )

    notify_field = forms.ChoiceField(
        label="Receber avisos", 
        required=True, 
        help_text="Deseja receber lembretes de tomar o remédio pelo telefone?"
    )

    observations_field = forms.CharField(
        label="Observações", 
        required=False, 
        help_text="Informações extras sobre o acompanhamento"
    )

    class Meta():
        model = Medication
        fields = ('name', 'frequency', 'dose', 'start_datetime', 'end_date', 'observations',)
