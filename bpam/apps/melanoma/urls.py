from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns(
    '',
    url(
        regex=r'^sequencefiles',
        view=views.MelanomaSequenceFileListView.as_view(),
        name='sequencefiles'),
    url(
        regex=r'^arrays',
        view=views.ArrayListView.as_view(),
        name='arrays'),
    url(
        regex=r'search/(.*)$',
        view=views.search_view,
        name="search"),
)
