from django.http import HttpResponse


def homepage(request):
    return HttpResponse("Hello, world. You're at the weather index.")