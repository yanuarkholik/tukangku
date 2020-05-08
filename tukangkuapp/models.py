from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Choices 
GENDER_CHOICES = [
    ('Pria', 'Pria'),
    ('Wanita', 'Wanita'),
]

POSISI_CHOICES = [
    ('Mandor', 'Mandor'),
    ('Kontraktor', 'Kontraktor'),
    ('Tukang', 'Tukang'),
]

# Create your models here.
class Post(models.Model):
    judul       = models.CharField(max_length=200)
    sub_judul   = models.CharField(max_length=200)
    konten      = models.TextField()
    pub_date    = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.judul 

    class Meta:
        verbose_name_plural = 'Buat-Post'

class Banner(models.Model):
    judul       = models.CharField(max_length=50)
    isi         = models.TextField()
    image       = models.ImageField(default='default.jpg', upload_to='upload')

    def __str__(self):
        return self.judul

    class Meta:
        verbose_name_plural = 'Buat-Banner'

# Form Section

class Daftar(models.Model):
    nama        = models.CharField(max_length=200, )
    email       = models.EmailField()
    telepon     = models.CharField(max_length=13)
    deskripsi   = models.TextField(default="Tidak ada deskripsi", null=True, blank=True)
    umur        = models.DateTimeField
    gender      = models.CharField(max_length=20, choices=GENDER_CHOICES)
    posisi      = models.CharField(max_length=20, choices=POSISI_CHOICES)
    buat        = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Data-Daftar'

class Pesan(models.Model):
    nama        = models.CharField(max_length=100)
    email       = models.EmailField()
    subjek      = models.CharField(max_length=100, blank=True, null=True)
    pesan       = models.TextField()

    class Meta:
        verbose_name_plural = 'Data-Pesan'

class Minta(models.Model):
    judul       = models.CharField(max_length=100)
    perusahaan  = models.CharField(max_length=50)
    estimasi    = models.CharField(max_length=10)
    deskripsi   = models.TextField(default="Tidak ada deskripsi", null=True, blank=True)
    buat        = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Data-Minta'
        
class Profile(models.Model):
    user    = models.OneToOneField(User, on_delete=models.CASCADE)
    image   = models.ImageField(default='default.jpg', upload_to='upload')
    

    def __str__(self):
        return f'{self.user.username}'

    class Meta:
        verbose_name_plural = 'Data-User'

