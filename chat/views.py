from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
import json
from .models import Scenario, TFQuestion
from research.models import TFAnswer


def index(request):
    scenarios = Scenario.objects.all()
    return render(request, 'chat/index.html', {'scenarios': scenarios})

def room(request, role, scenario, room_name):
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
    if role=='s':
        room_details.pop('teacher_background', None)
        room_details.pop('teacher_objective', None)
        room_details.pop('teacher_hints', None)

    if role=='t':
        room_details.pop('student_background', None)
        room_details.pop('student_profile', None)
        room_details.pop('student_hints', None)

    return render(request, 'chat/room.html', room_details)

def quiz(request, role, scenario, room_name):
    scene = Scenario.objects.get(pk=scenario)
    questions = TFQuestion.objects.filter(scenario=scene)
    if request.method == 'POST':
        for pk in request.POST:
            if not pk == "csrfmiddlewaretoken":
                question = TFQuestion.objects.get(pk=pk)
                answer = TFAnswer(user_answer=request.POST[pk],correct_answer=question.answer,question=question.question,user=request.user)
                answer.save()
        return redirect('/accounts/profile')
    else:
        return render(request, 'chat/quiz.html', {'questions':questions})