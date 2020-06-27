from django.contrib.auth.models import User
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
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
    Images,
    ProInfo,
    AlbumTukang,
    SellerGigsImage,
    RequestDirectAuthor,
)

from sellerapp.forms import (
    GigsForm,
    BecomeSellerForm,
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
def home(request):
    """ Menampilkan konten pada Home """
    gigs = Gigs.objects.order_by('-buat')
    context = {'gigs': gigs}
    return render(request, 'child/home.html', context)

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

    posts = Gigs.objects.filter(user=request.user)
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'posts': posts,
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

def GigsFormCreate(request):
    """ Membuat Form Gig untuk Seller """
    if request.method == 'POST':
        form = GigsForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('/profile/')
    else:
        form = GigsForm(instance=request.user.profile)
    context = {
        'form': form,
    }
    return render(request, 'create/gig_create.html', context)
    

class RequestCekUlang(ListView, LoginRequiredMixin):
    """ Menampilkan hasil Request pada Author """
    model = RequestDirectAuthor
    context_object_name = 'posts'
    success_url = '/post/order/selesai/<int:pk>/'
    template_name = 'child/request_cek.html'

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

def DashboardDetailView(request, username):
    """ Menampilkan detail author dan daftar gigs pada author """
    author  = get_object_or_404(User, username=username)
    gigs    = Gigs.objects.filter(user=author)
    req     = PesanAuthor.objects.filter(user=author).order_by('-id')
    if request.method == 'POST':
        msg = PesanAuthorForm(request.POST, instance=request.user)
        if msg.is_valid() :
            deskripsi   = request.POST.get('deskripsi')
            nama        = request.POST.get('nama')
            link        = request.POST.get('link')
            kontak      = request.POST.get('kontak')
            upah        = request.POST.get('upah')
            authors      = PesanAuthor.objects.create(author=username, user=request.user, deskripsi=deskripsi, link=link, kontak=kontak)
            authors.save()
            return HttpResponseRedirect('/home/')
    else :
         msg = PesanAuthorForm(request.POST)
    context = {
        'posts': gigs,
        'form': msg,
    }
    return render(request, 'details/dashboard_detail.html', context)
    # model = Gigs
    # context_object_name = 'posts'
    # form_class = RequestDirectAuthorForm
        

    # def get_context_data(self, **kwargs):
    #     context = super(DashboardDetailView, self).get_context_data(**kwargs)
    #     context['form'] = self.get_form()
    #     return context

    # def post(self, request, *args, **kwargs):
    #     return FormView.post(self, request, *args, **kwargs)

class DaftarDetailView(DetailView, FormView):
    """ Menampilkan slug pada url ke Daftar Detail """
    model = Gigs
    form_class = PesanAuthorForm
    context_object_name = 'gigs'
    slug_url_kwarg = 'slug'
    slug_field = 'slug'
    username = 'username'
    
    def get_context_data(self, **kwargs):
        context = super(DaftarDetailView, self).get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            form.instance.author = self.username
            form.instance.user = self.request.user.profile
            return self.form_valid(form)
        else:
            return self.form_invalid(form)  
    
    def form_valid(self, form):
        return super(DaftarDetailView, self).form_valid(form)

    def form_invalid(self, form):
        #put logic here
        return super(DaftarDetailView, self).form_invalid(form)

class DaftarListView(ListView):
    """ List daftar gigs pada profile """
    model = Gigs
    template_name = 'tukangkuapp/profile.html'

    def get_context_data(self, request, **kwargs):
        context = super( DaftarListView, self).get_context_data(**kwargs)
        context['daftar'] = Gigs.objects.filter(user=request.user)
        return context

# class MintaCreateView(CreateView):
#     """ Membuat Request Job Dari User Untuk Seller """
#     model   = Minta
#     fields  = ['judul', 'kontak', 'upah', 'deskripsi', 'file']
    
#     def form_valid(self, form):
#         form.instance.author = self.request.author
#         return super().form_valid(form)

# class PesanAuthorCreateView(LoginRequiredMixin, CreateView):
#     """ Membuat Massage Dari User Untuk Seller """
#     model = PesanAuthor
#     fields  = ['user', 'kontak', 'upah', 'deskripsi', 'file']

#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         return super().form_valid(form)

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

# class MintaUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
#     """ Membuat update data pada Minta  """
#     model = Minta
#     fields = ['judul', 'kontak', 'upah', 'deskripsi', 'file']

#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         return super().form_valid(form)

#     def test_func(self):
#         minta = self.get_object()
#         if self.request.user == minta.author:
#             return True
#         return False

# class MintaDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
#     """ Menghapus data Minta yang dipilih dan kembali ke Home """
#     model = Minta
#     success_url = '/post/'

#     def test_func(self):
#         minta = self.get_object()
#         if self.request.user == minta.author:
#             return True
#         return False


