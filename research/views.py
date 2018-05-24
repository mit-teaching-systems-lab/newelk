from django.shortcuts import render

# Create your views here.




# https://docs.djangoproject.com/en/2.0/howto/outputting-csv/
import csv
from .models import Message

from django.http import StreamingHttpResponse

class Echo:
    """An object that implements just the write method of the file-like
    interface.
    """
    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value

def streaming_csv_view(request):
    """A view that streams a large CSV file."""
    # Generate a sequence of rows. The range is based on the maximum number of
    # rows that can be handled by a single sheet in most spreadsheet
    # applications.
    # rows = (["Row {}".format(idx), str(idx)] for idx in range(65536))
    rows = Message.objects.all().order_by("transcript", "-creation_time")
    pseudo_buffer = Echo()
    # writer = csv.writer(pseudo_buffer)
    # response = StreamingHttpResponse((writer.writerow(str(row)) for row in rows),
    #                                  content_type="text/csv")
    response = StreamingHttpResponse((str(row) + '\n' for row in rows),
                                     content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="data.csv"'
    return response