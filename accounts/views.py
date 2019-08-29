from django.shortcuts import render, redirect

from research.models import Transcript, TFAnswer, Message


# Create your views here.
def profile(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    transcripts = Transcript.objects.filter(users=request.user).order_by(
        "-creation_time"
    )
    quiz_results = {}
    playercount = 0
    if transcripts:
        for t in transcripts:
            t.messages = Message.objects.filter(transcript=t).order_by("creation_time")
            if not t.messages:
                t.messages = {}
                t.messages["text"] = "no text found!"
        latest_transcript = transcripts.latest("creation_time")
        participants = latest_transcript.users.distinct()
        scenario = latest_transcript.scenario
        for person in participants:
            answers = TFAnswer.objects.filter(
                question__scenario=scenario, user=person, transcript=latest_transcript
            )
            # answers = TFAnswer.objects.filter(transcript=latest_transcript,user=person)
            quiz_results[person.username] = {}
            quiz_results["question_details"] = {}
            for answer in answers:
                quiz_results[person.username][answer.question.pk] = answer.user_answer
                quiz_results["question_details"][answer.question.pk] = {
                    answer.question.question: answer.correct_answer
                }
        playercount = participants.count
    else:
        transcripts = None
    print("showing profile")
    print(quiz_results)
    return render(
        request,
        "profile.html",
        {
            "transcripts": transcripts,
            "quiz_results": quiz_results,
            "participant_count": playercount,
        },
    )


def about(request):
    return render(request, "about.html")
