# Generated by Django 2.1 on 2018-08-15 04:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('modeling', '0006_auto_20180815_0138'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('runs', models.IntegerField(default=0)),
                ('data', models.TextField(null=True)),
                ('system', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='datasets', to='modeling.System')),
            ],
        ),
    ]