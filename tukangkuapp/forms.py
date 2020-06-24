from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import Pesan, Minta, Profile, Review, PesanAuthor

from sellerapp.models import RequestDirectAuthor

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
        fields = ['image', 'deskripsi']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['review', 'author','nama', 'gambar']

class RequestDirectAuthorForm(forms.ModelForm):
    class Meta:
        model = RequestDirectAuthor
        fields = '__all__'


class PesanForm(forms.ModelForm):
    class Meta:
        model = Pesan
        fields = '__all__'

class PesanAuthorForm(forms.ModelForm):
    class Meta:
        model = PesanAuthor
        fields = '__all__'

class MintaForm(forms.ModelForm):
    class Meta:
        model = Minta
        fields = '__all__'