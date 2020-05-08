from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import Daftar, Pesan, Minta

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

class DaftarForm(ModelForm):
    class Meta:
        model = Daftar
        fields = '__all__'

class PesanForm(ModelForm):
    class Meta:
        model = Pesan
        fields = '__all__'

class MintaForm(ModelForm):
    class Meta:
        model = Minta
        fields = '__all__'