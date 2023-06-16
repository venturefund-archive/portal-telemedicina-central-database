# Generated by Django 3.2.14 on 2023-06-15 14:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0005_auto_20230615_1435'),
        ('vaccines', '0006_auto_20230605_1026'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalvaccinealert',
            name='fhir_store_id',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='customers.fhirstore'),
        ),
        migrations.AddField(
            model_name='historicalvaccinestatus',
            name='fhir_store_id',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='customers.fhirstore'),
        ),
        migrations.AddField(
            model_name='vaccinealert',
            name='fhir_store_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='customers.fhirstore'),
        ),
        migrations.AddField(
            model_name='vaccineprotocol',
            name='client',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='customers.client'),
        ),
        migrations.AddField(
            model_name='vaccinestatus',
            name='fhir_store_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='customers.fhirstore'),
        ),
    ]
