# Generated by Django 2.2.5 on 2019-09-29 04:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('timeAttendance', '0002_auto_20190928_0142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeattendance',
            name='capture_location',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.SET_DEFAULT, to='timeAttendance.TerminalDetails'),
        ),
    ]
