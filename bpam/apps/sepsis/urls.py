from django.conf.urls import url
from rest_framework import routers
import views

from bpam.decorators import DEBUG_ONLY_VIEW

router = routers.DefaultRouter()
router.register(r"sepsis_samples", views.SepsisSampleViewSet)
router.register(r"hosts", views.HostViewSet)
router.register(r"project", views.BPAProjectViewSet)
router.register(r"bpa_ids", views.BPAIDViewSet)
router.register(r"track_genomics", views.GenomicsMiseqFileViewSet)
router.register(r"genomic_miseq_files", views.GenomicsMiseqFileViewSet)
router.register(r"genomic_pacbio_files", views.GenomicsPacBioFileViewSet)

router.register(r"track_pacbio", views.PacBioTrackViewSet)
router.register(r"track_miseq", views.MiSeqTrackViewSet)
router.register(r"track_rna_hiseq", views.RNAHiSeqTrackViewSet)
router.register(r"track_metabolomics", views.MetabolomicsTrackViewSet)
router.register(r"track_deeplc", views.DeepLCMSTrackViewSet)
router.register(r"track_swath", views.SWATHMSTrackViewSet)

urlpatterns = [
    # url(r'^api/v2/', include(router.urls)),
    url(r'^$', DEBUG_ONLY_VIEW(views.SepsisView.as_view()), name='index'),
    url(r'^samples', views.SampleListView.as_view(), name='samples'),
    url(r'^sample/(?P<pk>.*)/$', views.SampleDetailView.as_view(), name='sample'),
    url(r'^genomicsmiseqfiles', views.GenomicsMiseqFileListView.as_view(), name='genomics_miseq_files'),
    url(r'^transcriptomicshiseqfiles', views.TranscriptomicsHiseqFileListView.as_view(), name='transcriptomics_hiseq_files'),
    url(r'^genomicspacbiofiles', views.GenomicsPacBioFileListView.as_view(), name='genomics_pacbio_files'),

    # BEGIN----- Tracker URLs ----------

    url(r'^overview/$', views.TrackOverview.as_view(), name='overview'),

    url(r'^overview/data/$', views.TrackOverviewConstraints.as_view(), name='overview_constraints'),

    url(r'^overview/(?P<constraint>.*)/(?P<status>.*)/$', views.TrackDetails.as_view(), name='overview_detail'),

    # END------- Tracker URLs ----------
]
