# Generated by Django 3.0 on 2020-05-10 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tukangkuapp', '0010_auto_20200510_2021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='minta',
            name='upah',
            field=models.CharField(choices=[('< Rp. 500.000', '< Rp. 500.000'), (' Rp. 500.000 - Rp. 1.000.000', ' Rp. 500.000 - Rp. 1.000.000'), (' Rp. 1.000.000 - Rp. 2.000.000', ' Rp. 1.000.000 - Rp. 2.000.000'), (' Rp. 2.000.000 - Rp. 3.000.000', ' Rp. 2.000.000 - Rp. 3.000.000'), (' Rp. 3.000.000', ' Rp. 3.000.000')], default='< Rp. 500.000', max_length=50),
        ),
    ]
