# Generated by Django 3.0.7 on 2020-06-27 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tukangkuapp', '0114_auto_20200627_1426'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pesanauthor',
            options={'verbose_name_plural': 'Data-Pesanan'},
        ),
        migrations.AddField(
            model_name='pesanauthor',
            name='nama_belakang',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='pesanauthor',
            name='nama_depan',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
