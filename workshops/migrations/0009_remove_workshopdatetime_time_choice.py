# Generated by Django 5.1a1 on 2024-06-28 19:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workshops', '0008_workshop_is_canceled'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workshopdatetime',
            name='time_choice',
        ),
    ]