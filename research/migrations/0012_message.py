# Generated by Django 2.0.4 on 2018-05-23 22:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('research', '0011_auto_20180508_0034'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('role', models.CharField(max_length=1, null=True)),
                ('creation_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('transcript', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='research.Transcript')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
