from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns(
    '',
    url(
        regex=r'^$',
        view=views.PathogensView.as_view(),
        name='index'),
)
