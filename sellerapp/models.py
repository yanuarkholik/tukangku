from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image
# Create your models here.
class Seller(models.Model):
    author      = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seller')
    image       = models.ImageField(default='default.jpg', upload_to='upload')
    deskripsi   = models.TextField(null=True, blank=True)
    buat        = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.author.username}'
    
    def save(self, *args, **kwargs):
        super(Seller, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    class Meta:
        verbose_name_plural = 'Data-Seller'

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Seller.objects.create(user=instance)
    instance.profile.save()

class ProInfo(models.Model):
    user        = models.ForeignKey(Seller, on_delete=models.CASCADE)
    profesi     = models.CharField(max_length=100)
    keahlian    = models.CharField(max_length=100)
    pengalaman  = models.CharField(max_length=100)
    pendidikan  = models.CharField(max_length=100)
    sertifikasi = models.CharField(max_length=100, blank=True, null=True)
    web         = models.CharField(max_length=100, blank=True, null=True)
    email       = models.EmailField()