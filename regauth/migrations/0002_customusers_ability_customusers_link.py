# Generated by Django 5.0.1 on 2024-01-29 03:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('regauth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customusers',
            name='ability',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='customusers',
            name='link',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
