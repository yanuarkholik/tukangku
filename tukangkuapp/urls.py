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
    CreateRequest,
    DetailUpdatePermintaan,
    DetailDeleteView,

)
urlpatterns = [
    # Parents
    path('', landing, name='landing'),
    path('index/', index, name='index'),
    path('profile/', profile, name='profile'),
    
    # CRUD
    path('request/create/', CreateRequest.as_view(), name='request-create'),
    path('request/delete/<pk>/', DetailDeleteView.as_view(), name='delete-permintaan'),

    # Childs    
    path('home/', home, name='home'),
    path('register/', registerForm, name='registerForm'),
    path('detail/<str:username>/<pk>/', detail_permintaan, name='details'),
    path('detail/<pk>/', DetailUpdatePermintaan.as_view(), name='detail-permintaan'),
    path('logout/', auth_views.LogoutView.as_view(template_name='landing.html'), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='tukangkuapp/login.html'), name='login'),

    # Pass Reset
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='child/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view( template_name='users/password_reset_done.html' ), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view( template_name='users/password_reset_confirm.html' ), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view( template_name='users/password_reset_complete.html' ), name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
