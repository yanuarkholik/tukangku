# Generated by Django 3.0 on 2020-06-04 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tukangkuapp', '0093_auto_20200604_1601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestdirectauthor',
            name='deskripsi',
            field=models.TextField(),
        ),
    ]
