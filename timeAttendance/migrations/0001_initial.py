# Generated by Django 2.2.5 on 2019-09-27 16:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeDetail',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=32)),
                ('gender', models.IntegerField()),
                ('image_name', models.CharField(max_length=500)),
                ('department', models.CharField(max_length=500, null=True)),
                ('branch', models.CharField(max_length=500, null=True)),
                ('status', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='TerminalDetails',
            fields=[
                ('terminal_id', models.IntegerField(primary_key=True, serialize=False)),
                ('terminal_ip', models.CharField(max_length=100)),
                ('terminal_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeAttendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('capture_time', models.CharField(max_length=200)),
                ('capture_location', models.CharField(max_length=100)),
                ('EmployeeDetail', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='timeAttendance.EmployeeDetail')),
            ],
        ),
    ]
