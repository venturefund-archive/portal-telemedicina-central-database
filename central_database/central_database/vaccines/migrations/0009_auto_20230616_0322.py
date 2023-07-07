# Generated by Django 3.2.14 on 2023-06-16 03:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0007_auto_20230616_0259'),
        ('vaccines', '0008_auto_20230616_0259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vaccinealert',
            name='fhir_store',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='customers.fhirstore'),
        ),
        migrations.AlterField(
            model_name='vaccinestatus',
            name='fhir_store',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='customers.fhirstore'),
        ),
    ]
