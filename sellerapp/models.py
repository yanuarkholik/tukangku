from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image
# Create your models here.

from tukangkuapp.models import Profile


KATEGORI_CHOICES = [
    ('Kategori', 'Kategori'),
    ('Pemrograman & TI', 'Pemrograman & TI'),
    ('Desain Grafis', 'Desain Grafis'),
    ('Marketing', 'Marketing'),
    ('Menulis', 'Menulis'),
    ('Video & Animasi','Video & Animasi'),
    ('Musik & Audio', 'Musik & Audio'),
    ('Bisnis', 'Bisnis'),
]

STATUS_CHOICES = [
    ('Seller', 'Seller'),
    ('Client', 'Client')
]

PAKET_CHOICES = [
    ('Basic', 'Basic'),
    ('Standard', 'Standard'),
    ('Premium', 'Premium'),
]

class ProInfo(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sellerProfile', null=True, blank=True)
    status      = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Client')
    nama_depan  = models.CharField(max_length=50, null=True, blank=True)
    nama_belakang = models.CharField(max_length=100, null=True, blank=True)
    profesi     = models.CharField(max_length=100)
    keahlian    = models.CharField(max_length=100)
    pengalaman  = models.CharField(max_length=100)
    deskripsi   = models.TextField(null=True, blank=True)
    pendidikan  = models.CharField(max_length=100)
    sertifikasi = models.CharField(max_length=100, blank=True, null=True)
    web         = models.CharField(max_length=100, blank=True, null=True)
    email       = models.EmailField()
    buat        = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Data-Seller'

class Gigs(models.Model):
    judul       = models.CharField(max_length=254, null=True, blank=True)
    deskripsi_singkat   = models.CharField(max_length=50 , help_text='Deskripsi singkat Gigs anda**')
    kategori    = models.CharField(choices=KATEGORI_CHOICES, max_length=50, default='Kategori')
    user        = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authorGigs', null=True, blank=True)
    buat        = models.DateTimeField(default=timezone.now)
    thumbnail   = models.FileField(blank=True)
    slug        = models.SlugField(unique=True, blank=True, null=True)
    basic       = models.PositiveIntegerField(default=0)
    standard    = models.PositiveIntegerField(default=0)
    premium     = models.PositiveIntegerField(default=0)


    def get_absolute_url(self):
        return reverse('daftar-detail', kwargs={'pk': self.id, 'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = self.slug or slugify(self.judul)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Data-Gigs'


class SellerGigsImage(models.Model):
    user        = models.ForeignKey(Gigs, default=None, on_delete=models.CASCADE)
    images      = models.FileField(upload_to = 'upload/display/')

class RequestDirectAuthor(models.Model):
    """ Data dari client yang request secara langsung ke author """
    user        = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requestAuthor', blank=True, null=True)
    judul       = models.ForeignKey(Gigs, on_delete=models.CASCADE, related_name='orderFrom', blank=True, null=True)
    deskripsi_singkat   = models.CharField(max_length=500, help_text='Isi deskripsi singkat agar Seller paham dengan permintaan anda**', null=True, blank=True)
    paket       = models.CharField(choices=PAKET_CHOICES, max_length=30, default='Basic')
    kirim_ke    = models.CharField(max_length=254, null=True, blank=True)
    buat        = models.DateTimeField(default=timezone.now)
    document    = models.FileField(null=True, blank=True, help_text='Upload file permintaan anda jika perlu**')

    def get_absolute_url(self):
        return reverse('req-cek', kwargs={'pk': self.pk})

    class Meta: 
        verbose_name_plural = 'Data-Request Author'
