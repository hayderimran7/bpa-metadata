from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns(
    '',
    url(
        regex=r'^chemical',
        view=views.ChemicalAnalysisListView.as_view(),
        name='chemicalanalysis'),
)
