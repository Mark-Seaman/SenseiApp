# Generated by Django 2.2.4 on 2019-08-19 22:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unc', '0036_merge_20190819_1611'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='due',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 19, 16, 11, 17, 107310), editable=False, null=True),
        ),
    ]