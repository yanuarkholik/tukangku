from django.contrib import admin

from sellerapp.models import ProInfo, Gigs, SellerGigsImage
# Register your models here.

@admin.register(ProInfo)
class SellerAdmin(admin.ModelAdmin):  
    list_display = ('user','email', 'keahlian', 'id')
    ordering = ('-buat',)
    search_fields = ()

class SellerGigsAdminInline(admin.TabularInline):
    model = SellerGigsImage

@admin.register(Gigs)
class GigsAdmin(admin.ModelAdmin): 
    inlines = [SellerGigsAdminInline,] 
    list_display = ('user','judul', 'kategori', 'id')
    prepopulated_fields = {'slug': ('judul',)}
    ordering = ('-buat',)
    search_fields = ()

    class Meta:
           model = Gigs


