from django.conf.urls import url, include

from bpam.decorators import DEBUG_ONLY_VIEW

import views

urlpatterns = [
    url(r'^$', DEBUG_ONLY_VIEW(views.BaseView.as_view()), name='index'),
    url(r'^search/?$', views.BASESearchView.as_view(), name='search'),
    url(r'^lookup/(?P<search_field>.*)', views.StandardisedVocabularyLookUpView.as_view(), name='lookup'),
    url(r'^taxonomy/(?P<level>.*)/(?P<taxon>.*)', views.TaxonomyLookUpView.as_view(), name='taxonomy'),
    url(r'^requestaccess', views.RequestAccessView.as_view(), name='requestaccess'),
    url(r'^searchexport', views.SearchExportView.as_view(), name='searchexport'),
    url(r'^docs/', include('rest_framework_swagger.urls')),
]
