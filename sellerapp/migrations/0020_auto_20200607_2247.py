# Generated by Django 3.0.7 on 2020-06-07 15:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sellerapp', '0019_requestdirectauthor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gigs',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='authorGigs', to=settings.AUTH_USER_MODEL),
        ),
    ]
