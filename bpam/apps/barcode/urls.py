from django.conf.urls import patterns, url

from . import views
from . import data_export

urlpatterns = patterns(
    "",
    url(
        regex=r"^$",
        view=views.BarcodeIndex.as_view(),
        name="index"),
    url(
        regex=r"^pilbara_flora$",
        view=views.PilbaraFloraIndex.as_view(),
        name="pilbara_index"),
    url(
        regex=r"^contacts$",
        view=views.ContactsView.as_view(),
        name="contacts"),
    url(
        regex=r"^pilbara_flora/sheets/(?P<pk>.*)/$",
        view=views.SheetDetailView.as_view(),
        name="pilbara_sheet"),
    url(
        regex=r"^pilbara_flora/sheets",
        view=views.SheetListView.as_view(),
        name="pilbara_sheets"),
    url(
        regex=r"^pilbara_flora/sites",
        view=views.PilbaraCollectionSiteListView.as_view(),
        name="pilbara_sites"),
)
