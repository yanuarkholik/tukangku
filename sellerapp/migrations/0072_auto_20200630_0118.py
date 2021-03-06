# Generated by Django 2.2.10 on 2020-06-29 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sellerapp', '0071_auto_20200630_0106'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='alamat',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='deskripsi',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='email',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='files',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='image',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='jenis_ruangan',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='jumlah_budget',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='kontak',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='kota',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='link',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='nama_belakang',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='nama_depan',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='provinsi',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='services',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='status',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='tanggal_pengerjaan',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='tanggal_selesai',
        ),
        migrations.AlterField(
            model_name='invoice',
            name='buat',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='komentar',
            field=models.TextField(blank=True, null=True),
        ),
    ]
