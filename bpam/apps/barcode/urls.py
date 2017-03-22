from django.conf.urls import patterns, url

from bpam.decorators import DEBUG_ONLY_VIEW

from . import views

urlpatterns = patterns(
    '',
    url(r'^$', DEBUG_ONLY_VIEW(views.BarcodeIndex.as_view()), name='index'),
    url(r'^pilbara_flora$', views.PilbaraFloraIndex.as_view(), name='pilbara_index'),
    url(r'^pilbara_flora/sheets/(?P<pk>.*)/$', views.SheetDetailView.as_view(), name='pilbara_sheet'),
    url(r'^pilbara_flora/sheets', views.SheetListView.as_view(), name='pilbara_sheets'),
    url(r'^pilbara_flora/sites', views.PilbaraCollectionSiteListView.as_view(), name='pilbara_sites'),
)
