# Generated by Django 2.0.4 on 2018-05-03 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('research', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transcript',
            name='transcript',
            field=models.TextField(default=''),
        ),
    ]
