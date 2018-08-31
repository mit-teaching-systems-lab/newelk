# Generated by Django 2.0.4 on 2018-05-23 22:06

from django.db import migrations
from datetime import timedelta

def transcript_to_message(apps, schema_editor):
    Transcript = apps.get_model('research', 'Transcript')
    Message = apps.get_model('research', 'Message')
    User = apps.get_model('auth', 'user')
    for item in Transcript.objects.all():
        text_array = item.transcript.split('\n')
        delta = timedelta(seconds=20);
        for text in text_array:
            delta += timedelta(seconds=20)
            message_array = text.split(': ', 1)
            creation_time = item.creation_time + delta
            if message_array[0].startswith("***") or message_array[0]=='':
                #system messages filter out here
                m = Message(text=message_array[0],
                            transcript=item,
                            creation_time=creation_time)
            else:
                user = User.objects.get(username=message_array[0])
                m = Message(user=user,
                            text=message_array[1],
                            transcript=item,
                            creation_time=creation_time)
            m.save()

class Migration(migrations.Migration):

    dependencies = [
        ('research', '0012_message'),
    ]

    operations = [
        migrations.RunPython(transcript_to_message),
    ]


