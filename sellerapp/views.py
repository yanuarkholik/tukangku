from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import TemplateView, ListView 
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from sellerapp.models import ( 
    Gigs, 
    ProInfo,
    SellerGigsImage,
)

from sellerapp.forms import (
    GigsForm,
    BecomeSellerForm,
    SellerImageDisplayForm,
)

### Seller Registration ###
@login_required
def Seller(request):
    """ Menampilkan konten pada User Profile """
    if request.method == 'POST':
        s_form = BecomeSellerForm(request.POST, instance=request.user)
        if s_form.is_valid():
            s_form.save()
            return redirect('Seller')

    else:
        s_form = BecomeSellerForm(instance=request.user)
    context = {
        's_form': s_form,
    }
    return render(request, 'sellerapp/seller_registration.html', context)

