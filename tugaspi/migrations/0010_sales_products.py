# Generated by Django 3.1.4 on 2020-12-02 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tugaspi', '0009_auto_20201202_1632'),
    ]

    operations = [
        migrations.AddField(
            model_name='sales',
            name='products',
            field=models.ManyToManyField(through='tugaspi.SalesProduct', to='tugaspi.Product'),
        ),
    ]