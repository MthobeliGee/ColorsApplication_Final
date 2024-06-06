# Generated by Django 5.0.2 on 2024-03-14 14:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0011_alter_apparel_dateadded_alter_apparel_datecreated_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apparel',
            name='DateAdded',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 14, 16, 14, 1, 716600)),
        ),
        migrations.AlterField(
            model_name='apparel',
            name='DateCreated',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 14, 16, 14, 1, 716600)),
        ),
        migrations.AlterField(
            model_name='application',
            name='ApplicationDate',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 14, 16, 14, 1, 716600)),
        ),
        migrations.AlterField(
            model_name='application',
            name='DateCreated',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 14, 16, 14, 1, 716600)),
        ),
        migrations.AlterField(
            model_name='feddocuments',
            name='DateAdded',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 14, 16, 14, 1, 715095)),
        ),
        migrations.AlterField(
            model_name='federation',
            name='dateSelected',
            field=models.DateField(default=datetime.datetime(2024, 3, 14, 16, 14, 1, 715095)),
        ),
        migrations.AlterField(
            model_name='federation',
            name='date_approved',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 14, 16, 14, 1, 715095)),
        ),
        migrations.AlterField(
            model_name='federation',
            name='date_requested',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 14, 16, 14, 1, 715095)),
        ),
    ]
