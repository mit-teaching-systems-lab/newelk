from .models import MessageCode

def process_codes(request):
    checked = []
    for item in request.POST:
        if not item == "csrfmiddlewaretoken":
            print(item)
            checked.append(item)
            u, c, n = item.split("_")
            if request.user.is_authenticated:
                MessageCode.objects.create(url=str(u), other_id=str(n), code=c, user=request.user)
            else:
                MessageCode.objects.create(url=str(u), other_id=str(n), code=c)
    return checked