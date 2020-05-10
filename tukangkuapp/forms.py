from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import Daftar, Pesan, Minta, Profile

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

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