# Generated by Django 2.2.10 on 2020-07-05 12:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sellerapp', '0084_auto_20200705_1857'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='request',
            name='image',
        ),
        migrations.RemoveField(
            model_name='request',
            name='image_1',
        ),
        migrations.RemoveField(
            model_name='request',
            name='image_2',
        ),
        migrations.RemoveField(
            model_name='request',
            name='image_3',
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=None)),
                ('image_1', models.ImageField(upload_to=None)),
                ('image_2', models.ImageField(upload_to=None)),
                ('image_3', models.ImageField(upload_to=None)),
                ('oleh', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='sellerapp.Request')),
            ],
        ),
    ]
