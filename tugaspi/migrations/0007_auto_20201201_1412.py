# Generated by Django 3.1.4 on 2020-12-01 14:12

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tugaspi', '0006_auto_20201130_0731'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['price']},
        ),
        migrations.AddField(
            model_name='sales',
            name='state',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=100, unique=True, validators=[django.core.validators.RegexValidator('^[a-z A-Z]*$', 'Only alphanumeric characters are allowed.')], verbose_name='Name'),
        ),
    ]
