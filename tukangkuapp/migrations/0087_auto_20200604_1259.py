# Generated by Django 3.0 on 2020-06-04 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tukangkuapp', '0086_auto_20200604_1259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='daftar',
            name='basic',
            field=models.DecimalField(decimal_places=10, max_digits=19),
        ),
        migrations.AlterField(
            model_name='daftar',
            name='premium',
            field=models.DecimalField(decimal_places=10, max_digits=19),
        ),
        migrations.AlterField(
            model_name='daftar',
            name='standard',
            field=models.DecimalField(decimal_places=10, max_digits=19),
        ),
        migrations.AlterField(
            model_name='minta',
            name='upah',
            field=models.DecimalField(decimal_places=10, max_digits=19),
        ),
    ]
