from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render_to_response

def melanoma_list(request):
    return render_to_response('melanoma_list.html',
                              context_instance=RequestContext(request))
