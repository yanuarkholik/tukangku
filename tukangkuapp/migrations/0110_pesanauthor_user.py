# Generated by Django 2.2.10 on 2020-06-22 07:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tukangkuapp', '0109_auto_20200618_2215'),
    ]

    operations = [
        migrations.AddField(
            model_name='pesanauthor',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='authorPesan', to=settings.AUTH_USER_MODEL),
        ),
    ]
