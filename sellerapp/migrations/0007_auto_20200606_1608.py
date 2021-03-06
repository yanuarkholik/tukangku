# Generated by Django 3.0 on 2020-06-06 09:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sellerapp', '0006_auto_20200606_1602'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='gigs',
            options={'verbose_name_plural': 'Data-Gigs'},
        ),
        migrations.CreateModel(
            name='SellerGigsImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('images', models.FileField(upload_to='upload/display/')),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='sellerapp.Gigs')),
            ],
        ),
    ]
