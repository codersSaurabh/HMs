# Generated by Django 5.0.3 on 2024-04-12 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_rename_date_admitpatients_admit_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admitpatients',
            name='Bed_no',
            field=models.IntegerField(default=0),
        ),
    ]
