from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import Profile

from sellerapp.models import Request

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

class UpdatePermintaan(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['nama_depan','revisi', 'bukti', 'nama_belakang', 'email', 'kontak', 'deskripsi', 'link', 'jenis_ruangan', 'services', 'jumlah_budget', 'provinsi', 'kota', 'alamat', 'feedback', 'lainnya', 'setujui', 'kepuasan']
