from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


from .views import (
    # Parents
    index, landing, register, 
    home, profile,
    
    # Childs 
    registerForm, 
    detail_permintaan,

    # Crud
    DashboardDetailView,
    DaftarDetailView, 
    CreateRequest,
    DetailUpdatePermintaan

)

from sellerapp.views import (
    Seller,
)

urlpatterns = [
    # Parents
    path('', landing, name='landing'),
    path('index/', index, name='index'),
    path('profile/', profile, name='profile'),
    
    # CRUD
    # path('post/gigs/create/', GigsFormCreate, name='gigs-create'),
    path('post/<str:username>/', DashboardDetailView, name='dashboard'),
    path('gigs/<str:username>/<slug:slug>/', DaftarDetailView.as_view(template_name='details/detail_gig.html'), name='gigs-detail'),
    path('request/create/', CreateRequest.as_view(), name='request-create'),

    # Childs    
    path('home/', home, name='home'),
    path('register/', registerForm, name='registerForm'),
    path('register/seller-registration/', Seller, name='seller-registration'),
    path('detail/<pk>/', DetailUpdatePermintaan.as_view(), name='detail-permintaan'),
    path('detail/<str:username>/<pk>/', detail_permintaan, name='details'),
    path('logout/', auth_views.LogoutView.as_view(template_name='landing.html'), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='tukangkuapp/login.html'), name='login'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
