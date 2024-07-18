# Generated by Django 5.0.2 on 2024-03-19 07:28

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0019_remove_represantative_event_alter_apparel_dateadded_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='committeemember',
            name='application',
        ),
        migrations.AddField(
            model_name='application',
            name='Committee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='MyApp.committeemember'),
        ),
        migrations.AlterField(
            model_name='apparel',
            name='DateAdded',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 19, 9, 28, 51, 734055)),
        ),
        migrations.AlterField(
            model_name='apparel',
            name='DateCreated',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 19, 9, 28, 51, 734055)),
        ),
        migrations.AlterField(
            model_name='application',
            name='ApplicationDate',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 19, 9, 28, 51, 733052)),
        ),
        migrations.AlterField(
            model_name='application',
            name='DateCreated',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 19, 9, 28, 51, 733052)),
        ),
        migrations.AlterField(
            model_name='feddocuments',
            name='DateAdded',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 19, 9, 28, 51, 732049)),
        ),
        migrations.AlterField(
            model_name='federation',
            name='dateSelected',
            field=models.DateField(default=datetime.datetime(2024, 3, 19, 9, 28, 51, 732049)),
        ),
        migrations.AlterField(
            model_name='federation',
            name='date_approved',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 19, 9, 28, 51, 732049)),
        ),
        migrations.AlterField(
            model_name='federation',
            name='date_requested',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 19, 9, 28, 51, 732049)),
        ),
    ]