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


# Form Section

class Daftar(models.Model):
    email       = models.EmailField()
    telepon     = models.CharField(max_length=13)
    deskripsi   = models.TextField(null=True, blank=True)
    umur        = models.DateTimeField
    gender      = models.CharField(max_length=20, choices=GENDER_CHOICES)
    posisi      = models.CharField(max_length=20, choices=POSISI_CHOICES)
    author      = models.ForeignKey(User, on_delete=models.CASCADE)
    buat        = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Data-Daftar'

class Pesan(models.Model):
    nama        = models.CharField(max_length=100)
    email       = models.EmailField()
    subjek      = models.CharField(max_length=100, blank=True, null=True)
    pesan       = models.TextField

    class Meta:
        verbose_name_plural = 'Data-Pesan'

class Minta(models.Model):
    judul       = models.CharField(max_length=100)
    kontak      = models.CharField(max_length=50, help_text='Nomor telepon atau email**')
    upah        = models.CharField(max_length=50, default='Rp ')
    deskripsi   = models.TextField(null=True, blank=True)
    buat        = models.DateTimeField(default=timezone.now)
    author      = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('minta-detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name_plural = 'Data-Request'

class Profile(models.Model):
    user    = models.OneToOneField(User, on_delete=models.CASCADE)
    image   = models.ImageField(default='default.jpg', upload_to='upload')
    display = models.ImageField(default='default.jpg', upload_to='upload/display')
    buat    = models.DateTimeField(auto_now=True)
    
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