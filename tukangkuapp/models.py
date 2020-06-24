from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image

from sellerapp.models import Gigs

# Choices 

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

# Form Section
class Minta(models.Model):
    judul       = models.CharField(max_length=100)
    kontak      = models.CharField(max_length=50, help_text='Nomor telepon atau email**')
    upah        = models.CharField(max_length=50)
    file        = models.FileField(null=True, blank=True, help_text='Upload file permintaan anda jika perlu**')
    deskripsi   = models.TextField(null=True, blank=True)
    buat        = models.DateTimeField(default=timezone.now)
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    slug        = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = self.slug or slugify(self.judul)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('minta')

    class Meta: 
        verbose_name_plural = 'Data-Request'

class Pesan(models.Model):
    nama        = models.CharField(max_length=100)
    email       = models.EmailField()
    subjek      = models.CharField(max_length=100, blank=True, null=True)
    pesan       = models.TextField

    class Meta:
        verbose_name_plural = 'Data-Pesan'

class Profile(models.Model):
    user        = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    image       = models.ImageField(default='default.jpg', upload_to='upload')
    deskripsi   = models.TextField(null=True, blank=True, help_text='Deskripsi singkat Profile anda**')
    deskripsi_singkat   = models.CharField(max_length=50, null=True, blank=True)
    nama_depan  = models.CharField(max_length=50, null=True, blank=True)
    nama_belakang = models.CharField(max_length=100, null=True, blank=True)
    profesi     = models.CharField(max_length=100, blank=True, null=True)
    pengalaman  = models.CharField(max_length=100, blank=True, null=True)
    sertifikasi = models.CharField(max_length=100, blank=True, null=True)
    web         = models.CharField(max_length=100, blank=True, null=True)
    pendidikan  = models.CharField(max_length=100, blank=True, null=True)
    gigs        = models.ForeignKey(Gigs, on_delete=models.CASCADE, related_name='profileGigs', null=True, blank=True)
    buat        = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.user.username}'
    
    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    class Meta:
        verbose_name_plural = 'Data-User'

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

class Review(models.Model):
    author      = models.ForeignKey(Profile, on_delete=models.CASCADE)
    nama        = models.CharField(max_length=250)
    review      = models.TextField(blank=True)
    gambar      = models.ImageField(upload_to='upload', blank=True, help_text='Masukkan gambar project anda jika perlu**')
    buat        = models.DateField(auto_now=True)
    
    def get_absolute_url(self):
        return reverse('review', kwargs={'pk': self.pk})

    class Meta: 
        verbose_name_plural = 'Data-Review'

class PesanAuthor(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reqUser', null=True, blank=True)
    author      = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reqtAuthor', blank=True, null=True)
    kontak      = models.CharField(max_length=50, help_text='Nomor telepon atau email**')
    link        = models.CharField(max_length=2000, help_text='Cantumkan link file keterangan bila perlu**', null=True, blank=True)
    upah        = models.CharField(max_length=50)
    deskripsi   = models.TextField(null=True, blank=True)
    buat        = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        return reverse('pesan-author', kwargs={'pk': self.pk})

    class Meta: 
        verbose_name_plural = 'Data-Request Pesan Author'



