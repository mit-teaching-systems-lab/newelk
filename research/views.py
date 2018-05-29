from .models import Message, TFAnswer

from django.http import StreamingHttpResponse

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

def streaming_chat_csv(request):
    """A view that streams a large CSV file."""
    # rows = (["Row {}".format(idx), str(idx)] for idx in range(65536))
    rows = Message.objects.all().order_by("transcript", "creation_time")
    headers = "group_id,room_name,scenario,username,role,message_id,message_text,time"
    pseudo_buffer = Echo(headers)
    response = StreamingHttpResponse((pseudo_buffer.write(row) for row in rows),
                                     content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="chatlogs.csv"'
    return response

def streaming_answers_view(request):
    rows = TFAnswer.objects.all().order_by("transcript")
    headers = "group_id,username,question,correct_answer,user_response"
    pseudo_buffer = Echo(headers)
    response = StreamingHttpResponse((pseudo_buffer.write(row) for row in rows),
                                     content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="answerlogs.csv"'
    return response