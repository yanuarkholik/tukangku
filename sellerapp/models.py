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

def path_and_rename(path):
    def wrapper(instance, filename):
        ext = filename.split('.')[-1]
        if instance.pk:
            filename = '{}.{}'.format(instance.oleh, ext)
        else:
            filename = '{}.{}'.format(uuid4().hex, ext)
        return os.path.join(path, filename)
    # return wrapper


class Request(models.Model):
    oleh            = models.ForeignKey(User, on_delete=models.CASCADE, related_name='karyawanUser', null=True, blank=True)
    nama_depan      = models.CharField(max_length=100)
    nama_belakang   = models.CharField(max_length=100)
    email           = models.EmailField()
    kontak          = models.CharField(max_length=14)
    link            = models.URLField(null=True, blank=True)
    jenis_ruangan   = models.CharField(choices=JENIS_RUANGAN, max_length=50, default='Jenis Ruangan')
    services        = models.CharField(choices=KATEGORI_CHOICES, max_length=50, default='Pilihan Service')
    jumlah_budget   = models.PositiveIntegerField(default=0)
    alamat          = models.CharField(max_length=500)
    kota            = models.CharField(max_length=50)
    provinsi        = models.CharField(choices=PROVINSI_CHOICES, max_length=50, default='Aceh')
    deskripsi       = models.TextField()
    status          = models.CharField(choices=STATUS_CHOICES, max_length=30, default='Dalam Antrian')
    buat            = models.DateField(auto_now=True)
    tanggal_pengerjaan  = models.DateField(null=True, blank=True)
    tanggal_selesai     = models.DateField(null=True, blank=True)
    files           = models.FileField(upload_to='upload/files/', default='default.jpg')
    image           = models.ImageField(upload_to=path_and_rename('upload/display/{}'.format(time.strftime("%Y/%m/%d"))), default='default.jpg')
    feedback        = models.TextField(null=True, blank=True)

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
            self.id = "{}{:08d}".format('TKG', self.emp_id)
        super(Request, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Data - Permintaan'

class Invoice(models.Model):
    oleh            = models.ForeignKey(Request, on_delete=models.CASCADE, related_name='invoice', null=True, blank=True)
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
