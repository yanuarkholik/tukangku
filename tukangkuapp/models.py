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

class PesanAuthor(models.Model):
    nama_depan  = models.CharField(max_length=100, null=True, blank=True)
    nama_belakang  = models.CharField(max_length=100, null=True, blank=True)
    kontak      = models.CharField(max_length=50, help_text='Nomor telepon atau email**')
    link        = models.CharField(max_length=2000, help_text='Cantumkan link file keterangan bila perlu**', null=True, blank=True)
    deskripsi   = models.TextField(null=True, blank=True)
    buat        = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        return reverse('pesan-author', kwargs={'pk': self.pk, 'username':self.user})

    class Meta: 
        verbose_name_plural = 'Data-Pesanan'




