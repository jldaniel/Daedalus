# Generated by Django 2.1 on 2018-08-15 01:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modeling', '0005_inputvariable_outputvariable'),
    ]

    operations = [
        migrations.AddField(
            model_name='inputvariable',
            name='lower_bound',
            field=models.FloatField(default=0.0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='inputvariable',
            name='upper_bound',
            field=models.FloatField(default=1.0),
            preserve_default=False,
        ),
    ]
