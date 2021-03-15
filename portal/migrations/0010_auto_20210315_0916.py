# Generated by Django 3.1.4 on 2021-03-15 03:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0009_audit_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audit',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('matched', 'Matched'), ('unmatched', 'Unmatched')], default='unmatched', max_length=1000),
        ),
    ]
