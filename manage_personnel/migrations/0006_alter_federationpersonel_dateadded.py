# Generated by Django 5.0.2 on 2024-03-07 11:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manage_personnel', '0005_alter_federationpersonel_dateadded'),
    ]

    operations = [
        migrations.AlterField(
            model_name='federationpersonel',
            name='DateAdded',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 7, 13, 20, 30, 223548)),
        ),
    ]
