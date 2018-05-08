from django.shortcuts import render, redirect
from research.models import Transcript, TFAnswer


# Create your views here.
def profile(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')
    transcripts = Transcript.objects.filter(users=request.user).order_by("creation_time")
    latest_transcript = transcripts.latest("creation_time")
    participants = latest_transcript.users.distinct()
    quiz_results = {}
    for person in participants:
        answers = TFAnswer.objects.filter(transcript=latest_transcript,user=person)
        quiz_results[person.username] = {}
        quiz_results["correct_answer"] = {}
        for answer in answers:
            quiz_results[person.username][answer.pk] = answer.user_answer
            quiz_results["correct_answer"][answer.pk] = answer.correct_answer

    return render(request, 'profile.html',{"transcripts": transcripts, "quiz_results": quiz_results})