# Generated by Django 2.1 on 2018-09-01 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modeling', '0013_auto_20180901_1713'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='applied',
            field=models.BooleanField(default=False),
        ),
    ]
