# Generated by Django 2.0.4 on 2018-09-18 20:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0013_auto_20180918_0351'),
    ]

    operations = [
        migrations.RenameField(
            model_name='scenario',
            old_name='scenario_name',
            new_name='name',
        ),
    ]
