# Generated by Django 2.1.4 on 2018-12-16 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0009_auto_20181216_2058'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatnode',
            name='type',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]