from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns(
    '',
    url(
        regex=r'^files/csv',
        view=views.get_file_csv,
        name='files_csv'),
    url(
        regex=r'^metagenomics',
        view=views.IndexView.as_view(),
        name='metagenomics'),
    url(
        regex=r'^files',
        view=views.FileListView.as_view(),
        name='files'),
    url(
        regex=r'^extractions',
        view=views.ExtractionListView.as_view(),
        name='extractions'),
    url(
        regex=r'^samples',
        view=views.SampleListView.as_view(),
        name='samples'),
    url(
        regex=r'^runs',
        view=views.RunListView.as_view(),
        name='runs'),
    url(
        regex=r'^sample/(?P<bpa_id>\d{3,}.*)$',
        view=views.SampleDetailView.as_view(),
        name='sample'),
)
