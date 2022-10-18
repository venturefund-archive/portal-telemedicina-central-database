# Generated by Django 3.2.14 on 2022-10-18 12:21

import datetime
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.expressions


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Vaccine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('system', models.CharField(choices=[('CVX', 'http://hl7.org/fhir/sid/cvx'), ('BRI', 'https://integracao.esusab.ufsc.br/ledi/documentacao/referencias/dicionario.html#imunobiologico')], help_text='Which system of codes is used on FHIR to define the vaccine codes.', max_length=3)),
                ('code', models.PositiveSmallIntegerField(help_text='Vaccine code used defined on a specific system.')),
                ('display', models.CharField(help_text='Small text description from display field on FHIR.', max_length=200)),
                ('description', models.CharField(help_text='Full text description of the vaccine.', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='VaccineDose',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('minimum_recommended_age', models.PositiveIntegerField(blank=True, default=None, help_text='The minimum age, in months, if the administration can be performed within a range. If there is no range, leave it blank and use only the maximum recommended age.', null=True)),
                ('maximum_recommended_age', models.PositiveIntegerField(help_text='The maximum age, in months, if the administration can be performed within a range. If there is no range, this is the recommended age.')),
                ('dose_order', models.PositiveSmallIntegerField(help_text='The order of this dose in the vaccination schedule.')),
                ('booster', models.BooleanField(help_text='Check if this is considered a booster shot in the vaccination schedule.')),
                ('gender_recommendation', models.CharField(choices=[('B', 'Both'), ('M', 'Male'), ('F', 'Female')], default='B', help_text='Select if this dose is gender specific.', max_length=1)),
                ('vaccine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vaccines', to='vaccines.vaccine')),
            ],
        ),
        migrations.CreateModel(
            name='VaccineAlert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient_id', models.PositiveIntegerField(help_text='Patient ID from FHIR.')),
                ('issue', models.CharField(choices=[('Delayed', 'Dose is delayed')], help_text='Vaccination issue communicated by this alert.', max_length=50)),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('active', models.BooleanField(default=True, help_text='Check if this alert is active.')),
                ('vaccine_dose', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vaccine_doses', to='vaccines.vaccinedose')),
            ],
        ),
        migrations.AddIndex(
            model_name='vaccine',
            index=models.Index(fields=['system', 'code'], name='vaccines_va_system_ed9718_idx'),
        ),
        migrations.AddIndex(
            model_name='vaccine',
            index=models.Index(fields=['code', 'system'], name='vaccines_va_code_8089a0_idx'),
        ),
        migrations.AddConstraint(
            model_name='vaccine',
            constraint=models.UniqueConstraint(fields=('system', 'code'), name='unique_system_code'),
        ),
        migrations.AddIndex(
            model_name='vaccinedose',
            index=models.Index(fields=['vaccine'], name='vaccines_va_vaccine_aa69bc_idx'),
        ),
        migrations.AddIndex(
            model_name='vaccinedose',
            index=models.Index(fields=['maximum_recommended_age'], name='vaccines_va_maximum_b6fbd2_idx'),
        ),
        migrations.AddConstraint(
            model_name='vaccinedose',
            constraint=models.CheckConstraint(check=models.Q(('maximum_recommended_age__gt', django.db.models.expressions.F('minimum_recommended_age'))), name='age_max_greater_age_min'),
        ),
        migrations.AddConstraint(
            model_name='vaccinedose',
            constraint=models.UniqueConstraint(fields=('vaccine', 'dose_order', 'gender_recommendation'), name='unique_vaccine_dose_order_gender_recommendation'),
        ),
        migrations.AddIndex(
            model_name='vaccinealert',
            index=models.Index(fields=['patient_id'], name='vaccines_va_patient_ae329f_idx'),
        ),
        migrations.AddIndex(
            model_name='vaccinealert',
            index=models.Index(fields=['issue'], name='vaccines_va_issue_c78b50_idx'),
        ),
        migrations.AddIndex(
            model_name='vaccinealert',
            index=models.Index(fields=['created_at'], name='vaccines_va_created_c9b1f8_idx'),
        ),
        migrations.AddConstraint(
            model_name='vaccinealert',
            constraint=models.UniqueConstraint(fields=('vaccine_dose', 'patient_id', 'issue'), name='unique_dose_alert_type_per_patient'),
        ),
    ]
