# Generated by Django 3.0.7 on 2020-06-07 15:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tukangkuapp', '0100_delete_requestdirectauthor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='postdaftarimage',
            name='user',
        ),
        migrations.DeleteModel(
            name='Daftar',
        ),
        migrations.DeleteModel(
            name='PostDaftarImage',
        ),
    ]
