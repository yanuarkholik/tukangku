# Generated by Django 3.0 on 2020-05-13 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tukangkuapp', '0051_daftar_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='daftar',
            name='file',
            field=models.FileField(upload_to='upload/display/'),
        ),
    ]
