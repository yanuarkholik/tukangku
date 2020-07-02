from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    FormView,
    View
)

from .forms import ( 
    SignUpForm,  
    PesanAuthorForm,
    UserUpdateForm, 
    ProfileUpdateForm, 
    UpdatePermintaan,
)

from .models import ( 
    Profile, 
    PesanAuthor, 
)

from sellerapp.models import ( 
    Gigs,
    Images,
    Request,
)

from sellerapp.forms import (
    GigsForm,
)

# Parent
def index(request):
    """ Parent page: Index """
    drop =  Gigs.objects.all()
    context = {
        'drop': drop,
    }
    return render(request, 'index.html', context)

def landing(request):
    """ Parent page: Landing """
    drop =  Gigs.objects.all()
    context = {
        'drop': drop,
    }
    return render(request, 'landing.html', context)

def register(request):
    """ Parent page: Register """
    return render(request, 'tukangkuapp/register.html')


# Child
def home(request):
    """ Menampilkan konten pada Home """
    gigs = Request.objects.filter(status='Selesai')
    context = {
        'gigs': gigs,
    }
    return render(request, 'child/home.html', context)


class DetailUpdatePermintaan(DetailView, LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Request
    form_class = UpdatePermintaan
    template_name = 'details/detail_permintaan.html'

    def get_context_data(self, **kwargs):
        context = super(DetailUpdatePermintaan, self).get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        form.instance.pk = Request.objects.get(pk=pk)
        form.save()
        return FormView.post(self, request, *args, **kwargs)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.oleh:
            return True
        return False


@login_required
def detail_permintaan(request, username, pk):
    """ Menampilkan detail Permintaan dan Update Permintaan """
    ins = Request.objects.get(pk=pk)
    req = Request.objects.filter(pk=pk)
    context = {
        'req': req,
        'ins':ins,
    }
    return render(request, 'details/detail.html', context)

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

@login_required
def profile(request):
    """ Menampilkan konten pada User Profile """
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user, prefix='user')
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile, prefix='profile')
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return HttpResponseRedirect(reverse("profile"))
    else:
        u_form = UserUpdateForm(instance=request.user, prefix='user')
        p_form = ProfileUpdateForm(instance=request.user.profile, prefix='profile')

    posts = Request.objects.filter(oleh=request.user).order_by('status')
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'posts': posts,
    }

    return render(request, 'tukangkuapp/profile.html', context)

# CRUD

class TukangAllListView(ListView):
    model = Gigs
    template_name = 'child/tukang_all.html'

    def get_context_data(self, **kwargs):
        context = super(TukangAllListView, self).get_context_data(**kwargs)
        context['daftar'] = Gigs.objects.all()
        return context

def DashboardDetailView(request, username):
    """ Menampilkan detail author dan daftar gigs pada author """
    author  = get_object_or_404(User, username=username)
    gigs    = Gigs.objects.filter(user=author)
    if request.method == 'POST':
        msg = PesanAuthorForm(request.POST, instance=request.user)
        if msg.is_valid() :
            deskripsi   = request.POST.get('deskripsi')
            nama_depan  = request.POST.get('nama_depan')
            nama_belakang = request.POST.get('nama_belakang')
            link        = request.POST.get('link')
            kontak      = request.POST.get('kontak')
            upah        = request.POST.get('upah')
            authors      = PesanAuthor.objects.create(nama_depan=nama_depan, nama_belakang=nama_belakang, deskripsi=deskripsi, link=link, kontak=kontak)
            authors.save()
            return HttpResponseRedirect('/home/')
    else :
         msg = PesanAuthorForm(request.POST)
    context = {
        'posts': gigs,
        'form': msg,
    }
    return render(request, 'details/dashboard_detai.html', context)

class CreateRequest(CreateView):
    model = Request
    template_name = 'child/pesan.html'
    fields = ['nama_depan', 'nama_belakang', 'email', 'kontak', 'deskripsi', 'link', 'jenis_ruangan', 'services', 'jumlah_budget', 'provinsi', 'kota', 'alamat']
    
    def form_valid(self, form):
        form.instance.oleh = self.request.user
        return super().form_valid(form)

class DaftarDetailView(DetailView, FormView):
    """ Menampilkan slug pada url ke Daftar Detail """
    model = Gigs
    form_class = PesanAuthorForm
    context_object_name = 'gigs'
    slug_url_kwarg = 'slug'
    slug_field = 'slug'
    username = 'username'
    success_url = '/home/'
    
    def form_valid(self, form):
        return super().form_valid(form)

class DaftarListView(ListView):
    """ List daftar gigs pada profile """
    model = Gigs
    template_name = 'tukangkuapp/profile.html'

    def get_context_data(self, request, **kwargs):
        context = super( DaftarListView, self).get_context_data(**kwargs)
        context['daftar'] = Gigs.objects.filter(user=request.user)
        return context

