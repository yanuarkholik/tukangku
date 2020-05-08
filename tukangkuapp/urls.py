from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


from .views import (
    index, 
    landing,
    register,
    registerForm,
    profile,
    home,  
    pesan,
    minta,
    daftar,
    list_baru,
    list_populer,
    Search,
)

urlpatterns = [
    # Childs
    path('home/', home, name='home'),
    path('contact/', pesan, name='pesan' ),
    path('request/', minta, name='minta'),
    path('daftar/', daftar, name='daftar'),
    path('list-terbaru/', list_baru, name='list_baru'),
    path('list-terpopuler/', list_populer, name='list_populer'),
    path('registerForm/', registerForm, name='registerForm'),

    # Parents
    path('', landing, name='landing'),
    path('index/', index, name='index'),
    path('profile/', profile, name='profile'),
    path('search/', Search, name='search'),
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='landing.html'), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
