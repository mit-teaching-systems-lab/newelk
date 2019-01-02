import random

from django.db.models import Max


def get_random_object(obj):
    max_id = obj.objects.all().aggregate(max_id=Max("id"))['max_id']
    while True:
        pk = random.randint(1, max_id)
        random_obj = obj.objects.filter(pk=pk).first()
        if random_obj:
            return random_obj
