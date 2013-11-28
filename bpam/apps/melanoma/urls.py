from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from apps.melanoma.views import MelanomaSequenceFileListView, search_view, index

urlpatterns = patterns(
    '',
    url(r'^$', login_required(index), name="melanoma-index"),
    url(r'^all$', login_required(MelanomaSequenceFileListView.as_view()), name="melanoma-list"),
    url(r'search/(.*)$', login_required(search_view), name="melanoma-search"),
)
