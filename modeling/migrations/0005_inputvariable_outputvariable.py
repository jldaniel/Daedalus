# Generated by Django 2.1 on 2018-08-15 01:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('modeling', '0004_auto_20180815_0018'),
    ]

    operations = [
        migrations.CreateModel(
            name='InputVariable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('description', models.TextField()),
                ('system', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='input_variables', to='modeling.System')),
            ],
        ),
        migrations.CreateModel(
            name='OutputVariable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('description', models.TextField()),
                ('system', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='output_variables', to='modeling.System')),
            ],
        ),
    ]
