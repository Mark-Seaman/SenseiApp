# Generated by Django 2.2.4 on 2019-08-14 16:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unc', '0021_auto_20190813_1720'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='due',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 14, 10, 6, 2, 964774), editable=False, null=True),
        ),
    ]