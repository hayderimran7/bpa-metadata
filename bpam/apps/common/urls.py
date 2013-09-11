
from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required, permission_required

from apps.common.views import search_view

urlpatterns = patterns('',
    url(r'^search/(.*)', search_view, name="melanoma-list"),
)

