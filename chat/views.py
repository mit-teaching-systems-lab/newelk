from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
import json
from .models import Scenario, TFQuestion, ChatRoom
from research.models import TFAnswer, Transcript, Message
from rest_framework import viewsets
from .serializers import ChatRoomSerializer

class ChatRoomViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = ChatRoom.objects.all().order_by('name')
    serializer_class = ChatRoomSerializer

def select_role(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')
    scenarios = Scenario.objects.all()
    return render(request, 'chat/select_role.html')

def select_scenario(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')
    scenarios = Scenario.objects.all()
    return render(request, 'chat/select_scenario.html', {'scenarios': scenarios})

def join_scenario(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')
    chatrooms = ChatRoom.objects.all()
    return render(request, 'chat/join_scenario.html', {'chatrooms': chatrooms})

def room(request, role, scenario, room_name):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')

    room_details = get_room_details(role, scenario, room_name)

    return render(request, 'chat/room.html', room_details)

def join_room(request):
    return render(request, 'chat/join_room.html')

def quiz(request, role, scenario, room_name):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')
    scene = Scenario.objects.get(pk=scenario)
    questions = TFQuestion.objects.filter(scenario=scene)
    transcript = Transcript.objects.filter(users=request.user).latest("creation_time")
    transcript.messages = Message.objects.filter(transcript=transcript).order_by("creation_time")
    if request.method == 'POST':
        for pk in request.POST:
            if not pk == "csrfmiddlewaretoken":
                question = TFQuestion.objects.get(pk=pk)
                answer = TFAnswer(user_answer=request.POST[pk],
                                  correct_answer=question.answer,
                                  question=question,
                                  user=request.user,
                                  transcript=transcript)
                answer.save()
        return redirect('/accounts/profile')
    else:
        quiz_context = get_room_details(role, scenario, room_name)
        quiz_context.update({'transcript':transcript, 'questions':questions})
        return render(request, 'chat/quiz.html', quiz_context)

def get_room_details(role, scenario, room_name):
    scene = Scenario.objects.get(pk=scenario)

    room_details = {
        'room_name_json': mark_safe(json.dumps(room_name)),
        'scenario_name': scene.scenario_name,
        'scenario': scenario,
        'role': role,
        'student_background': scene.student_background,
        'student_profile': scene.student_profile,
        'student_hints': scene.student_hints,
        'teacher_background': scene.teacher_background,
        'teacher_objective': scene.teacher_objective,
        'teacher_hints': scene.teacher_hints,
    }
    if role == 's':
        room_details.pop('teacher_background', None)
        room_details.pop('teacher_objective', None)
        room_details.pop('teacher_hints', None)

    if role == 't':
        room_details.pop('student_background', None)
        room_details.pop('student_profile', None)
        room_details.pop('student_hints', None)

    return room_details
