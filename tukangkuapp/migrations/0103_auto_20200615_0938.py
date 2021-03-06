# Generated by Django 2.2.10 on 2020-06-15 02:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tukangkuapp', '0102_auto_20200615_0934'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pesanauthor',
            old_name='judul',
            new_name='nama',
        ),
        migrations.RemoveField(
            model_name='pesanauthor',
            name='author',
        ),
        migrations.RemoveField(
            model_name='pesanauthor',
            name='file',
        ),
        migrations.AddField(
            model_name='pesanauthor',
            name='link',
            field=models.CharField(blank=True, help_text='Cantumkan link file keterangan bila perlu**', max_length=2000, null=True),
        ),
    ]
