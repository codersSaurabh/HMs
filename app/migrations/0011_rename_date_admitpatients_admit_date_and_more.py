# Generated by Django 5.0.3 on 2024-04-12 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_patient_gender'),
    ]

    operations = [
        migrations.RenameField(
            model_name='admitpatients',
            old_name='Date',
            new_name='Admit_Date',
        ),
        migrations.RenameField(
            model_name='admitpatients',
            old_name='time',
            new_name='Admit_time',
        ),
        migrations.AddField(
            model_name='admitpatients',
            name='Discharge_Date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='admitpatients',
            name='Bed_no',
            field=models.IntegerField(default=''),
        ),
    ]
