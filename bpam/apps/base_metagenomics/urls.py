from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns(
    '',
    url(
        regex=r'^samples',
        view=views.SampleListView.as_view(),
        name='samples'),
    url(
        regex=r'^sample/(?P<bpa_id>\d{3,}.*)$',
        view=views.SampleDetailView.as_view(),
        name='sample'),
)
