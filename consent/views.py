from django.shortcuts import render


# Create your views here.

def presurvey(request):
    return render(request, 'presurvey.html')
