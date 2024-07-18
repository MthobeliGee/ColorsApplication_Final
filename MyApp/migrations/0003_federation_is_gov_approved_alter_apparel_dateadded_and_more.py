# Generated by Django 4.2.3 on 2024-03-07 10:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0002_federation_user_alter_apparel_dateadded_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='federation',
            name='is_Gov_approved',
            field=models.CharField(default='Pending', max_length=30),
        ),
        migrations.AlterField(
            model_name='apparel',
            name='DateAdded',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 7, 12, 1, 41, 912473)),
        ),
        migrations.AlterField(
            model_name='apparel',
            name='DateCreated',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 7, 12, 1, 41, 912473)),
        ),
        migrations.AlterField(
            model_name='application',
            name='ApplicationDate',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 7, 12, 1, 41, 912473)),
        ),
        migrations.AlterField(
            model_name='application',
            name='DateCreated',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 7, 12, 1, 41, 912473)),
        ),
        migrations.AlterField(
            model_name='feddocuments',
            name='DateAdded',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 7, 12, 1, 41, 912473)),
        ),
        migrations.AlterField(
            model_name='federation',
            name='FederationEmail',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='federation',
            name='dateSelected',
            field=models.DateField(default=datetime.datetime(2024, 3, 7, 12, 1, 41, 912473)),
        ),
    ]