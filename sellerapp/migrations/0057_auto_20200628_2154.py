# Generated by Django 2.2.10 on 2020-06-28 14:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sellerapp', '0056_request'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proinfo',
            name='user',
        ),
        migrations.DeleteModel(
            name='AlbumTukang',
        ),
        migrations.DeleteModel(
            name='ProInfo',
        ),
    ]