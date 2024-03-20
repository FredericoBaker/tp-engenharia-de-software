from django import forms
from django.contrib.auth.forms import UserCreationForm

from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm

from .models import User
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