from django.conf.urls import url
from django.views.generic import TemplateView
import views

from bpam.decorators import DEBUG_ONLY_VIEW

urlpatterns = [
    # url(r'^api/v2/', include(router.urls)),
    url(r'^$', DEBUG_ONLY_VIEW(views.SepsisView.as_view()), name='index'),
    url(r'^samples', views.SampleListView.as_view(), name='samples'),
    url(r'^sample/(?P<package_id>[^\/]+)/?$', views.SampleDetailView.as_view(), name='sample'),
    url(r'^sample/(?P<resource_type>[^/]+)/(?P<status>[\w-]+)/(?P<package_id>[^\/]+)/?$', views.SampleDetailView.as_view(), name='sample'),
    # in CKAN
    url(r'^transcriptomicshiseqfiles', views.TranscriptomicsHiseqFileListView.as_view(), name='transcriptomics_hiseq_files'),
    url(r'^genomicsmiseqfiles', views.GenomicsMiseqFileListView.as_view(), name='genomics_miseq_files'),
    url(r'^genomicspacbiofiles', views.GenomicsPacBioFileListView.as_view(), name='genomics_pacbio_files'),
    url(r'^metabolomicslcmsfiles', views.MetabolomicsLCMSFileListView.as_view(), name='metabolomics_lcms_files'),
    url(r'^proteomicsms1files', views.ProteomicsMS1QuantificationFileListView.as_view(), name='proteomics_ms1_files'),
    url(r'^proteomicsswathfiles', views.ProteomicsSwathMSListView.as_view(), name='proteomics_swath_files'),
    url(r'^ckan_refresh/?$', views.CKANRefresh.as_view(), name='ckan_refresh'),

    # BEGIN----- Tracker URLs ----------
    url(r'^overview/?$',
        TemplateView.as_view(template_name='sepsis/project_overview.html'),
        name='overview'),

    # END------- Tracker URLs ----------
]
