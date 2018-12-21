from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
import json
from .models import Scenario, TFQuestion, ChatRoom, MessageCode, ChatNode, OnboardLevel
from research.models import TFAnswer, Transcript, Message
from rest_framework import viewsets
from .serializers import ChatRoomSerializer, MessageCodeSerializer, ChatNodeSerializer
from django.shortcuts import get_object_or_404
from .forms import ScenarioForm
from django.http import HttpResponseRedirect
from django.forms import modelformset_factory
from .utils import get_random_object
import os

class ChatRoomViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = ChatRoom.objects.all().order_by('name')
    serializer_class = ChatRoomSerializer
    def get_queryset(self):
        user = self.request.user
        print('player looking for chatrooms')
        print(user)
        return ChatRoom.objects.all().order_by('name')



class MessageCodeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = MessageCode.objects.all()
    serializer_class = MessageCodeSerializer
    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(user=user)

class ChatNodeViewSet(viewsets.ModelViewSet):
    queryset = ChatNode.objects.all()
    serializer_class = ChatNodeSerializer

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
    try:
        key = os.environ['feedback']
        if key == 'True':
            give_feedback = True
        else:
            give_feedback = False
    except KeyError:
        give_feedback = True
    room_details['give_feedback'] = give_feedback
    return render(request, 'chat/room.html', room_details)

def join_room(request):
    return render(request, 'chat/join_scenario.html')


def result(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')
    transcript = Transcript.objects.filter(users=request.user).latest("creation_time")
    quiz_results = {}
    playercount = 0
    # transcript.messages = Message.objects.filter(transcript=t).order_by("creation_time")
    # if not transcript.messages:
    #     transcript.messages = {}
    #     transcript.messages['text'] = "no text found!"

    participants = transcript.users.distinct()
    scenario = transcript.scenario
    for person in participants:
        answers = TFAnswer.objects.filter(question__scenario=scenario, user=person, transcript=transcript)
        # answers = TFAnswer.objects.filter(transcript=latest_transcript,user=person)
        quiz_results[person.username] = {}
        quiz_results["question_details"] = {}
        for answer in answers:
            quiz_results[person.username][answer.question.pk] = answer.user_answer
            quiz_results["question_details"][answer.question.pk] = {answer.question.question: answer.correct_answer}
    playercount = participants.count

    print('showing profile')
    print(quiz_results)
    return render(request, 'chat/result.html',
                  {"quiz_results": quiz_results, "participant_count": playercount})


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
                print('changed visibility on scenario')
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
        T: Very good. What do you know about oceans?;evaluating,eliciting;Evaluating and Eliciting because “Very good” tells the student that they are correct and then there is a question asked on a new topic, oceans. 
        S: There’s the Atlantic Ocean, that’s the one I go swimming in sometimes.;;
        T: That’s right.;evaluating;Evaluating because it simply tells the student that they are correct
        S: And there’s the Pacific Ocean, that’s on the other side of the country.;;
        T: Yep.;evaluating;Evaluating because it tell the student they are correct OR None because it conveys that the teacher heard and acknowledges what the student said without telling the student if they are correct. 
        S: Polar bears live in the Arctic Ocean so that’s another one. I think there’s one more, but I don’t remember what it is.;;
        T: You’re probably thinking of the Indian Ocean.;telling;Telling because here the teacher directly gives the student a piece of information they did not recall. 
        S: Oh, okay. Does that mean India is not a continent?;;
        T: No, it isn’t, but that’s okay.;evaluating;Evaluating because “No, it isn’t” tells the student they are incorrect. 
        T: Do you know what countries border the mainland United States?;eliciting;Eliciting because this a question on a topic (bordering countries) which has not been asked about before. 
        S: There’s Canada to the north and Mexico to the south.;;
        T: Very good. What about Hawaii?;evaluating,probing;Evaluating and Probing because the teacher starts out by letting the student know that they are correct and then asks a question on the same topic (bordering countries) as before.
        S: That’s an island in the Pacific Ocean.;;
        T: I see. What about Alaska?;probing;Probing because the question is once again a follow-up question on bordering countries.  “I see” doesn’t tell the student whether they are correct, just that the teacher heard them so doesn’t get a code. 
        S: That’s also an island... somewhere.;;
        T: Interesting.;none;None because this once again doesn’t tell the student whether they are correct. 
        *bell rings*;;"""

    try:
        key = os.environ['feedback']
        if key == 'True':
            give_feedback = True
        else:
            give_feedback = False
    except KeyError:
        give_feedback = True

    lines = text.split("\n")
    messages = []
    answers = []
    feedback = []
    for line in lines:
        item = line.split(";")
        print(item)
        messages.append(item[0])
        answers.append(item[1])
        feedback.append(item[2])
    return render(request, 'chat/coding_onboarding.html', {"messages":zip(messages,answers,feedback),"nextpage":"/chat/onboard2","give_feedback":give_feedback})


def onboard2(request):
    text = """T: Hi! Do you know what we are learning today?;priming;Priming because this introduces what the topic of conversation will be about.
        S: Something about writing sentences?;;
        T: What do you know about parts of speech?;eliciting;Eliciting because it is the first question on the topic that the teacher wants to know about. 
        S: I know that there are nouns, which are things, and verbs, which are actions, and description words, but I don’t remember what they are called.;;
        T: Very good. Can you tell me more about nouns? Is “school” a noun?;evaluating,probing;Evaluating and Probing because “very good” tells the student that they are correct and the question directly asks about what the student just said and so is a follow-up question. 
        S: Yeah, a school is a type of thing.;;
        T: What about “idea” or “Eastern High School”? Are they nouns?;probing;Probing because this question is meant to expand more on what the student thinks of nouns. 
        S: Idea is a thing, so yeah. But Eastern High School isn’t a noun because it’s capitalized.;;
        T: Not quite.;evaluating;Evaluating because it tells the student whether they were correct.
        S: What did I get wrong?;;
        T: Nouns can be capitalized. “Eastern High School” is a ‘thing,’ right? Capitalized nouns are called proper nouns.;telling;Telling because this sentence directly tells the student information about the topic of discussion (parts of speech/nouns).
        S: Okay;;
        T: Do all words have a part of speech?;eliciting;Eliciting because this is a question about a “sub-topic” of parts of speech that has not been asked about before. 
        S: I don’t know;;
        T: Okay.;none;None because this is not asking anything or giving the student any information, but rather an acknowledgement of having heard the student. 
        T: Let’s look at the sentence “I quickly ate a delicious cupcake.” What words can you classify as parts of speech?;eliciting;Eliciting because this asks about a different subtopic in parts of speech, namely the skill of identifying specific words as parts of speech. 
        S: “I” and “cupcake” are nouns. “Ate” is a verb. And “quickly” and “delicious” are description words. I don’t know about “a.” Am I right?;;
        T: I’m not going to answer that right now because I would like to know what you remember before class starts.;priming;Priming because this is a ‘meta-comment’ about what the purpose of the conversation is and doesn’t directly touch the topic of discussion, parts of speech. 
        *bell rings*;;"""
    try:
        key = os.environ['feedback']
        if key == 'True':
            give_feedback = True
        else:
            give_feedback = False
    except KeyError:
        give_feedback = True
    lines = text.split("\n")
    messages = []
    answers = []
    feedback = []
    for line in lines:
        item = line.split(";")
        print(item)
        messages.append(item[0])
        answers.append(item[1])
        feedback.append(item[2])
    return render(request, 'chat/coding_onboarding.html', {"messages":zip(messages,answers,feedback),"nextpage":"/chat/onboard3","give_feedback":give_feedback})


def onboard3(request):
    text = """T: Hello, Matthew. I’m hoping you can help me with something for a minute.;priming;Priming because this is a meta-message that starts setting the tone for the conversation
        T: I know you did a dinosaur project with Mr. Jones last year in first grade. Can you tell me what you remember about dinosaurs and fossils?;priming,eliciting;Priming and Eliticing because the first sentence is another meta-message setting the tone and the question is the first question about dinosaurs and fossils. 
        S: I made a velociraptor like in Jurassic Park and I put feathers on mine. Mine was the only one like that!;;
        T: That sounds really cool. Do you think there are still dinosaurs today?;probing;Probing because the first comment does not fit any category and the question is a follow-up to asking about dinosaurs. 
        S: No, they all died.;;
        T: How did that happen?;probing;Probing because this is a follow up question to what was just said. 
        S: Umm... I’m not sure. Maybe humans needed more space?;;
        T: Does that mean that humans and dinosaurs existed at the same time?;probing;Probing because this is a follow-up question to what was just said.
        S: I guess so. Before the Ice Age, right?;;
        T: I’ll be happy to tell you during class today.;priming;Priming because this is a meta-message (i.e. not about dinosaurs) that sets the context of the conversation.
        S: Oh... Okay.;;
        T: What do you know about fossils?;eliciting;Eliciting because this is the first question asked about fossils. 
        S: They’re leftovers of dead animals.;;
        T: So a fossil of a bone is made of bone?;probing;Probing because this is a follow-up question. 
        S: Yeah!;;
        T: Can fossils be only of bones?;probing;Probing because this is a follow-up question. 
        S: No... They can be of feathers, too, and seashells.;;
        T: Very good. Is there any connection between fossils and extinct species?;evaluating,probing;Evaluating and Probing because “very good” tell the student they were right and the question asks more details about fossils which were previously asked about
        S: Not really...;;
        T: Okay. Thank you for talking to me! I now know what we’re going to talk about today.;priming;Priming because this is a meta-message about the conversation and what it was for. 
        *bell rings*;;"""
    try:
        key = os.environ['feedback']
        if key == 'True':
            give_feedback = True
        else:
            give_feedback = False
    except KeyError:
        give_feedback = True
    lines = text.split("\n")
    messages = []
    answers = []
    feedback = []
    for line in lines:
        item = line.split(";")
        print(item)
        messages.append(item[0])
        answers.append(item[1])
        feedback.append(item[2])
    return render(request, 'chat/coding_onboarding.html', {"messages":zip(messages,answers,feedback),"nextpage":"/chat/onboard4","give_feedback":give_feedback})


def onboard4(request):
    text = """T: Hi, Sarah! Is it okay if I ask you a few questions about negative numbers before class? I want to get an idea of what you already know.;priming;Priming because this is a meta-message telling the student what you will be discussing
        S: Okay, Mr. Thomas. What do you want to know?;;
        T: Can you tell me what a negative number is?;eliciting;Eliciting because this is the first question about the definition of a negative number
        S: It’s like if you owe someone something or have to give someone stuff. ;;
        T: Very good. Do you know how to write a negative number?;evaluating,eliciting;Evaluating and Eliciting because this tells the student they were right and then asks the first question about how negative numbers are written
        S: Yeah, you just take the number and put a minus sign in front of it.;;
        T: So, if I write “-3,” what does that mean?;probing;Probing because this is a follow-up question about how negative numbers are written
        S: It means negative three or that someone owes 3 of something.;;
        T: That’s right. Is negative three more or less than zero?;evaluating,eliciting;Evaluating and Eliciting because this tells the student they are correct and then asks about comparing negative numbers
        S: Less. Because having nothing is better than owing someone stuff.;;
        T: That’s right, Sarah. What about -2 and -3? Which do you think is bigger?;evaluating,probing;Evaluating and Probing because this tells the student that they are right and then asks a follow-up question about comparing negative numbers
        S: Well, 3 is bigger than 2, but I would rather owe someone 2 things than 3. So I’m not sure.;;
        T: That’s very good thinking.;evaluating;Evaluating because it tells the student whether they are right. None might make sense too because it fits none of the categories.
        S: So which one is right?;;
        T: I’ll tell you in class, okay?;priming;Priming because this reminds the student of the context for the conversation
        S: Okay.;;
        T: So what happens in we add -3 and 2?;eliciting;Eliciting because this is the first question about adding negative numbers.
        S: Well, if you owe someone 3 apples and then get 2 apples, then you can give them away and only owe 1 apple. So -1, Mr. Thomas?;;
        T: That’s right. What about if we add -3 and -2?;evaluating,probing;Evaluating and Probing because this first tells the student they are correct and then asks a follow-up question about adding negative numbers.
        S: Well if you owe someone 3 apples and owe someone else 2 apples, then together you owe 5 apples. So -5.;;
        T: Nice job! Thanks for talking to me, Sarah.;evaluating,priming;Evaluating and Priming because it firsts tells the student they are correct and the reminds the student of the context.
        S: You’re welcome.;;
        *bell rings*;;"""
    try:
        key = os.environ['feedback']
        if key == 'True':
            give_feedback = True
        else:
            give_feedback = False
    except KeyError:
        give_feedback = True
    lines = text.split("\n")
    messages = []
    answers = []
    feedback = []
    for line in lines:
        item = line.split(";")
        print(item)
        messages.append(item[0])
        answers.append(item[1])
        feedback.append(item[2])
    return render(request, 'chat/coding_onboarding.html', {"messages":zip(messages,answers,feedback),"nextpage":"/","give_feedback":give_feedback})


def code_messages(request):
    try:
        key = os.environ['feedback']
        if key == 'True':
            give_feedback = True
        else:
            give_feedback = False
    except KeyError:
        give_feedback = True
    transcript = get_random_object(Transcript)

    messages = Message.objects.filter(transcript=transcript).order_by('pk')

    text = ""
    for m in messages:
        # feedback should go after the 2nd semicolon
        text += m.text + ";;\n"

    lines = text.split("\n")
    messages = []
    answers = []
    feedback = []
    for line in lines:
        if line != "" and not line.startswith('***'):
            print(line)
            item = line.split(";")
            print(item)
            messages.append(item[0])
            answers.append(item[1])
            feedback.append(item[2])
    if len(messages) == 0:
        return code_messages(request)
    else:
        return render(request, 'chat/coding_onboarding.html', {"messages":zip(messages,answers,feedback),"nextpage":"/chat/code","give_feedback":give_feedback})


def single_player_chat(request, level):
    return render(request, 'chat/single_player_chat.html', {"level":OnboardLevel.objects.get(pk=level)})