from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, ListView 
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm


from .forms import DaftarForm, PesanForm, MintaForm, SignUpForm, UserUpdateForm, ProfileUpdateForm, ReviewForm, PesanAuthorForm
from .models import Daftar, Pesan, Minta, Profile, PesanAuthor, PostDaftarImage

# Parent
def index(request):
    return render(request, 'index.html')

def landing(request):
    return render(request, 'landing.html')

def register(request):
    return render(request, 'tukangkuapp/register.html')

# Child
def pesan(request):
    form = PesanForm()
    if request.method == 'POST':
        form = PesanForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("pesan"))
    else:
        form = PesanForm()
    context = {'form': form}
    return render(request, 'child/pesan.html', context)

def list_baru(request):
    terbaru = Daftar.objects.order_by('-buat')
    count_terbaru = Daftar.objects.all().count()
    context = {'baru': terbaru, 'count': count_terbaru }
    return render(request, 'child/list_baru.html', context)

def list_populer(request):
    terpopuler = Daftar.objects.order_by('-buat')
    count_terbaru = Daftar.objects.all().count()
    context = {'populer': terpopuler, 'count': count_terbaru}
    return render(request, 'child/list_populer.html', context)

def registerForm(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'tukangkuapp/register.html', {'form': form})

def reviewForm(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('reviewForm')
    else:
        form = ReviewForm()
    
    context = { 'form': form }
    return render(request, 'tukangkuapp/review.html', context)

@login_required
def profile(request):
    posts = Daftar.objects.all()
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'posts': posts,
    }
    class DaftarDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
        model = Daftar
        success_url = '/profile/'

        def test_func(self):
            daftar = self.get_object()
            if self.request.user == daftar.author:
                return True
            return False

    return render(request, 'tukangkuapp/profile.html', context)

# CRUD
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    View
)

def home(request):
    profile = Daftar.objects.order_by('-buat')[:4]
    minta   = Minta.objects.order_by('-buat')[:4]
    context = {'profile': profile, 'request': minta}
    return render(request, 'child/home.html', context)

class MintaDetailView(DetailView):
    model = Minta

class DashboardDetailView(DetailView):
    model = Minta

    def get_context_data(self, **kwargs):
        context = super(DashboardDetailView, self).get_context_data(**kwargs)
        context['profile'] = Minta.objects.filter(pk=self.kwargs.get('pk'))
        return context

class DaftarCreateView(View):
    def get(self, request):
        photos_list = Daftar.objects.all()
        return render(self.request, 'tukangkuapp/profile.html', {'photos': photos_list})

    def post(self, request):
        form = DaftarForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            photo = form.save()
            data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)

class DaftarDetailView(DetailView):
    model = Daftar

    def get_context_data(self, **kwargs):
        context = super( DaftarDetailView, self).get_context_data(**kwargs)
        context['profile'] = Daftar.objects.filter(pk=self.kwargs.get('pk'))
        return context

class DaftarListView(ListView):
    model = Daftar
    template_name = 'tukangkuapp/profile.html'

    def get_context_data(self, request, **kwargs):
        context = super( DaftarListView, self).get_context_data(**kwargs)
        context['daftar'] = Daftar.objects.filter(user=request.author)
        return context

class MintaCreateView(CreateView):
    """ Membuat Request Job Dari User Untuk Seller """
    model   = Minta
    fields  = ['judul', 'kontak', 'upah', 'deskripsi', 'file']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PesanAuthorCreateView(LoginRequiredMixin, CreateView):
    """ Membuat Massage Dari User Untuk Seller """
    model = PesanAuthor
    fields  = ['judul', 'kontak', 'upah', 'deskripsi', 'file']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class DaftarUpdateView(UpdateView):
    model = Daftar
    fields = ['deskripsi', 'anggota', 'posisi', 'file']
    success_url = '/profile/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class DaftarDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Daftar
    success_url = '/profile/'

    def test_func(self):
        daftar = self.get_object()
        if self.request.user == daftar.author:
            return True
        return False

class MintaUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Minta
    fields = ['judul', 'kontak', 'upah', 'deskripsi', 'file']

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
    success_url = '/post/'

    def test_func(self):
        minta = self.get_object()
        if self.request.user == minta.author:
            return True
        return False


