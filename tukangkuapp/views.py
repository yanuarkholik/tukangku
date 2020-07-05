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
    UserUpdateForm, 
    ProfileUpdateForm, 
    UpdatePermintaan,
)

from .models import ( 
    Profile, 
)

from sellerapp.models import ( 
    Request,
    Invoice,
    Images
)

################################ CETAK INVOICE ################################ 

from io import StringIO, BytesIO
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
import cgitb


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    context = Context(context_dict)
    html  = template.render(context_dict)
    result = BytesIO()

    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('Ada yang error nich<pre>%s</pre>' % escape(html))

def cetakPDF(request, pk):
    gig = Request.objects.filter(pk=pk)
    return render_to_pdf( 'invoice/invoice.html', { 'pagesize':'A4', 'gig': gig}, )
################################ PARENTS ################################ 

def index(request):
    """ Parent page: Index """
    drop =  Request.objects.all()
    context = {
        'drop': drop,
    }
    return render(request, 'index.html', context)

def landing(request):
    """ Parent page: Landing """
    drop =  Images.objects.all()
    context = {
        'drop': drop,
    }
    return render(request, 'landing.html', context)

def register(request):
    """ Parent page: Register """
    return render(request, 'tukangkuapp/register.html')


################################ CHILDS ################################ 

def home(request):
    """ Menampilkan konten pada Home """
    # gigs = Request.objects.filter(status='Selesai')
    gigs    = Images.objects.all().order_by('-id')
    puas    = Invoice.objects.all().order_by('-id')
    context = {
        'gigs': gigs,
        'puas': puas
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

    def form_valid(self, form):
        form.instance.oleh = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.oleh:
            return True
        return False

class DetailDisplay(DetailView):
    model = Request

    # def get_queryset(self):
    #     ins = Invoice.objects.get(pk=id)
    #     content = { 'ins': ins}
    #     return context

# def detail_permintaan(request, username, pk):
#     """ Menampilkan detail Permintaan dan Update Permintaan """
#     ins = Invoice.objects.filter(pk=pk)
#     context = {
#         'ins':ins,
#     }
#     return render(request, 'details/detail.html', context)

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

    posts = Request.objects.filter(oleh=request.user)
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'posts': posts,
    }

    return render(request, 'tukangkuapp/profile.html', context)

################################ CRUD ################################ 

# REQUEST
class CreateRequest(CreateView):
    """ Membuat pesanan pasa Request """
    model = Request
    template_name = 'child/pesan.html'
    fields = ['nama_depan', 'nama_belakang', 'email', 'kontak', 'deskripsi', 'link', 'jenis_ruangan', 'services', 'jumlah_budget', 'provinsi', 'kota', 'alamat', 'lainnya']
    
    def form_valid(self, form):
        form.instance.oleh = self.request.user
        return super().form_valid(form)

class DetailUpdatePermintaan(DetailView, LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """ Mengupdate pesanan pada detail view """
    model = Request
    form_class = UpdatePermintaan
    template_name = 'details/detail_permintaan.html'

    def get_context_data(self, **kwargs):
        context = super(DetailUpdatePermintaan, self).get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def form_valid(self, form):
        form.instance.oleh = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.oleh:
            return True
        return False

class DetailDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """ Cancel pemesanan pada """
    model = Request
    success_url = '/profile/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.oleh:
            return True
        return False