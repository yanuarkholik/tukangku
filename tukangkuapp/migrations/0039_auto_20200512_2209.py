# Generated by Django 3.0 on 2020-05-12 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tukangkuapp', '0038_auto_20200512_2201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='review',
            field=models.TextField(),
        ),
    ]
