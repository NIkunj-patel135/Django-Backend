# Generated by Django 5.0.1 on 2024-02-06 10:52

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0003_alter_students_billinginfo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='students',
            name='wishlist',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), blank=True, size=10),
        ),
    ]
