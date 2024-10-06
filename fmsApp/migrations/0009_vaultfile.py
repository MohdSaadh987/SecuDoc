# Generated by Django 5.0.7 on 2024-07-26 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fmsApp', '0008_post_password'),
    ]

    operations = [
        migrations.CreateModel(
            name='VaultFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(max_length=255, upload_to='vault_files/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
