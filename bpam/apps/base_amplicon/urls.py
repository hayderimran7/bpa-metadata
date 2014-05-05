from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns(
    '',
    url(
        regex=r'^all_metadata',
        view=views.MetadataListView.as_view(),
        name='all_metadata'),
    url(
        regex=r'^metadata/(?P<pk>.*)/$',
        view=views.MetadataView.as_view(),
        name='metadata'),
)
