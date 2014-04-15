from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns(
    '',
    url(
        regex=r'^$',
        view=views.BaseView.as_view(),
        name='index'),
    url(
        regex=r'^search/?$',
        view=views.OTUSearchView.as_view(),
        name='otusearch'),
    url(
        regex=r'^options/(?P<thing>\w*)',
        view=views.OTUAutoCompleteView.as_view(),
        name='search_auto_complete'),
)
