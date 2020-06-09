from django.contrib import admin

from .models import Pesan, Minta, Profile, Review, PesanAuthor

from sellerapp.models import RequestDirectAuthor
# Custom Column

@admin.register(RequestDirectAuthor)
class RequestDirectAuthorAdmin(admin.ModelAdmin):  
    list_display = ('user','judul','buat', 'id')
    ordering = ('-buat',)
    search_fields = ()

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):  
    list_display = ('user','buat', 'id')
    ordering = ('-buat',)
    search_fields = ()

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):  
    list_display = ('author', 'review','buat', 'id')
    ordering = ('-buat',)
    search_fields = ('author',)

@admin.register(PesanAuthor)
class PesanAuthorAdmin(admin.ModelAdmin):  
    list_display = ('judul', 'kontak', 'upah', 'author', 'buat', 'id')
    ordering = ('-buat',)
    search_fields = ('author',)

@admin.register(Pesan)
class PesanAdmin(admin.ModelAdmin):  
    list_display = ('nama', 'email', 'subjek', 'pesan', 'id')
    ordering = ('nama',)
    search_fields = ('nama', 'subjek',)

@admin.register(Minta)
class MintaAdmin(admin.ModelAdmin):  
    list_display = ('judul', 'kontak', 'upah', 'user', 'buat', 'id')
    prepopulated_fields = {'slug': ('judul',)}
    ordering = ('-buat',)
    search_fields = ('judul',)