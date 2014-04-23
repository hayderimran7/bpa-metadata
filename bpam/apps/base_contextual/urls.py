from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns(
    '',
    url(
        regex=r'^$',
        view=views.LandingView.as_view(),
        name='index'),
    url(
        regex=r'^chemical',
        view=views.ChemicalAnalysisListView.as_view(),
        name='chemicalanalysis'),
    url(
        regex=r'^sites/(?P<pk>\d+)/$',
        view=views.CollectionSiteDetailView.as_view(),
        name='collectionsitedetail'),
    url(
        regex=r'^sites',
        view=views.CollectionSiteListView.as_view(),
        name='collectionsites'),
    url(
        regex=r'^sample/(?P<pk>.*)/$',
        view=views.SampleContextDetailView.as_view(),
        name='sampledetail'),
    url(
        regex=r'^samples',
        view=views.SampleContextListView.as_view(),
        name='samples'),
)
