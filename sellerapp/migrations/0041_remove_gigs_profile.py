# Generated by Django 2.2.10 on 2020-06-18 14:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sellerapp', '0040_auto_20200618_2039'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gigs',
            name='profile',
        ),
    ]
