# Generated by Django 3.2.14 on 2024-09-15 00:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0006_auto_20240915_0005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='latitude',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='longitude',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
