# Generated by Django 5.0.2 on 2024-03-14 15:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manage_personnel', '0015_alter_federationpersonel_dateadded'),
    ]

    operations = [
        migrations.AlterField(
            model_name='federationpersonel',
            name='DateAdded',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 14, 17, 59, 21, 384253)),
        ),
    ]