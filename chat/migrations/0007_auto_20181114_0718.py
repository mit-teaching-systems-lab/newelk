# Generated by Django 2.1.3 on 2018-11-14 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0006_auto_20181114_0640'),
    ]

    operations = [
        migrations.AddField(
            model_name='messagecode',
            name='url',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='messagecode',
            name='other_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
