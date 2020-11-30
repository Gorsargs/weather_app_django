from django import forms
from .models import City
from django.forms import ModelForm,TextInput

class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ('name',)
        widgets  = {'name' : TextInput(attrs={'placeholder' : 'Your City Name', 
                    'type' : 'text', 'class' : 'search'})}
