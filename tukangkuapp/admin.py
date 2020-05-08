from django.contrib import admin

from .models import Post, Daftar, Pesan, Banner, Minta, Profile
# Register your models here.

admin.site.register(Post)
admin.site.register(Banner)
admin.site.register(Profile)

# Custom Column
@admin.register(Daftar)
class DaftarAdmin(admin.ModelAdmin):  
    list_display = ('nama', 'email', 'telepon', 'gender', 'posisi', 'buat')
    ordering = ('-buat',)
    search_fields = ('nama',)

@admin.register(Pesan)
class PesanAdmin(admin.ModelAdmin):  
    list_display = ('nama', 'email', 'subjek', 'pesan')
    ordering = ('nama',)
    search_fields = ('nama', 'subjek',)

@admin.register(Minta)
class MintaAdmin(admin.ModelAdmin):  
    list_display = ('judul', 'perusahaan', 'estimasi', 'buat')
    ordering = ('-buat',)
    search_fields = ('nama',)