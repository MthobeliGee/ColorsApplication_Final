# Generated by Django 5.0.2 on 2024-05-05 21:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0037_remove_sportsperson_status_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sportsperson',
            name='RepresatativeLevel',
        ),
        migrations.RemoveField(
            model_name='sportsperson',
            name='RepresatativeType',
        ),
        migrations.AddField(
            model_name='applicantapplication',
            name='RepresatativeLevel',
            field=models.CharField(default='Junior', max_length=50),
        ),
        migrations.AddField(
            model_name='applicantapplication',
            name='RepresatativeType',
            field=models.CharField(default='Athlete', max_length=50),
        ),
        migrations.AlterField(
            model_name='apparel',
            name='DateAdded',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 5, 23, 43, 12, 3414)),
        ),
        migrations.AlterField(
            model_name='apparel',
            name='DateCreated',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 5, 23, 43, 12, 3414)),
        ),
        migrations.AlterField(
            model_name='application',
            name='ApplicantsClosingDate',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 5, 23, 43, 12, 2415)),
        ),
        migrations.AlterField(
            model_name='application',
            name='ApplicationDate',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 5, 23, 43, 12, 2415)),
        ),
        migrations.AlterField(
            model_name='application',
            name='DateCreated',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 5, 23, 43, 12, 2415)),
        ),
        migrations.AlterField(
            model_name='committeemember',
            name='RequestDate',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 5, 23, 43, 12, 1428)),
        ),
        migrations.AlterField(
            model_name='committeemember',
            name='ResponseDate',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 5, 23, 43, 12, 1428)),
        ),
        migrations.AlterField(
            model_name='feddocuments',
            name='DateAdded',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 5, 23, 43, 12, 1428)),
        ),
        migrations.AlterField(
            model_name='federation',
            name='dateSelected',
            field=models.DateField(default=datetime.datetime(2024, 5, 5, 23, 43, 12, 416)),
        ),
        migrations.AlterField(
            model_name='federation',
            name='date_approved',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 5, 23, 43, 12, 416)),
        ),
        migrations.AlterField(
            model_name='federation',
            name='date_requested',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 5, 23, 43, 12, 416)),
        ),
    ]
