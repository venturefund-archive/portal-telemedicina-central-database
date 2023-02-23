# Generated by Django 3.2.14 on 2023-02-16 16:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vaccines', '0004_historicalvaccine_historicalvaccinealert_historicalvaccinealerttype_historicalvaccinedose_historical'),
    ]

    operations = [
        migrations.CreateModel(
            name='VaccineProtocol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Protocol Name', max_length=255)),
                ('description', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveIndex(
            model_name='vaccinealert',
            name='vaccines_va_patient_ae329f_idx',
        ),
        migrations.AlterField(
            model_name='vaccinealert',
            name='vaccine_dose',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vaccine_alerts', to='vaccines.vaccinedose'),
        ),
        migrations.AddIndex(
            model_name='vaccinealert',
            index=models.Index(fields=['patient_id', 'vaccine_dose'], name='vaccines_va_patient_58e3f7_idx'),
        ),
        migrations.AddField(
            model_name='vaccineprotocol',
            name='vaccine_doses',
            field=models.ManyToManyField(to='vaccines.VaccineDose'),
        ),
        migrations.AddIndex(
            model_name='vaccineprotocol',
            index=models.Index(fields=['name'], name='vaccines_va_name_b5701e_idx'),
        ),
    ]