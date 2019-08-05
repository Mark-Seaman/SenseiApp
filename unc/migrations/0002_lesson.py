# Generated by Django 2.2.3 on 2019-08-02 22:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('unc', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week', models.IntegerField(default=1)),
                ('date', models.DateTimeField(default=None, editable=False, null=True)),
                ('lesson', models.IntegerField(default=1)),
                ('topic', models.CharField(default='none', max_length=100)),
                ('reading', models.CharField(default='none', max_length=100)),
                ('course', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='unc.Course')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='unc.Project')),
            ],
        ),
    ]