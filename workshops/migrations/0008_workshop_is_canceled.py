# Generated by Django 5.1a1 on 2024-06-27 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshops', '0007_delete_cartitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='workshop',
            name='is_canceled',
            field=models.BooleanField(default=False),
        ),
    ]
