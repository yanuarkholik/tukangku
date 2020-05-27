from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


from .views import (
    index, landing, register, home, profile,
    
    pesan, list_baru, list_populer, registerForm, reviewForm, 

    MintaDetailView, MintaUpdateView, MintaDeleteView, DashboardDetailView,
    DaftarDetailView, MintaCreateView, PesanAuthorCreateView, DaftarUpdateView,
    TukangAllListView,
)

urlpatterns = [
    # Childs
    path('post/', home, name='home'),
    path('contact/', pesan, name='pesan' ),
    path('list-terbaru/', list_baru, name='list_baru'),
    path('list-terpopuler/', list_populer, name='list_populer'),
    path('registerForm/', registerForm, name='registerForm'),
    path('reviewForm/', reviewForm, name='reviewForm'),

    # CRUD
    path('post/request/<slug:slug>/', MintaDetailView.as_view(), name='minta-detail'),
    path('post/create/', MintaCreateView.as_view(template_name='child/request.html'), name='minta'),
    path('post/dashboard/seller/msg/<int:pk>/', PesanAuthorCreateView.as_view(template_name='tukangkuapp/pesanauthor.html'), name='pesan-user'),
    path('post/seller/pesan/', MintaCreateView.as_view(template_name='tukangkuapp/dashboard_detail.html'), name='minta-create'),
    path('post/<int:pk>/update/', MintaUpdateView.as_view(), name='minta-update'),
    path('profile/daftar/<int:pk>/update/', DaftarUpdateView.as_view(template_name='tukangkuapp/daftar_update.html'), name='daftar-update'),
    path('post/<int:pk>/delete/', MintaDeleteView.as_view(), name='minta-delete'),

    # Parents
    path('', landing, name='landing'),
    path('index/', index, name='index'),
    path('profile/', profile, name='profile'),
    path('register/', register, name='register'),
    path('post/mytukang/', TukangAllListView.as_view(), name='all-tukang'),
    path('post/<str:username>/', DashboardDetailView.as_view(template_name='tukangkuapp/dashboard_detail.html'), name='dashboard'),
    path('post/gigs/<slug:slug>/', DaftarDetailView.as_view(template_name='tukangkuapp/daftar_detail.html'), name='daftar-detail'),
    path('login/', auth_views.LoginView.as_view(template_name='tukangkuapp/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='landing.html'), name='logout'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
