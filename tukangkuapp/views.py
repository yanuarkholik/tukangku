from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse, reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, ListView 
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm


from .forms import (
    DaftarForm, 
    PesanForm, 
    MintaForm, 
    SignUpForm, 
    UserUpdateForm, 
    ProfileUpdateForm, 
    ReviewForm, 
    PesanAuthorForm,
    RequestDirectAuthorForm
)

from .models import ( 
    Daftar, 
    Pesan, 
    Minta, 
    Profile, 
    PesanAuthor, 
    PostDaftarImage,
    RequestDirectAuthor,
)

# Parent
def index(request):
    """ Parent page: Index """
    return render(request, 'index.html')

def landing(request):
    """ Parent page: Landing """
    return render(request, 'landing.html')

def register(request):
    """ Parent page: Register """
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
    """ Menampilkan list baru dari Daftar """
    terbaru = Daftar.objects.order_by('-buat')
    count_terbaru = Daftar.objects.all().count()
    context = {'baru': terbaru, 'count': count_terbaru }
    return render(request, 'child/list_baru.html', context)

def list_populer(request):
    """ Menampilkan list populer dari Daftar """
    terpopuler = Daftar.objects.order_by('-buat')
    count_terbaru = Daftar.objects.all().count()
    context = {'populer': terpopuler, 'count': count_terbaru}
    return render(request, 'child/list_populer.html', context)

def registerForm(request):
    """ Membuat Form Register akun MyTukang """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
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
    """ Menampilkan konten pada User Profile """
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

    posts = Daftar.objects.filter(user=request.user)
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'posts': posts,
    }

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

class RequestDirectForm(CreateView, LoginRequiredMixin):
    """ Membuat Request Langsung pada Author oleh User """
    model = RequestDirectAuthor
    slug_url_kwarg = 'slug'
    slug_field = 'slug'
    fields  = ['deskripsi', 'files']

    def form_valid(self, form):
        form.instance.author    = self.request.user
        form.instance.to_author = self.request.user
        return super().form_valid(form)

    

class RequestCekUlang(ListView):
    """ Menampilkan hasil Request pada Author """
    model = RequestDirectAuthor
    context_object_name = 'posts'
    template_name = 'child/request_cek.html'

def home(request):
    """ Menampilkan konten pada Home """
    profile = Daftar.objects.order_by('-buat')[:5]
    minta   = Minta.objects.order_by('-buat')[:5]
    carousel= PostDaftarImage.objects.all()
    context = {'profile': profile, 'request': minta, 'carousel': carousel}
    return render(request, 'child/home.html', context)

class TukangAllListView(ListView):
    model = Daftar
    template_name = 'child/tukang_all.html'

    def get_context_data(self, **kwargs):
        context = super(TukangAllListView, self).get_context_data(**kwargs)
        context['daftar'] = Daftar.objects.all()
        return context

class MintaDetailView(DetailView):
    """ Menampilkan slug pada url ke Minta Detail """
    model = Minta
    slug_url_kwarg = 'slug'
    slug_field = 'slug'

class DashboardDetailView(ListView):
    """ Menampilkan detail author dan daftar gigs pada author """
    model = Daftar
    context_object_name = 'posts'
        
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Daftar.objects.filter(user=user).order_by('-buat')

class DaftarDetailView(DetailView):
    """ Menampilkan slug pada url ke Daftar Detail """
    model = Daftar
    context_object_name = 'posts'
    slug_url_kwarg = 'slug'
    slug_field = 'slug'

class DaftarListView(ListView):
    """ List daftar gigs pada profile """
    model = Daftar
    template_name = 'tukangkuapp/profile.html'

    def get_context_data(self, request, **kwargs):
        context = super( DaftarListView, self).get_context_data(**kwargs)
        context['daftar'] = Daftar.objects.filter(user=request.user)
        return context

class MintaCreateView(CreateView):
    """ Membuat Request Job Dari User Untuk Seller """
    model   = Minta
    fields  = ['judul', 'kontak', 'upah', 'deskripsi', 'file']
    
    def form_valid(self, form):
        form.instance.author = self.request.author
        return super().form_valid(form)

class PesanAuthorCreateView(LoginRequiredMixin, CreateView):
    """ Membuat Massage Dari User Untuk Seller """
    model = PesanAuthor
    fields  = ['judul', 'kontak', 'upah', 'deskripsi', 'file']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class DaftarUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """ Membuat update data pada Daftar dan kembali ke Profile """
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

class MintaUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """ Membuat update data pada Minta  """
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
    """ Menghapus data Minta yang dipilih dan kembali ke Home """
    model = Minta
    success_url = '/post/'

    def test_func(self):
        minta = self.get_object()
        if self.request.user == minta.author:
            return True
        return False


