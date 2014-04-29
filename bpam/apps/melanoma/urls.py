from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns(
    '',
    url(
        regex=r'^sequencefiles',
        view=views.MelanomaSequenceFileListView.as_view(),
        name='sequencefiles'),
    url(
        regex=r'^sample/(?P<pk>.*)/$',
        view=views.SampleDetailView.as_view(),
        name='sampledetail'),
    url(
        regex=r'^arrays',
        view=views.ArrayListView.as_view(),
        name='arrays'),
    url(
        regex=r'search/(.*)$',
        view=views.search_view,
        name="search"),
    url(
        regex=r'^$',
        view=views.IndexView.as_view(),
        name='index'),
)
