from django.conf.urls import patterns, url

from . import views
from . import data_export

urlpatterns = patterns(
    '',
    url(
        regex=r'^$',
        view=views.BarcodeView.as_view(),
        name='index'),
    url(
        regex=r'^contacts$',
        view=views.ContactsView.as_view(),
        name='contacts'),
    url(
        regex=r'^sheets/(?P<pk>.*)/$',
        view=views.SheetDetailView.as_view(),
        name='sheet'),
    url(
        regex=r'^sheets',
        view=views.SheetListView.as_view(),
        name='sheets'),
    url(
        regex=r'^sheets/csv',
        view=data_export.get_sheets,
        name='sheets_csv'),
)
