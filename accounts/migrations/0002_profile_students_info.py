# Generated by Django 5.0.6 on 2024-06-15 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='students_info',
            field=models.TextField(blank=True),
        ),
    ]
