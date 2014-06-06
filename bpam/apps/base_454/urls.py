from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns(
    '',
    url(
        regex=r'^samples',
        view=views.Sample454ListView.as_view(),
        name='454samples'),
    url(
        regex=r'^sample/(?P<pk>.*)/$',
        view=views.Sample454DetailView.as_view(),
        name='454sampledetail'),
)
