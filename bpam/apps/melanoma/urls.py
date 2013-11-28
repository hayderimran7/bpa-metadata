from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from apps.melanoma.views import MelanomaSequenceFileListView, search_view

urlpatterns = patterns(
    '',
    url(r'^$', login_required(MelanomaSequenceFileListView.as_view()), name="melanoma-list"),
    url(r'search/(.*)$', search_view, name="melanoma-search"),
)
