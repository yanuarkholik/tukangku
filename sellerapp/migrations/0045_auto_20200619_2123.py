# Generated by Django 2.2.10 on 2020-06-19 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sellerapp', '0044_auto_20200619_2025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gigs',
            name='deskripsi_singkat',
            field=models.CharField(blank=True, help_text='Deskripsi singkat Gigs anda**', max_length=50, null=True),
        ),
    ]
