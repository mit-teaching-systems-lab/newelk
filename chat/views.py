from django.shortcuts import render
from django.utils.safestring import mark_safe
import json
from .models import Scenario

def index(request):
    scenarios = Scenario.objects.all()
    return render(request, 'chat/index.html', {'scenarios': scenarios})

def room(request, room_name):

    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })