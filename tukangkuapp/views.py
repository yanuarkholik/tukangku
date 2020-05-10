from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, ListView 
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


from .forms import DaftarForm, PesanForm, MintaForm, SignUpForm, UserUpdateForm, ProfileUpdateForm
from .models import Daftar, Pesan, Minta, Profile

# Parent
def index(request):
    return render(request, 'index.html')

def landing(request):
    return render(request, 'landing.html')

def register(request):
    return render(request, 'users/register.html')

# Child
def minta(request):
    mintakonten = Minta.objects.order_by('-buat')[:4]
    form = MintaForm()
    if request.method == 'POST':
        form = MintaForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("minta"))

    context = { 'form': form, 'request': minta }
    return render(request, 'child/request.html', context)

def daftar(request):
    form = DaftarForm()
    if request.method == 'POST':
        form = DaftarForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("daftar"))
    context = { 'form': form }
    return render(request, 'child/daftar.html', context)

def home(request):
    profile = Daftar.objects.order_by('-buat')[:4]
    context = {'profile': profile}
    return render(request, 'child/home.html', context)

def pesan(request):
    form = PesanForm()
    if request.method == 'POST':
        form = PesanForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("pesan"))

    context = {'form': form}
    return render(request, 'child/pesan.html', context)

def list_baru(request):
    terbaru = Daftar.objects.order_by('-buat')
    count_terbaru = Daftar.objects.all().count()
    context = {'baru': terbaru, 'count': count_terbaru }
    return render(request, 'child/list_baru.html', context)

def list_populer(request):
    terpopuler = Daftar.objects.order_by('-buat')
    context = {'populer': terpopuler}
    return render(request, 'child/list_populer.html', context)

def registerForm(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)

# CRUD

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)


class MintaListView(ListView):
    model = Minta
    template_name = 'child/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']


class MintaDetailView(DetailView):
    model = Minta


class MintaCreateView(LoginRequiredMixin, CreateView):
    model = Minta
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class MintaUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Minta
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        minta = self.get_object()
        if self.request.user == minta.author:
            return True
        return False


class MintaDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Minta
    success_url = '/'

    def test_func(self):
        minta = self.get_object()
        if self.request.user == minta.author:
            return True
        return False


