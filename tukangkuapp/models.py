from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image

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

TEAM_CHOICES = [
    ('Perorangan', 'Perorangan'),
    ('Team', 'Team')
]

# Form Section

class Daftar(models.Model):
    deskripsi   = models.TextField(null=True, blank=True, help_text='Deskripsikan keahlian anda disini**')
    anggota     = models.CharField(choices=TEAM_CHOICES, default='Perorangan', max_length=30, help_text='Pilihan anggota atau perorangan**')
    posisi      = models.CharField(max_length=20, choices=POSISI_CHOICES)
    author      = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    buat        = models.DateTimeField(auto_now=True)
    file        = models.FileField(blank=True)

    def get_absolute_url(self):
        return reverse('daftar-detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name_plural = 'Data-Daftar'

class PostDaftarImage(models.Model):
    post        = models.ForeignKey(Daftar, default=None, on_delete=models.CASCADE)
    images      = models.FileField(upload_to = 'upload/display/')


class Pesan(models.Model):
    nama        = models.CharField(max_length=100)
    email       = models.EmailField()
    subjek      = models.CharField(max_length=100, blank=True, null=True)
    pesan       = models.TextField

    class Meta:
        verbose_name_plural = 'Data-Pesan'

class Review(models.Model):
    author      = models.ForeignKey(User, on_delete=models.CASCADE)
    review      = models.TextField()
    buat        = models.DateField(default=timezone.now)
    
    def get_absolute_url(self):
        return reverse('review', kwargs={'pk': self.pk})

    class Meta: 
        verbose_name_plural = 'Data-Review'

class Minta(models.Model):
    judul       = models.CharField(max_length=100)
    kontak      = models.CharField(max_length=50, help_text='Nomor telepon atau email**')
    upah        = models.CharField(max_length=50)
    file        = models.FileField(null=True, blank=True, help_text='Upload file permintaan anda jika perlu**')
    deskripsi   = models.TextField(null=True, blank=True)
    buat        = models.DateTimeField(default=timezone.now)
    author      = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('minta')

    class Meta: 
        verbose_name_plural = 'Data-Request'

class Profile(models.Model):
    user        = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    image       = models.ImageField(default='default.jpg', upload_to='upload')
    deskripsi   = models.TextField(null=True, blank=True)
    buat        = models.DateTimeField(auto_now=True)
    daftar      = models.ForeignKey(Daftar, on_delete=models.CASCADE)
    
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
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

class PesanAuthor(models.Model):
    judul       = models.CharField(max_length=100)
    kontak      = models.CharField(max_length=50, help_text='Nomor telepon atau email**')
    upah        = models.CharField(max_length=50)
    file        = models.FileField(null=True, blank=True, help_text='Upload file permintaan anda jika perlu**')
    deskripsi   = models.TextField(null=True, blank=True)
    buat        = models.DateTimeField(default=timezone.now)
    author      = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('pesan-author', kwargs={'pk': self.pk})

    class Meta: 
        verbose_name_plural = 'Data-Request Pesan Author'
