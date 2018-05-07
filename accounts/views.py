from django.shortcuts import render
from research.models import Transcript


# Create your views here.
def profile(request):
    transcripts = Transcript.objects.filter(users=request.user).order_by("creation_time")
    # scores =

    return render(request, 'profile.html',{"transcripts": transcripts})