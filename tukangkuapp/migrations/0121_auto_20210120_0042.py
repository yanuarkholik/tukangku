# Generated by Django 3.1.5 on 2021-01-19 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tukangkuapp', '0120_delete_pesanauthor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.FileField(default='default.jpg', upload_to='upload'),
        ),
    ]
