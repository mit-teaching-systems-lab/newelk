# Generated by Django 2.0.4 on 2018-09-18 23:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('chat', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('role', models.CharField(max_length=1, null=True)),
                ('creation_time', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='TFAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_answer', models.TextField(null=True)),
                ('correct_answer', models.TextField(null=True)),
                ('creation_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('question', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='chat.TFQuestion')),
            ],
        ),
        migrations.CreateModel(
            name='Transcript',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transcript', models.TextField(default='')),
                ('last_line', models.TextField(default='')),
                ('room_name', models.TextField()),
                ('creation_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('scenario', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='chat.Scenario')),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='tfanswer',
            name='transcript',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='research.Transcript'),
        ),
        migrations.AddField(
            model_name='tfanswer',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='message',
            name='transcript',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='research.Transcript'),
        ),
        migrations.AddField(
            model_name='message',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
