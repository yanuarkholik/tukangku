# Generated by Django 2.2.10 on 2020-06-28 14:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tukangkuapp', '0116_remove_pesanauthor_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='minta',
            name='user',
        ),
        migrations.DeleteModel(
            name='Pesan',
        ),
        migrations.RemoveField(
            model_name='review',
            name='author',
        ),
        migrations.DeleteModel(
            name='Minta',
        ),
        migrations.DeleteModel(
            name='Review',
        ),
    ]
