from django.forms import ModelForm
from django import forms

from sellerapp.models import (
    ProInfo,
    Gigs,
    SellerGigsImage,
    RequestDirectAuthor,
)

class BecomeSellerForm(forms.ModelForm):
    class Meta:
        model = ProInfo
        fields = '__all__'

class GigsForm(forms.ModelForm):
    class Meta:
        model = Gigs
        fields = '__all__'

class SellerImageDisplayForm(forms.ModelForm):
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = SellerGigsImage
        fields = ['images', 'file_field']

class RequestDirectAuthorForm(forms.ModelForm):
    class Meta:
        model = RequestDirectAuthor
        fields = ['deskripsi_singkat', 'paket', 'document']
