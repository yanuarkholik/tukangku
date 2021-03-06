# Generated by Django 3.0 on 2020-06-06 09:02

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('sellerapp', '0004_auto_20200606_1558'),
    ]

    operations = [
        migrations.CreateModel(
            name='Daftar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('judul', models.CharField(blank=True, max_length=254, null=True)),
                ('deskripsi', models.CharField(help_text='Deskripsi singkat Gigs anda**', max_length=50)),
                ('kategori', models.CharField(choices=[('Kategori', 'Kategori'), ('Pemrograman & TI', 'Pemrograman & TI'), ('Desain Grafis', 'Desain Grafis'), ('Marketing', 'Marketing'), ('Menulis', 'Menulis'), ('Video & Animasi', 'Video & Animasi'), ('Musik & Audio', 'Musik & Audio'), ('Bisnis', 'Bisnis')], default='Kategori', max_length=50)),
                ('buat', models.DateTimeField(default=django.utils.timezone.now)),
                ('file', models.FileField(blank=True, upload_to='')),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
                ('basic', models.PositiveIntegerField(default=0)),
                ('standard', models.PositiveIntegerField(default=0)),
                ('premium', models.PositiveIntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author', to='sellerapp.ProInfo')),
            ],
            options={
                'verbose_name_plural': 'Data-Daftar',
            },
        ),
    ]
