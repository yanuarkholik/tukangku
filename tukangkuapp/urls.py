from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


from .views import (
    # Parents
    index, landing, register, 
    home, profile,
    
    # Childs
    pesan, 
    # list_baru, list_populer, 
    registerForm, 
    # RequestSelesai,

    # Crud
    # MintaDetailView, MintaUpdateView, 
    # MintaDeleteView, 
    DashboardDetailView,
    DaftarDetailView, #MintaCreateView, 
    # PesanAuthorCreateView, 
    DaftarUpdateView,
    # TukangAllListView, RequestDirectForm,
    # RequestCekUlang, 
    GigsFormCreate,
)

from sellerapp.views import (
    Seller,
)

urlpatterns = [
    # Parents
    path('', landing, name='landing'),
    path('index/', index, name='index'),
    path('profile/', profile, name='profile'),
    path('register/', register, name='register'),
    
    # CRUD
    path('post/gigs/create/', GigsFormCreate, name='gigs-create'),
    # path('post/mytukang/', TukangAllListView.as_view(), name='all-tukang'),
    # path('post/order/<int:pk>-<slug:slug>/', RequestDirectForm, name='req-direct'),
    # path('post/<int:pk>/update/', MintaUpdateView.as_view(), name='minta-update'),
    # path('post/<int:pk>/delete/', MintaDeleteView.as_view(), name='minta-delete'),
    # path('post/request/<slug:slug>/', MintaDetailView.as_view(), name='minta-detail'),
    # # path('post/create/', MintaCreateView.as_view(template_name='child/request.html'), name='minta'),
    # path('post/order/cek/', RequestCekUlang.as_view(template_name='child/request_cek.html'), name='req-cek'),
    # path('post/seller/pesan/', MintaCreateView.as_view(template_name='tukangkuapp/dashboard_detail.html'), name='minta-create'),
    path('post/<str:username>/', DashboardDetailView, name='dashboard'),
    path('gigs/<str:username>/<slug:slug>/', DaftarDetailView.as_view(template_name='details/detail_gig.html'), name='gigs-detail'),
    path('profile/daftar/<int:pk>/update/', DaftarUpdateView.as_view(template_name='tukangkuapp/daftar_update.html'), name='daftar-update'),
    # path('post/dashboard/seller/msg/<int:pk>/', PesanAuthorCreateView.as_view(template_name='tukangkuapp/pesanauthor.html'), name='pesan-user'),

    # Childs    
    path('home/', home, name='home'),
    path('contact/', pesan, name='pesan' ),
    # path('list-terbaru/', list_baru, name='list_baru'),
    # path('list-terpopuler/', list_populer, name='list_populer'),
    path('register/', registerForm, name='registerForm'),
    # path('post/order/selesai/<int:pk>/', RequestSelesai, name='req-done'),
    path('register/seller-registration/', Seller, name='seller-registration'),
    path('logout/', auth_views.LogoutView.as_view(template_name='landing.html'), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='tukangkuapp/login.html'), name='login'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
