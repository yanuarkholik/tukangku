from django.contrib.auth.models import User
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import TemplateView, ListView 
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    View
)

from .forms import (
    PesanForm, 
    MintaForm, 
    SignUpForm, 
    ReviewForm, 
    PesanAuthorForm,
    UserUpdateForm, 
    ProfileUpdateForm, 
    RequestDirectAuthorForm
)

from .models import ( 
    Pesan, 
    Minta, 
    Profile, 
    PesanAuthor, 
)

from sellerapp.models import ( 
    Gigs,
    ProInfo,
    SellerGigsImage,
    RequestDirectAuthor,
)

from sellerapp.forms import (
    GigsForm,
    BecomeSellerForm,
    SellerImageDisplayForm,
    RequestDirectAuthorForm,
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
    terbaru = Gigs.objects.order_by('-buat')
    count_terbaru = Gigs.objects.all().count()
    context = {'baru': terbaru, 'count': count_terbaru }
    return render(request, 'child/list_baru.html', context)

def list_populer(request):
    """ Menampilkan list populer dari Daftar """
    terpopuler = Gigs.objects.order_by('-buat')
    count_terbaru = Gigs.objects.all().count()
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
            return HttpResponseRedirect(reverse("profile"))

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    sellers = ProInfo.objects.filter(user=request.user)
    posts = Gigs.objects.filter(user=request.user)
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'posts': posts,
        'sellers': sellers,
    }

    return render(request, 'tukangkuapp/profile.html', context)

# CRUD
def RequestSelesai(request):
    """ Request Selesai """
    rincian = RequestDirectAuthor.objects.filter(auhtor=request.user)
    return render(request, 'child/request_done.html')

@login_required
def RequestDirectForm(request, slug, pk):
    """ Membuat Request Langsung pada Author oleh User """
    if request.method == 'POST':
        form = RequestDirectAuthorForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            instance = RequestDirectAuthor(document=request.FILES['document'])
            instance.save()
            return redirect('/post/order/cek/')
    else:
        form = RequestDirectAuthorForm(instance=request.user.profile)
    gigs = Gigs.objects.get(slug=slug, pk=pk)
    context = {
        'form': form,
        'gigs': gigs
    }
    return render(request, 'child/request_author.html', context)

class GigsFormCreate(CreateView):
    """ Membuat Form Gig untuk Seller """
    model = Gigs
    fields = ['user', 'judul', 'deskripsi_singkat', 'kategori', 'basic', 'standard', 'premium', 'thumbnail']
    succes_url = '/profile/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class RequestCekUlang(ListView, LoginRequiredMixin):
    """ Menampilkan hasil Request pada Author """
    model = RequestDirectAuthor
    context_object_name = 'posts'
    success_url = '/post/order/selesai/<int:pk>/'
    template_name = 'child/request_cek.html'

def home(request):
    """ Menampilkan konten pada Home """
    profile = Gigs.objects.order_by('-buat')[:5]
    minta   = Minta.objects.order_by('-buat')[:5]
    carousel= SellerGigsImage.objects.all()
    context = {'profile': profile, 'request': minta, 'carousel': carousel}
    return render(request, 'child/home.html', context)

class TukangAllListView(ListView):
    model = Gigs
    template_name = 'child/tukang_all.html'

    def get_context_data(self, **kwargs):
        context = super(TukangAllListView, self).get_context_data(**kwargs)
        context['daftar'] = Gigs.objects.all()
        return context

class MintaDetailView(DetailView):
    """ Menampilkan slug pada url ke Minta Detail """
    model = Minta
    slug_url_kwarg = 'slug'
    slug_field = 'slug'

class DashboardDetailView(ListView):
    """ Menampilkan detail author dan daftar gigs pada author """
    model = Gigs
    context_object_name = 'posts'
        
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Gigs.objects.filter(user=user).order_by('-buat')

class DaftarDetailView(DetailView):
    """ Menampilkan slug pada url ke Daftar Detail """
    model = Gigs
    context_object_name = 'posts'
    slug_url_kwarg = 'slug'
    slug_field = 'slug'

class DaftarListView(ListView):
    """ List daftar gigs pada profile """
    model = Gigs
    template_name = 'tukangkuapp/profile.html'

    def get_context_data(self, request, **kwargs):
        context = super( DaftarListView, self).get_context_data(**kwargs)
        context['daftar'] = Gigs.objects.filter(user=request.user)
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
    model = Gigs
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


