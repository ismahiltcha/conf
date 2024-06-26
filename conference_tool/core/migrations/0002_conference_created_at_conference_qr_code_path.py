# Generated by Django 5.0.6 on 2024-06-09 22:05

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='conference',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='conference',
            name='qr_code_path',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
