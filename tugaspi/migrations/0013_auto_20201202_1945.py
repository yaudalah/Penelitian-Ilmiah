# Generated by Django 3.1.4 on 2020-12-02 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tugaspi', '0012_auto_20201202_1938'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='hawkerproduct',
            constraint=models.UniqueConstraint(fields=('hawker_id', 'product_id'), name='unique hawker product'),
        ),
    ]
