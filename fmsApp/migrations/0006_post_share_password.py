# Generated by Django 4.2 on 2024-07-24 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fmsApp', '0005_document'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='share_password',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
