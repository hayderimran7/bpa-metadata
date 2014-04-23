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
        regex=r'^autocomplete/(?P<search_field>.*)',
        view=views.AutoCompleteView.as_view(),
        name='auto_complete'),
)
