from django.contrib import admin

from .models import Daftar, Pesan, Minta, Profile, Review, PesanAuthor, PostDaftarImage
# Custom Column

class PostImageAdmin(admin.TabularInline):
    model = PostDaftarImage

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):  
    list_display = ('user','buat','deskripsi', 'id')
    ordering = ('-buat',)
    search_fields = ()

@admin.register(Daftar)
class DaftarAdmin(admin.ModelAdmin):  
    inlines = [
        PostImageAdmin,
        ]
    list_display = ('author','posisi','deskripsi','buat', 'id')
    ordering = ('-buat',)
    search_fields = ()

    class Meta:
           model = Daftar

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
    list_display = ('judul', 'kontak', 'upah', 'author', 'buat', 'id')
    ordering = ('-buat',)
    search_fields = ('judul',)