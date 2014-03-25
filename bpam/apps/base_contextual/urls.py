from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns(
    '',
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
)
