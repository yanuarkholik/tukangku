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
    ('Lainnya', 'Lainnya')
]

PROVINSI_CHOICES = [
    ('Aceh', 'Aceh'), ('Sumatra Utara', 'Sumatra Utara'), ('Sumatra Barat', 'Sumatra Barat'), ('Riau', 'Riau'), ('Kepulauan Riau', 'Kepulauan Riau'),
    ('Jambi	', 'Jambi'), ('Bengkulu', 'Bengkulu'), ('Sumatra Selatan', ' Sumatra Selatan'), (' Kepulauan Bangka Belitung', ' Kepulauan Bangka Belitung'), ('Lampung', 'Lampung'),
    ('Banten', 'Banten'), ('Jawa Barat', 'Jawa Barat'), ('Jakarta', 'Jakarta'), ('Jawa Tengah', 'Jawa Tengah'), ('Yogyakarta', 'Yogyakarta'),
    ('Jawa Timur', 'Jawa Timur'), ('Bali', 'Bali'), ('Nusa Tenggara Barat', 'Nusa Tenggara Barat'), ('Nusa Tenggara Timur', 'Nusa Tenggara Timur'), ('Kalimantan Barat', 'Kalimantan Barat'),
    ('Kalimantan Selatan', 'Kalimantan Selatan'), ('Kalimantan Tengah', 'Kalimantan Tengah'), ('Kalimantan Timur', 'Kalimantan Timur'), ('Kalimantan Utara', 'Kalimantan Utara'), ('Gorontalo', 'Gorontalo'),
    ('Sulawesi Barat', 'Sulawesi Barat'), ('Sulawesi Selatan', 'Sulawesi Selatan'), ('Sulawesi Tengah', 'Sulawesi Tengah'), ('Sulawesi Tenggara', 'Sulawesi Tenggara'), ('Sulawesi Utara', 'Sulawesi Utara'),
    ('Maluku', 'Maluku'), ('Maluku Utara', 'Maluku Utara'), ('Papua Barat', 'Papua Barat'), ('Papua', 'Papua'),
] 


STATUS_CHOICES = [
    ('Dalam Antrian', 'Dalam Antrian'),
    ('Dalam Pengerjaan', 'Dalam Pengerjaan'),
    ('Menunggu Pembayaran', 'Menunggu Pembayaran'),
    ('Selesai', 'Selesai')
]

KEPUASAN_CHOICES = [
    ('Puas', 'Puas'),
    ('Tidak Puas', 'Tidak Puas'),
]

SETUJU_CHOICES = [
    ('Beri Persetujuan', 'Beri Persetujuan'),
    ('Setuju', 'Setuju'),
    ('Tidak Setuju', 'Tidak Setuju'),
]

class Request(models.Model):
    oleh            = models.ForeignKey(User, on_delete=models.CASCADE, related_name='karyawanUser', null=True, blank=True)
    nama_depan      = models.CharField(max_length=100)
    nama_belakang   = models.CharField(max_length=100)
    email           = models.EmailField()
    kontak          = models.CharField(max_length=14)
    link            = models.URLField(null=True, blank=True)
    jenis_ruangan   = models.CharField(choices=JENIS_RUANGAN, max_length=50, default='Jenis Ruangan')
    lainnya         = models.CharField(max_length=1000, null=True, blank=True)
    services        = models.CharField(choices=KATEGORI_CHOICES, max_length=50, default='Pilihan Service')
    jumlah_budget   = models.PositiveIntegerField(default=0)
    alamat          = models.CharField(max_length=500)
    kota            = models.CharField(max_length=50)
    provinsi        = models.CharField(max_length=50, choices=PROVINSI_CHOICES, default='Aceh')
    deskripsi       = models.TextField()
    status          = models.CharField(choices=STATUS_CHOICES, max_length=30, default='Dalam Antrian')
    buat            = models.DateField(auto_now=True)
    tanggal_pengerjaan  = models.DateField(null=True, blank=True)
    tanggal_selesai     = models.DateField(null=True, blank=True)
    files           = models.FileField(upload_to='upload/files/', default='default.jpg')
    bukti           = models.ImageField(upload_to='upload/bukti/', null=True, blank=True)
    feedback        = models.TextField(null=True, blank=True)
    setujui         = models.CharField(max_length=50, choices=SETUJU_CHOICES, default='Beri Persetujuan',null=True, blank=True)
    revisi          = models.TextField(null=True, blank=True)
    kepuasan        = models.CharField(max_length=30, choices=KEPUASAN_CHOICES, default='Puas', null=True, blank=True)

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
        if not self.id:
            self.id = "{}{:08d}".format('TKG', self.emp_id)
        super(Request, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Data - Permintaan'

class Images(models.Model):
    oleh            = models.ForeignKey(Request, on_delete=models.CASCADE, related_name='images', null=True, blank=True)
    image           = models.ImageField(upload_to='upload/display/{}'.format(time.strftime("%Y/%m/%d")))
    image_1         = models.ImageField(upload_to='upload/display/{}'.format(time.strftime("%Y/%m/%d")))
    image_2         = models.ImageField(upload_to='upload/display/{}'.format(time.strftime("%Y/%m/%d")))
    image_3         = models.ImageField(upload_to='upload/display/{}'.format(time.strftime("%Y/%m/%d")))

    def save(self, *args, **kwargs):
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)
        super(Images, self).save(*args, **kwargs)

class Invoice(models.Model):
    oleh            = models.OneToOneField(Request, on_delete=models.CASCADE, related_name='invoice', null=True, blank=True)
    buat            = models.DateField(auto_now_add=True)
    kepuasan        = models.CharField(max_length=30, choices=KEPUASAN_CHOICES, default='')

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
