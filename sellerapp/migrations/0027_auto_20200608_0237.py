# Generated by Django 3.0.7 on 2020-06-07 19:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sellerapp', '0026_auto_20200608_0229'),
    ]

    operations = [
        migrations.RenameField(
            model_name='requestdirectauthor',
            old_name='author',
            new_name='user',
        ),
    ]
