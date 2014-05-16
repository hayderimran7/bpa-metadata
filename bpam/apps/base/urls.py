from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns(
    '',
    url(
        regex=r'^$',
        view=views.BaseView.as_view(),
        name='index'),
    url(
        regex=r'^search/?$',
        view=views.BASESearchView.as_view(),
        name='search'),
    url(
        regex=r'^lookup/(?P<search_field>.*)',
        view=views.StandardisedVocabularyLookUpView.as_view(),
        name='lookup'),
    url(
        regex=r'^taxonomy/(?P<level>.*)/(?P<taxon>.*)',
        view=views.TaxonomyLookUpView.as_view(),
        name='taxonomy',
    ),
    url(
        regex=r'^contacts$',
        view=views.ContactsView.as_view(),
        name='contacts'),
    url(
        regex=r'^accessrequest',
        view=views.RequestAccess.as_view(),
        name='requestaccess'),
    url(
        regex=r'^searchexport',
        view=views.SearchExportView.as_view(),
        name='searchexport'),
    url(
        regex=r'^contextexport',
        view=views.ContextExportView.as_view(),
        name='contextexport'),
    url(
        regex=r'^otuexport',
        view=views.OTUExportView.as_view(),
        name='otuexport'),
)
