from django.contrib import admin

from sellerapp.models import ProInfo, Gigs, Images, SellerGigsImage
# Register your models here.

class ImagesAdmin(admin.TabularInline):
    model = SellerGigsImage

@admin.register(Gigs)
class GigsAdmin(admin.ModelAdmin): 
    list_display = ('user','judul','jenis_ruangan', 'kategori', 'id')
    prepopulated_fields = {'slug': ('judul',)}
    ordering = ('-buat',)
    search_fields = ()
    inlines = [ImagesAdmin,]

    class Meta:
           model = Gigs

@admin.register(Images)
class ImagesAdmin(admin.ModelAdmin):
    list_display = ('user','images','buat')
    ordering = ('-buat',)