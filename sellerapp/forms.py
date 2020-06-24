from django.forms import ModelForm
from django import forms

from sellerapp.models import (
    ProInfo,
    Gigs,
    Images,
    SellerGigsImage,
    RequestDirectAuthor,
)

from tukangkuapp.models import (
    Profile
)

class BecomeSellerForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'

class GigsForm(forms.ModelForm):
    class Meta:
        model = Gigs
        fields = '__all__'

class RequestDirectAuthorForm(forms.ModelForm):
    class Meta:
        model = RequestDirectAuthor
        fields = ['deskripsi_singkat', 'paket', 'document']
