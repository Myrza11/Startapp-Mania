# Generated by Django 5.0.1 on 2024-02-25 15:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('regauth', '0008_merge_20240224_1520'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customusers',
            name='ability',
        ),
        migrations.RemoveField(
            model_name='customusers',
            name='link',
        ),
        migrations.RemoveField(
            model_name='customusers',
            name='link_name',
        ),
    ]
