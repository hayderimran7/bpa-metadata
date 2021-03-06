from django.conf.urls import url

import views

urlpatterns = [
    url(regex=r'^$', view=views.IndexView.as_view(), name='index'),
    url(regex=r'^chemicalanalyses/(?P<bpa_id>\d{3,}.*)$',
        view=views.ChemicalAnalysisDetailView.as_view(),
        name='chemicalanalysisdetail'),
    url(regex=r'^chemical', view=views.ChemicalAnalysisListView.as_view(),
        name='chemicalanalysis'),
    url(regex=r'^sites/(?P<pk>\d+)/$',
        view=views.CollectionSiteDetailView.as_view(),
        name='collectionsitedetail'),
    url(regex=r'^sites', view=views.CollectionSiteListView.as_view(),
        name='collectionsites'),
    url(regex=r'^sample/(?P<bpa_id>\d{3,}.*)$',
        view=views.SampleContextDetailView.as_view(),
        name='sampledetail'),
    url(regex=r'^samples', view=views.SampleContextListView.as_view(),
        name='samples'),
    url(regex=r'^samplematrix/csv', view=views.get_matrix_csv,
        name='samplematrix_csv'),
    url(regex=r'^samplematrix', view=views.SampleMatrixListView.as_view(),
        name='samplematrix'),
]
