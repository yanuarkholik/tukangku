# Generated by Django 3.0 on 2020-06-06 14:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sellerapp', '0011_proinfo_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gigs',
            old_name='author',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='proinfo',
            old_name='author',
            new_name='user',
        ),
    ]
