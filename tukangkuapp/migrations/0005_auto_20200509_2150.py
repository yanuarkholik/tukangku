# Generated by Django 3.0 on 2020-05-09 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tukangkuapp', '0004_auto_20200509_2147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='minta',
            name='kotak',
            field=models.CharField(help_text='Nomor telepon atau email**', max_length=50),
        ),
    ]
