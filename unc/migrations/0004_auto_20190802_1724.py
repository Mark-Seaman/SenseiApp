# Generated by Django 2.2.3 on 2019-08-02 23:24

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('unc', '0003_merge_20190802_1632'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='due',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 2, 23, 24, 49, 825939, tzinfo=utc), editable=False, null=True),
        ),
    ]