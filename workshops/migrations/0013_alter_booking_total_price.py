# Generated by Django 5.0.7 on 2024-09-16 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshops', '0012_booking_stripe_checkout_id_booking_total_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='total_price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
