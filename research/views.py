from .models import Message, TFAnswer
from datetime import timedelta
from django.http import StreamingHttpResponse, HttpResponse
from django.utils import timezone


class Echo:
    """An object that implements just the write method of the file-like
    interface.
    """
    def __init__(self, column_headers):
        self.header = column_headers
        self.header_written = False
    def write(self, value):
        if not self.header_written:
            value = self.header + '\n' + str(value)
            self.header_written = True
        """Write the value by returning it, instead of storing in a buffer."""
        value_string = str(value) + '\n'
        return value_string.encode('utf-8')

def filtered_data_as_http_response(rows, headers, filename):
    if rows:
        pseudo_buffer = Echo(headers)
        response = StreamingHttpResponse((pseudo_buffer.write(row) for row in rows),
                                         content_type="text/csv")
        response['Content-Disposition'] = 'attachment; filename="' + filename + '"'
    else:
        response = HttpResponse("No data found with current filters")
    return response

def streaming_chat_csv(request):
    """A view that streams a large CSV file."""
    # rows = (["Row {}".format(idx), str(idx)] for idx in range(65536))
    yesterday = timezone.now() - timedelta(days=1)
    rows = Message.objects.filter(creation_time__gt=yesterday).order_by("transcript", "creation_time")
    return filtered_data_as_http_response(rows,
                         "group_id,room_name,scenario,username,role,message_id,message_text,time",
                         "chatlogs.csv")

def streaming_answers_view(request):
    yesterday = timezone.now() - timedelta(days=1)
    rows = TFAnswer.objects.filter(creation_time__gt=yesterday).order_by("transcript")
    return filtered_data_as_http_response(rows,
                         "group_id,username,question_id,question,correct_answer,user_response",
                         "answerlogs.csv")