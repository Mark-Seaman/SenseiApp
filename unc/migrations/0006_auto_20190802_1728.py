# Generated by Django 2.2.3 on 2019-08-02 23:28

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('unc', '0005_auto_20190802_1726'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='due',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 2, 23, 28, 5, 424312, tzinfo=utc), editable=False, null=True),
        ),
    ]