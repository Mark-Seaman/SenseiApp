# Generated by Django 2.2.3 on 2019-08-10 21:20

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('unc', '0013_auto_20190807_0737'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='unc.Project'),
        ),
        migrations.AlterField(
            model_name='project',
            name='due',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 10, 15, 20, 34, 927721), editable=False, null=True),
        ),
    ]
