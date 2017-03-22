from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from bpam.decorators import DEBUG_ONLY_VIEW

from . import views

urlpatterns = patterns(
    '',
    url(r'^$', DEBUG_ONLY_VIEW(views.IndexView.as_view()), name='index'),
    url(r'^samples', views.SampleListView.as_view(), name='samples'),
    url(r'^sample/(?P<pk>.*)/$', views.SampleDetailView.as_view(), name='sample'),
    url(r'^sequencefiles', views.SequenceFileListView.as_view(), name='sequencefiles'),
    url(r'^arrays', views.ArrayListView.as_view(), name='arrays'),
    url(r'search/(.*)$', views.search_view, name="search"),
)

urlpatterns += staticfiles_urlpatterns()
