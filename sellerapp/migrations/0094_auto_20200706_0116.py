# Generated by Django 2.2.10 on 2020-07-05 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sellerapp', '0093_auto_20200706_0104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='kepuasan',
            field=models.CharField(choices=[('Puas', 'Puas'), ('Tidak Puas', 'Tidak Puas')], default='', max_length=30),
        ),
    ]