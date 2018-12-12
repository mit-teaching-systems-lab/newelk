from .models import MessageCode
import random
from django.db.models import Max

#
# def process_codes(request):
#     checked = []
#     for item in request.POST:
#         if not item == "csrfmiddlewaretoken":
#             print(item)
#             checked.append(item)
#             u, c, n = item.split("_")
#             if request.user.is_authenticated:
#                 MessageCode.objects.create(url=str(u), other_id=str(n), code=c, user=request.user)
#             else:
#                 MessageCode.objects.create(url=str(u), other_id=str(n), code=c)
#     return checked


def get_random_object(obj):
    max_id = obj.objects.all().aggregate(max_id=Max("id"))['max_id']
    while True:
        pk = random.randint(1, max_id)
        random_obj = obj.objects.filter(pk=pk).first()
        if random_obj:
            return random_obj