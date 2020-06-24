from django.contrib import admin

from sellerapp.models import ProInfo, Gigs, Images
# Register your models here.

@admin.register(ProInfo)
class SellerAdmin(admin.ModelAdmin):  
    list_display = ('user','email', 'keahlian', 'id')
    ordering = ('-buat',)
    search_fields = ()

@admin.register(Images)
class ImagesAdmin(admin.ModelAdmin):
    list_display = ('user', 'buat')
    ordering = ('-buat',)
    search_fields = ()

@admin.register(Gigs)
class GigsAdmin(admin.ModelAdmin): 
    list_display = ('user','judul', 'kategori', 'id')
    prepopulated_fields = {'slug': ('judul',)}
    ordering = ('-buat',)
    search_fields = ()

    class Meta:
           model = Gigs


