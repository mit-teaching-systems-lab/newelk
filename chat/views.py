from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
import json
from .models import Scenario, TFQuestion, ChatRoom
from research.models import TFAnswer, Transcript, Message
from rest_framework import viewsets
from .serializers import ChatRoomSerializer
from django.shortcuts import get_object_or_404
from .forms import ScenarioForm
from django.http import HttpResponseRedirect
from django.forms import modelformset_factory

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
    # scenarios = Scenario.objects.filter(children__isnull=True).filter(visible_to_players=True)
    scenarios = Scenario.objects.filter(visible_to_players=True)
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
    return render(request, 'chat/join_scenario.html')

def result(request):
    return render(request, 'chat/result.html')

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
        return redirect('/chat/result')
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

def scenario_creator(request):
    if request.method == 'POST':
        scenario_form = ScenarioForm(request.POST)
        if scenario_form.is_valid():
            new_scene = scenario_form.save()
            return HttpResponseRedirect('/scenarios/chat/scenario/%i/' % new_scene.pk)
    else:
        scenario_form = ScenarioForm()
        context = {
            'form': scenario_form,
        }
        return render(request, 'chat/scenario_editor.html', context)


def scenario_editor(request, pk):
    scenario = get_object_or_404(Scenario, pk=pk)
    # AuthorFormSet = modelformset_factory(Author, fields=('name', 'title'))
    ScenarioFormSet = modelformset_factory(Scenario, exclude=('parent','owner','creation_time'))

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        # scenario_form = ScenarioForm(request.POST, instance=scenario)
        scenario_form = ScenarioForm(request.POST)
        # Check if the form is valid:
        if scenario_form.is_valid():
            # process the data in form.cleaned_data
            # new_scene = Scenario.objects.create(scenario_form.cleaned_data)
            # scenario.pk = None
            # scenario.save()
            print(request.POST)
            new_scene = scenario_form.save(commit=False)
            new_scene.pk = None
            new_scene.parent = scenario
            new_scene.save()
            scenario.visible_to_players = False
            scenario.save()

            # Scenario.objects.rebuild()
            Scenario.objects.partial_rebuild(scenario.tree_id)

            # redirect to a new URL:
            return HttpResponseRedirect('/scenarios/chat/scenario/')
            # return HttpResponseRedirect('/scenarios/chat/scenario/%i/' % new_scene.pk)

    # If this is a GET (or any other method) create the default form.
    else:
        scenario_form = ScenarioForm(instance=scenario)
        # scenario_form = ScenarioFormSet(queryset=Scenario.objects.filter(pk=pk))
        # scenario_form = ScenarioForm(request.POST, instance=scenario)

    context = {
        'form': scenario_form,
        'scenario': scenario,
    }

    print(scenario_form)

    return render(request, 'chat/scenario_editor.html', context)

def onboard1(request):
    text = """T: What do you know about continents? Eliciting
        S: There’s like... America... and England... and Africa... and maybe India?
        T: Well, some of those are continents. Evaluating/Telling
        S: I know that there are 7 continents!
        T: Very good. What do you know about oceans? Evaluating, Eliciting
        S: There’s the Atlantic Ocean, that’s the one I go swimming in sometimes.
        T: That’s right. Evaluating
        S: And there’s the Pacific Ocean, that’s on the other side of the country.
        T: Yep. N/A
        S: Polar bears live in the Arctic Ocean so that’s another one. I think there’s one more, but I don’t remember what it is.
        T: You’re probably thinking of the Indian Ocean. Telling
        S: Oh, okay. Does that mean India is not a continent?
        T: No, it isn’t, but that’s okay. Evaluating
        T: Do you know what countries border the mainland United States? Eliciting
        S: There’s Canada to the north and Mexico to the south.
        T: Very good. What about Hawaii? Evaluating, Eliciting/Probing
        S: That’s an island in the Pacific Ocean.
        T: I see. What about Alaska? Eliciting/Probing
        S: That’s also an island... somewhere.
        T: Interesting. N/A
        *bell rings*
    """
    messages = text.split("\n")
    return render(request, 'chat/coding_onboarding.html', {"messages":messages)