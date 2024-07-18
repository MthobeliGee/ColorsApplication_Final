# Generated by Django 5.0.2 on 2024-03-20 10:07

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0028_committeemember_is_deleted_alter_apparel_dateadded_and_more'),
        ('manage_personnel', '0031_alter_federationpersonel_dateadded'),
    ]

    operations = [
        migrations.AddField(
            model_name='represantative',
            name='FederationPersonel',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='manage_personnel.federationpersonel'),
        ),
        migrations.AlterField(
            model_name='apparel',
            name='DateAdded',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 20, 12, 7, 8, 822620)),
        ),
        migrations.AlterField(
            model_name='apparel',
            name='DateCreated',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 20, 12, 7, 8, 822620)),
        ),
        migrations.AlterField(
            model_name='application',
            name='ApplicationDate',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 20, 12, 7, 8, 821619)),
        ),
        migrations.AlterField(
            model_name='application',
            name='DateCreated',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 20, 12, 7, 8, 821619)),
        ),
        migrations.AlterField(
            model_name='committeemember',
            name='RequestDate',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 20, 12, 7, 8, 820619)),
        ),
        migrations.AlterField(
            model_name='committeemember',
            name='ResponseDate',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 20, 12, 7, 8, 820619)),
        ),
        migrations.AlterField(
            model_name='feddocuments',
            name='DateAdded',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 20, 12, 7, 8, 819620)),
        ),
        migrations.AlterField(
            model_name='federation',
            name='dateSelected',
            field=models.DateField(default=datetime.datetime(2024, 3, 20, 12, 7, 8, 818620)),
        ),
        migrations.AlterField(
            model_name='federation',
            name='date_approved',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 20, 12, 7, 8, 818620)),
        ),
        migrations.AlterField(
            model_name='federation',
            name='date_requested',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 20, 12, 7, 8, 818620)),
        ),
    ]