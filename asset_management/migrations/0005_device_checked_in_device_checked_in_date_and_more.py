# Generated by Django 4.2.5 on 2023-09-16 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asset_management', '0004_alter_device_checked_out_to'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='checked_in',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='device',
            name='checked_in_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='device',
            name='checked_out_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='device',
            name='condition',
            field=models.TextField(blank=True, null=True),
        ),
    ]
