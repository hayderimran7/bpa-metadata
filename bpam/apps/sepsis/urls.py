from django.conf.urls import url
import views

from bpam.decorators import DEBUG_ONLY_VIEW

urlpatterns = [
    # url(r'^api/v2/', include(router.urls)),
    url(r'^$', DEBUG_ONLY_VIEW(views.SepsisView.as_view()), name='index'),
    url(r'^bacterialcontextualdata', views.SampleListView.as_view(), name='samples'),
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
        views.CKANTemplateView.as_view(template_name='sepsis/project_overview.html'),
        name='overview'),

    # END------- Tracker URLs ----------
]
