# Generated by Django 5.1a1 on 2024-06-19 22:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workshops', '0006_workshop_image'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CartItem',
        ),
    ]
