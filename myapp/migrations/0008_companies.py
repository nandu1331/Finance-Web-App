# Generated by Django 5.0.6 on 2024-07-22 12:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_uploadedfile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Companies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=256)),
                ('symbol', models.CharField(blank=True, max_length=256)),
                ('industry', models.CharField(blank=True, max_length=256)),
                ('isinCode', models.CharField(blank=True, max_length=256)),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.userprofile')),
            ],
        ),
    ]
