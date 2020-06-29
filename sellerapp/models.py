from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image
import time
import os
from uuid import uuid4
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

KEPUASAN_CHOICES = [
    ('Tingkat Kepuasan', 'Tingkat Kepuasan'),
    ('Puas', 'Puas'),
    ('Tidak Puas', 'Tidak Puas'),
]

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

def path_and_rename(path):
    def wrapper(instance, filename):
        ext = filename.split('.')[-1]
        if instance.pk:
            filename = '{}.{}'.format(instance.oleh, ext)
        else:
            filename = '{}.{}'.format(uuid4().hex, ext)
        return os.path.join(path, filename)


class Request(models.Model):
    nama_depan      = models.CharField(max_length=100)
    nama_belakang   = models.CharField(max_length=100)
    email           = models.EmailField()
    kontak          = models.CharField(max_length=14)
    deskripsi       = models.TextField()
    link            = models.URLField(null=True, blank=True)
    jenis_ruangan   = models.CharField(choices=JENIS_RUANGAN, max_length=50, default='Jenis Ruangan')
    files           = models.FileField(upload_to='upload/files/', default='default.jpg')
    image           = models.ImageField(upload_to=path_and_rename('upload/display/{}'.format(time.strftime("%Y/%m/%d"))), default='default.jpg')
    services        = models.CharField(choices=KATEGORI_CHOICES, max_length=50, default='Pilihan Service')
    jumlah_budget   = models.PositiveIntegerField(default=0)
    alamat          = models.CharField(max_length=500)
    kota            = models.CharField(max_length=50)
    provinsi        = models.CharField(choices=PROVINSI_CHOICES, max_length=50, default='Aceh')
    status          = models.CharField(choices=STATUS_CHOICES, max_length=30, default='Dalam Antrian')
    buat            = models.DateField(auto_now=True)
    tanggal_pengerjaan  = models.DateField(null=True, blank=True)
    tanggal_selesai     = models.DateField(null=True, blank=True)
    oleh            = models.ForeignKey(User, on_delete=models.CASCADE, related_name='karyawanUser', null=True, blank=True)
    revisi          = models.TextField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse('detail-permintaan', kwargs={'pk': self.id})

    def ids():
        no = Request.objects.count()
        if no == None:
            return 1
        else:
            return no + 1
    
    emp_id = models.IntegerField(('Code'), default=ids, unique=True, editable=False)
    
    id = models.CharField(primary_key=True, editable=False, max_length=30)
    def save(self, *args, **kwargs):
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)

        if not self.id:
            self.id = "{}{:08d}".format('YNK', self.emp_id)
        super(Request, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Data - Permintaan'

class Invoice(models.Model):
    oleh            = models.ForeignKey(Request, on_delete=models.CASCADE, related_name='invoice', null=True, blank=True)
    komentar        = models.TextField(null=True, blank=True)
    buat            = models.DateField(auto_now_add=True)
    kepuasan        = models.CharField(max_length=30, choices=KEPUASAN_CHOICES, default='Tingkat Kepuasan')

    def get_absolute_url(self):
        return reverse('profile', kwargs={'pk': self.id})

    def ids():
        no = Invoice.objects.count()
        if no == None:
            return 1
        else:
            return no + 1
    
    emp_id = models.IntegerField(('Code'), default=ids, unique=True, editable=False)

    id = models.CharField(primary_key=True, editable=False, max_length=30)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = "{}{:08d}/XX/VII/{}".format('INV', self.emp_id, self.oleh.id)
        super(Invoice, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Data - Invoice'

@receiver(post_save, sender=Request)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Invoice.objects.create(oleh=instance)
    instance.oleh.save()
