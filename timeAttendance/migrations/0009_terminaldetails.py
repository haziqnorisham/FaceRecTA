# Generated by Django 2.2.5 on 2019-09-23 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timeAttendance', '0008_auto_20190923_1501'),
    ]

    operations = [
        migrations.CreateModel(
            name='TerminalDetails',
            fields=[
                ('terminal_id', models.IntegerField(primary_key=True, serialize=False)),
                ('terminal_ip', models.CharField(max_length=100)),
                ('terminal_name', models.CharField(max_length=100)),
            ],
        ),
    ]
