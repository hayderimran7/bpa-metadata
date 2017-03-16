from django.conf.urls import patterns, url

from . import views
import data_export

from bpam.decorators import DEBUG_ONLY_VIEW

urlpatterns = patterns(
    '',
    url(r'^$', DEBUG_ONLY_VIEW(views.GBRView.as_view()), name='index'),

    url(r'^collections', views.CollectionEventListView.as_view(), name='collections'),
    url(r'^collection/?.*/$', views.CollectionView.as_view(), name='collection'),

    url(r'^samples/csv', data_export.get_samples, name='samples_csv'),
    url(r'^samples', views.SampleListView.as_view(), name='samples'),

    url(r'^sites', views.CollectionSiteListView.as_view(), name='sites'),
    url(r'^site/(?P<pk>.*)/$', views.CollectionSiteDetailView.as_view(), name='site'),
    url(r'^sample/(?P<pk>.*)/$', views.SampleDetailView.as_view(), name='sample'),

    url(r'^sequencefiles/csv', data_export.get_sequencefiles, name='sequencefiles_csv'),
    url(r'^sequencefiles', views.SequenceFileListView.as_view(), name='sequencefiles'),

    url(r'^contacts$', views.ContactsView.as_view(), name='contacts'),
)
