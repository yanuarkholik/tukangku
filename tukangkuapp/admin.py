from django.contrib import admin
from django.contrib.admin.filters import RelatedOnlyFieldListFilter

from .models import Profile, PesanAuthor

from sellerapp.models import RequestDirectAuthor, Request
# Custom Column

@admin.register(RequestDirectAuthor)
class RequestDirectAuthorAdmin(admin.ModelAdmin):  
    list_display = ('user','judul','buat', 'id')
    ordering = ('-buat',)
    search_fields = []

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):  
    list_display = ('user','buat', 'id')
    ordering = ('-buat',)
    search_fields = []

@admin.register(PesanAuthor)
class PesanAuthorAdmin(admin.ModelAdmin):  
    list_display = ('nama_depan','nama_belakang', 'kontak', 'buat', 'id')
    ordering = ('-buat',)
    search_fields = ['author',]

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('oleh', 'nama_depan', 'nama_belakang', 'email', 'kontak', 'provinsi', 'kota', 'status', 'buat', 'id')
    ordering = ('-buat',)
    list_filter = (
        ('services'),
        ('status'),
    )