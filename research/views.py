import os

from django.http import StreamingHttpResponse, HttpResponse
from django.shortcuts import render, redirect
from rest_framework import viewsets

from .models import Message, TFAnswer, Transcript
from .serializers import TFAnswerSerializer


class TFAnswerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = TFAnswer.objects.all()
    serializer_class = TFAnswerSerializer

    def get_queryset(self):
        print("getting queryset from api")
        user = self.request.user
        print(user)
        transcript = Transcript.objects.filter(users=user).latest("creation_time")
        print(transcript)
        participants = transcript.users.distinct()
        scenario = transcript.scenario
        all_answers = TFAnswer.objects.none()
        for person in participants:
            print(person)
            player_answers = TFAnswer.objects.filter(
                question__scenario=scenario, user=person, transcript=transcript
            )
            all_answers = all_answers | player_answers

        return all_answers


class Echo:
    """An object that implements just the write method of the file-like
    interface.
    """

    def __init__(self, column_headers):
        self.header = column_headers
        self.header_written = False

    def write(self, value):
        if not self.header_written:
            value = self.header + "\n" + str(value)
            self.header_written = True
        """Write the value by returning it, instead of storing in a buffer."""
        value_string = str(value) + "\n"
        return value_string.encode("utf-8")


def filtered_data_as_http_response(rows, headers, filename):
    if rows:
        pseudo_buffer = Echo(headers)
        response = StreamingHttpResponse(
            (pseudo_buffer.write(row) for row in rows), content_type="text/csv"
        )
        response["Content-Disposition"] = 'attachment; filename="' + filename + '"'
    else:
        response = HttpResponse("No data found with current filters")
    return response


def streaming_chat_csv(request):
    """A view that streams a large CSV file."""
    # yesterday = timezone.now() - timedelta(days=1)
    # rows = Message.objects.filter(creation_time__gt=yesterday).order_by("transcript", "creation_time")
    rows = Message.objects.all().order_by("transcript", "creation_time")
    return filtered_data_as_http_response(
        rows,
        "group_id,room_name,scenario,username,role,message_id,message_text,time",
        "chatlogs.csv",
    )


def streaming_answers_view(request):
    # yesterday = timezone.now() - timedelta(days=1)
    # rows = TFAnswer.objects.filter(creation_time__gt=yesterday).order_by("transcript")
    rows = TFAnswer.objects.all().order_by("transcript")
    return filtered_data_as_http_response(
        rows,
        "group_id,username,question_id,question,correct_answer,user_response",
        "answerlogs.csv",
    )


def toggle_feedback(request):
    try:
        key = os.environ["feedback"]
        if key == "True":
            feedback = True
        else:
            feedback = False
    except KeyError:
        feedback = True
        os.environ["feedback"] = "True"
    if request.POST:
        os.environ["feedback"] = str(not feedback)
        return redirect("/research/feedback/")
    return render(request, "research/toggle_feedback.html", {"feedback": feedback})
