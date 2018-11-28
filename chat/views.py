from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
import json
from .models import Scenario, TFQuestion, ChatRoom, MessageCode
from research.models import TFAnswer, Transcript, Message
from rest_framework import viewsets
from .serializers import ChatRoomSerializer
from django.shortcuts import get_object_or_404
from .forms import ScenarioForm
from django.http import HttpResponseRedirect
from django.forms import modelformset_factory
from .utils import process_codes

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

        questions = TFQuestion.objects.filter(scenario=scenario)

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
            if (new_scene.scenario_name == scenario.scenario_name and
                new_scene.student_background == scenario.student_background and
                new_scene.student_profile == scenario.student_profile and
                new_scene.teacher_background == scenario.teacher_background and
                new_scene.teacher_objective == scenario.teacher_objective and
                new_scene.visible_to_players != scenario.visible_to_players
                ):
                scenario.visible_to_players = new_scene.visible_to_players
                scenario.save()
                return HttpResponseRedirect('/scenarios/chat/scenario/')

            new_scene.pk = None
            new_scene.parent = scenario
            new_scene.save()
            scenario.visible_to_players = False
            scenario.save()

            for q in questions:
                q.scenario = new_scene
                q.save()

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

def onboard_inst(request):
    return render(request, 'chat/onboard_instructions.html')


def onboard1(request):
    text = """T: What do you know about continents?;eliciting;Eliciting because this is the first question on the topic of continents
    S: There’s like... America... and England... and Africa... and maybe India?;;
    T: Well, some of those are continents.;evaluating;Evaluating because this is a rephrasing of “Partially correct,” a way of telling students if they are correct.
    S: I know that there are 7 continents!;;
    # T: Very good. What do you know about oceans? Evaluating and Eliciting because “Very good” tells the student that they are correct and then there is a question asked on a new topic, oceans. 
    # S: There’s the Atlantic Ocean, that’s the one I go swimming in sometimes.
    # T: That’s right. Evaluating because it simply tells the student that they are correct
    # S: And there’s the Pacific Ocean, that’s on the other side of the country.
    # T: Yep. Evaluating because it tell the student they are correct OR None because it conveys that the teacher heard and acknowledges what the student said without telling the student if they are correct. 
    # S: Polar bears live in the Arctic Ocean so that’s another one. I think there’s one more, but I don’t remember what it is.
    # T: You’re probably thinking of the Indian Ocean. Telling because here the teacher directly gives the student a piece of information they did not recall. 
    # S: Oh, okay. Does that mean India is not a continent?
    # T: No, it isn’t, but that’s okay. Evaluating because “No, it isn’t” tells the student they are incorrect. 
    # T: Do you know what countries border the mainland United States? Eliciting because this a question on a topic (bordering countries) which has not been asked about before. 
    # S: There’s Canada to the north and Mexico to the south.
    # T: Very good. What about Hawaii? Evaluating and Probing because the teacher starts out by letting the student know that they are correct and then asks a question on the same topic (bordering countries) as before.
    # S: That’s an island in the Pacific Ocean.
    # T: I see. What about Alaska? Probing because the question is once again a follow-up question on bordering countries.  “I see” doesn’t tell the student whether they are correct, just that the teacher heard them so doesn’t get a code. 
    # S: That’s also an island... somewhere.
    # T: Interesting. None because this once again doesn’t tell the student whether they are correct. 
    *bell rings*"""

    lines = text.split("\n")
    checked = []
    messages = []
    answers = []
    feedback = []
    for line in lines:
        item = line.split(";")
        print(item)
        messages.append(item[0])
        answers.append(item[1])
        feedback.append(item[2])
    # submitted = False
    # if request.method == 'POST':
    #     checked = process_codes(request)
    #     submitted = True
    return render(request, 'chat/coding_onboarding.html', {"message":zip(messages,answers,feedback),"nextpage":"/chat/onboard2","checked":checked,"submitted":submitted})


def onboard2(request):
    text = """T: Hi! Do you know what we are learning today?
        S: Something about writing sentences?
        T: What do you know about parts of speech?
        S: I know that there are nouns, which are things, and verbs, which are actions, and description words, but I don’t remember what they are called.
        T: Very good. Can you tell me more about nouns? Is “school” a noun?
        S: Yeah, a school is a type of thing.
        T: What about “idea” or “Eastern High School”? Are they nouns?
        S: Idea is a thing, so yeah. But Eastern High School isn’t a noun because it’s capitalized.
        T: Not quite.
        S: What did I get wrong?
        T: Nouns can be capitalized. “Eastern High School” is a ‘thing,’ right? Capitalized nouns are called proper nouns.
        S: Okay
        T: Do all words have a part of speech?
        S: I don’t know
        T: Okay.
        T: Let’s look at the sentence “I quickly ate a delicious cupcake.” What words can you classify as parts of speech?
        S: “I” and “cupcake” are nouns. “Ate” is a verb. And “quickly” and “delicious” are description words. I don’t know about “a.” Am I right?
        T: I’m not going to answer that right now because I would like to know what you remember before class starts.
        *bell rings*"""
    messages = text.split("\n")
    checked = []
    submitted = False
    if request.method == 'POST':
        checked = process_codes(request)
        submitted = True
    return render(request, 'chat/coding_onboarding.html', {"messages":messages,"nextpage":"/chat/onboard3","checked":checked,"submitted":submitted})


def onboard3(request):
    text = """T: Hello, Matthew. I’m hoping you can help me with something for a minute.
        T: I know you did a dinosaur project with Mr. Jones last year in first grade. Can you tell me what you remember about dinosaurs and fossils?
        S: I made a velociraptor like in Jurassic Park and I put feathers on mine. Mine was the only one like that!
        T: That sounds really cool. Do you think there are still dinosaurs today?
        S: No, they all died. 
        T: How did that happen?
        S: Umm... I’m not sure. Maybe humans needed more space?
        T: Does that mean that humans and dinosaurs existed at the same time?
        S: I guess so. Before the Ice Age, right?
        T: I’ll be happy to tell you during class today.
        S: Oh... Okay.
        T: What do you know about fossils?
        S: They’re leftovers of dead animals.
        T: So a fossil of a bone is made of bone?
        S: Yeah!
        T: Can fossils be only of bones?
        S: No... They can be of feathers, too, and seashells.
        T: Very good. Is there any connection between fossils and extinct species?
        S: Not really...
        T: Okay. Thank you for talking to me! I now know what we’re going to talk about today.
        *bell rings*"""
    messages = text.split("\n")
    checked = []
    submitted = False
    if request.method == 'POST':
        checked = process_codes(request)
        submitted = True
    return render(request, 'chat/coding_onboarding.html', {"messages":messages,"nextpage":"/chat/onboard4","checked":checked,"submitted":submitted})


def onboard4(request):
    text = """T: Hi, Sarah! Is it okay if I ask you a few questions about negative numbers before class? I want to get an idea of what you already know.
        S: Okay, Mr. Thomas. What do you want to know?
        T: Can you tell me what a negative number is?
        S: It’s like if you owe someone something or have to give someone stuff. 
        T: Very good. Do you know how to write a negative number?
        S: Yeah, you just take the number and put a minus sign in front of it.
        T: So, if I write “-3,” what does that mean?
        S: It means negative three or that someone owes 3 of something.
        T: That’s right. Is negative three more or less than zero?
        S: Less. Because having nothing is better than owing someone stuff.
        T: That’s right, Sarah. What about -2 and -3? Which do you think is bigger?
        S: Well, 3 is bigger than 2, but I would rather owe someone 2 things than 3. So I’m not sure.
        T: That’s very good thinking.
        S: So which one is right?
        T: I’ll tell you in class, okay?
        S: Okay.
        T: So what happens in we add -3 and 2?
        S: Well, if you owe someone 3 apples and then get 2 apples, then you can give them away and only owe 1 apple. So -1, Mr. Thomas?
        T: That’s right. What about if we add -3 and -2?
        S: Well if you owe someone 3 apples and owe someone else 2 apples, then together you owe 5 apples. So -5.
        T: Nice job! Thanks for talking to me, Sarah.
        S: You’re welcome
        *bell rings*"""
    messages = text.split("\n")
    checked = []
    submitted = False
    if request.method == 'POST':
        checked = process_codes(request)
        submitted = True
    return render(request, 'chat/coding_onboarding.html', {"messages":messages,"nextpage":"/","checked":checked,"submitted":submitted})