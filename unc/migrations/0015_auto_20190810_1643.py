# Generated by Django 2.2.3 on 2019-08-10 22:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unc', '0014_auto_20190810_1520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='due',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 10, 16, 43, 0, 278601), editable=False, null=True),
        ),
    ]
