# Generated by Django 2.2.10 on 2020-06-29 17:02

from django.db import migrations, models
import sellerapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('sellerapp', '0066_auto_20200629_2358'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='emp_id',
            field=models.IntegerField(default=sellerapp.models.Request.ids, editable=False, verbose_name='Code'),
        ),
    ]