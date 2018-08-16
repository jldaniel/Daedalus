# Generated by Django 2.1 on 2018-08-15 00:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modeling', '0002_system_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='system',
            name='status',
            field=models.CharField(choices=[('READY', 'READY'), ('TRAINING', 'TRAINING'), ('ERROR', 'ERROR')], default='IDLE', max_length=8),
        ),
    ]
