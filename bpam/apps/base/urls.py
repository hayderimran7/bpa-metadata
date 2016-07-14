from django.conf.urls import url, include

import views

urlpatterns = [
    url(regex=r'^$', view=views.BaseView.as_view(),
        name='index'),
    url(regex=r'^search/?$', view=views.BASESearchView.as_view(),
        name='search'),
    url(regex=r'^lookup/(?P<search_field>.*)',
        view=views.StandardisedVocabularyLookUpView.as_view(),
        name='lookup'),
    url(regex=r'^taxonomy/(?P<level>.*)/(?P<taxon>.*)',
        view=views.TaxonomyLookUpView.as_view(),
        name='taxonomy'),
    url(regex=r'^contacts$', view=views.ContactsView.as_view(),
        name='contacts'),
    url(regex=r'^acknowledgements$',
        view=views.AcknowledgementView.as_view(),
        name='acknowledgement'),
    url(regex=r'^information$',
        view=views.InfoView.as_view(),
        name='information'),
    url(regex=r'^requestaccess',
        view=views.RequestAccessView.as_view(),
        name='requestaccess'),
    url(regex=r'^searchexport',
        view=views.SearchExportView.as_view(),
        name='searchexport'),
    url(r'^docs/', include('rest_framework_swagger.urls')),
]
