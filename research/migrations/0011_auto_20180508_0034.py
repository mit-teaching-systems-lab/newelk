# Generated by Django 2.0.4 on 2018-05-08 00:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('research', '0010_tfanswer_transcript'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tfanswer',
            name='question',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='chat.TFQuestion'),
        ),
    ]