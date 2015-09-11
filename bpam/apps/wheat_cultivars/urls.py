from django.conf.urls import patterns, url

from . import views
from . import data_export

urlpatterns = patterns(
    '',
    url(
        regex=r'^$',
        view=views.IndexView.as_view(),
        name='index'),
    url(
        regex=r'^samples',
        view=views.SampleListView.as_view(),
        name='samples'),
    url(
        regex=r'^sample/(?P<pk>.*)/$',
        view=views.SampleDetailView.as_view(),
        name='sample'),
    url(
        regex=r'^sequencefiles/csv',
        view=data_export.get_sequencefiles,
        name='sequencefiles_csv'),
    url(
        regex=r'^sequencefiles',
        view=views.SequenceFileListView.as_view(),
        name='sequencefiles'),
    url(
        regex=r'^contacts$',
        view=views.ContactsView.as_view(),
        name='contacts'),
)
