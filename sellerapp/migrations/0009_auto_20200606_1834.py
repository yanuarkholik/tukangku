# Generated by Django 3.0 on 2020-06-06 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sellerapp', '0008_auto_20200606_1736'),
    ]

    operations = [
        migrations.AddField(
            model_name='proinfo',
            name='nama_belakang',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='proinfo',
            name='nama_depan',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
