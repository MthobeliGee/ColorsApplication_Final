# Generated by Django 5.0.2 on 2024-05-15 11:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manage_personnel', '0040_alter_federationpersonel_dateadded'),
    ]

    operations = [
        migrations.AlterField(
            model_name='federationpersonel',
            name='DateAdded',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 15, 13, 15, 14, 854356)),
        ),
    ]