# Generated by Django 3.1.3 on 2020-11-24 16:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tugaspi', '0003_auto_20201124_1605'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sales',
            name='total',
        ),
    ]
