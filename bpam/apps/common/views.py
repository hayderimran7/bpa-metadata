
from django.http import HttpResponse

def search_view(request, term):
    return HttpResponse(term)
