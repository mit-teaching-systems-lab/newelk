# Generated by Django 2.0.4 on 2018-05-07 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('research', '0007_tfanswer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tfanswer',
            name='answer',
            field=models.TextField(),
        ),
    ]
