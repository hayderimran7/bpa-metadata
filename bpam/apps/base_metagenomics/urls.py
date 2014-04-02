from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns(
    '',
    url(
        regex=r'^samples',
        view=views.SampleListView.as_view(),
        name='metagenomicssamples'),
)
