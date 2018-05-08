from django.shortcuts import render
from research.models import Transcript, TFAnswer


# Create your views here.
def profile(request):
    transcripts = Transcript.objects.filter(users=request.user).order_by("creation_time")
    latest_transcript = transcripts.latest("creation_time")

    answers = TFAnswer.objects.filter(transcript=latest_transcript.pk,users=latest_transcript.users)


    # for user in latest_transcript.users:


    return render(request, 'profile.html',{"transcripts": transcripts, "answers": answers})