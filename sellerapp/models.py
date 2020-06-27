from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image
# Create your models here.


KATEGORI_CHOICES = [
    ('Kategori', 'Kategori'),
    ('Arsitek', 'Arsitek'),
    ('Design Interior', 'Design Interior'),
    ('Kontraktor', 'Kontraktor'),
    ('Design and Build', 'Design and Build'),
]

JENIS_RUANGAN = [
    ('Jenis Ruangan', 'Jenis Ruangan'),
    ('Kamar Tidur','Kamar Tidur'),
    ('Kamar Mandi', 'Kamar Mandi'),
    ('Dapur', 'Dapur'),
    ('Ruang Keluarga', 'Ruang Keluarga'),
    ('Taman', 'Taman'),
    ('Tangga', 'Tangga'),
    ('Ruang Makan', 'Ruang Makan'),
    ('Exterior', 'Exterior'),
    ('Ruang Belajar', 'Ruang Belajar'),
    ('Ruang Kerja', 'Ruang Kerja'),
    ('Perpustakaan', 'Perpustakaan'),
]

PAKET_CHOICES = [
    ('Basic', 'Basic'),
    ('Standard', 'Standard'),
    ('Premium', 'Premium'),
]

PROVINSI_CHOICES = [
    ('Aceh', 'Aceh'), ('Aceh', 'Aceh'), ('Aceh', 'Aceh'), ('Aceh', 'Aceh'), ('Aceh', 'Aceh'),
    ('Aceh', 'Aceh'), ('Aceh', 'Aceh'), ('Aceh', 'Aceh'), ('Aceh', 'Aceh'), ('Aceh', 'Aceh'),
    ('Aceh', 'Aceh'), ('Aceh', 'Aceh'), ('Aceh', 'Aceh'), ('Aceh', 'Aceh'), ('Aceh', 'Aceh'),
    ('Aceh', 'Aceh'), ('Aceh', 'Aceh'), ('Aceh', 'Aceh'), ('Aceh', 'Aceh'), ('Aceh', 'Aceh'),
    ('Aceh', 'Aceh'), ('Aceh', 'Aceh'), ('Aceh', 'Aceh'), ('Aceh', 'Aceh'), ('Aceh', 'Aceh'),
    ('Aceh', 'Aceh'), ('Aceh', 'Aceh'), ('Aceh', 'Aceh'), ('Aceh', 'Aceh'), ('Aceh', 'Aceh'),
    ('Aceh', 'Aceh'), ('Aceh', 'Aceh'), ('Aceh', 'Aceh'), ('Aceh', 'Aceh'),
] 


STATUS_CHOICES = [
    ('Dalam antrian', 'Dalam Antrian'),
    ('Dalam Pengerjaan', 'Dalam Pengerjaan'),
    ('Selesai', 'Selesai')
]

class ProInfo(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sellerProfile', null=True, blank=True)
    status      = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Client')
    nama_depan  = models.CharField(max_length=50, null=True, blank=True)
    nama_belakang = models.CharField(max_length=100, null=True, blank=True)
    profesi     = models.CharField(max_length=100)
    keahlian    = models.CharField(max_length=100)
    pengalaman  = models.CharField(max_length=100)
    deskripsi_singkat   = models.TextField(null=True, blank=True, help_text='Deskripsi singkat Profile anda**')
    deskripsi  = models.CharField(max_length=50)
    pendidikan  = models.CharField(max_length=100)
    sertifikasi = models.CharField(max_length=100, blank=True, null=True)
    web         = models.CharField(max_length=100, blank=True, null=True)
    email       = models.EmailField()
    buat        = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Data-Seller'

class Images(models.Model):
    user        = models.ForeignKey(User, default=None, on_delete=models.CASCADE, related_name='imgGigs', null=True, blank=True)
    images      = models.ImageField(upload_to = 'upload/display/',null=True, blank=True)
    buat        = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Data-Seller Gigs Display'

class Gigs(models.Model):
    judul               = models.CharField(max_length=254, null=True, blank=True)
    user                = models.ForeignKey(User, on_delete=models.PROTECT, related_name='usernameGigs', null=True, blank=True)
    deskripsi_project   = models.TextField(blank=True, null=True)
    kategori            = models.CharField(choices=KATEGORI_CHOICES, max_length=50, default='Kategori')
    jenis_ruangan       = models.CharField(choices=JENIS_RUANGAN, max_length=50, default='Jenis Ruangan')
    thumbnail           = models.FileField(blank=True)
    img                 = models.ForeignKey(Images, on_delete=models.CASCADE, related_name='relatedImageGigs', null=True, blank=True)
    slug                = models.SlugField(unique=True, blank=True, null=True)
    estimasi_kecil      = models.PositiveIntegerField(default=0)
    estimasi_besar      = models.PositiveIntegerField(default=0)
    waktu_pengerjaan    = models.PositiveIntegerField(default=0)
    banyak_revisi       = models.PositiveIntegerField(default=0)
    kota                = models.CharField(max_length=100, blank=True, null=True)
    provinsi            = models.CharField(max_length=100, choices=PROVINSI_CHOICES, default='Aceh')
    alamat              = models.CharField(max_length=100, blank=True, null=True)
    buat                = models.DateTimeField(auto_now=True)

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

class AlbumTukang(models.Model):
    """ Album rekam project Tukangku """
    user        = models.ForeignKey(User, on_delete=models.CASCADE, related_name='albumProject', blank=True, null=True)
    judul       = models.CharField(max_length=250)
    deskripsi   = models.TextField(null=True, blank=True)
    images      = models.ImageField(upload_to='upload')
    kota        = models.CharField(max_length=250)
    provinsi    = models.CharField(choices=PROVINSI_CHOICES, default='Aceh', max_length=50)

    class Meta: 
        verbose_name_plural = 'Data-Album Project'

